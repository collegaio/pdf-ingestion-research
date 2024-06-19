from typing import Dict, Any, Optional, Tuple, List, Set, Optional

from llama_index.core.llms import LLM
from llama_index.core.agent.react.types import (
    ActionReasoningStep,
    ObservationReasoningStep,
    ResponseReasoningStep,
)
from llama_index.core.agent.react.output_parser import ReActOutputParser
from llama_index.core.agent import (
    Task,
    AgentChatResponse,
    ReActChatFormatter,
    QueryPipelineAgentWorker,
)
from llama_index.core.agent.types import Task
from llama_index.core.query_pipeline import (
    QueryPipeline,
    AgentInputComponent,
    AgentFnComponent,
    CustomAgentComponent,
    QueryComponent,
    ToolRunnerComponent,
    InputComponent,
    Link,
)
from llama_index.core.llms import MessageRole, ChatResponse, ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.callbacks import CallbackManager


## Agent Input Component
## This is the component that produces agent inputs to the rest of the components
## Can also put initialization logic here.
def agent_input_fn(task: Task, state: Dict[str, Any]) -> Dict[str, Any]:
    """Agent input function.

    Returns:
        A Dictionary of output keys and values. If you are specifying
        src_key when defining links between this component and other
        components, make sure the src_key matches the specified output_key.

    """
    # initialize current_reasoning
    if "current_reasoning" not in state:
        state["current_reasoning"] = []
    reasoning_step = ObservationReasoningStep(observation=task.input)
    state["current_reasoning"].append(reasoning_step)
    return {"input": task.input}


## define prompt function
def react_prompt_fn(
    task: Task,
    state: Dict[str, Any],
    input: str,
    tools: List[BaseTool],
    context: str,
) -> List[ChatMessage]:
    # Add input to reasoning
    # TODO: may need to redo prompts
    chat_formatter = ReActChatFormatter.from_defaults(context=context)
    return chat_formatter.format(
        tools,
        chat_history=task.memory.get() + state["memory"].get_all(),
        current_reasoning=state["current_reasoning"],
    )


def parse_react_output_fn(
    task: Task, state: Dict[str, Any], chat_response: ChatResponse
):
    """Parse ReAct output into a reasoning step."""
    output_parser = ReActOutputParser()
    reasoning_step = output_parser.parse(chat_response.message.content)
    return {"done": reasoning_step.is_done, "reasoning_step": reasoning_step}


# TODO: convert tools
# def determine_chances(query_str: str, chat_history: List[str]):
#     response = chances_query_chain.run(
#         input=query_str,
#         chat_history=chat_history,
#     )
#     return response


# tool = FunctionTool.from_defaults(
#     determine_chances,
#     # async_fn=aget_weather,  # optional!
# )


def run_tool_fn(
    task: Task,
    state: Dict[str, Any],
    reasoning_step: ActionReasoningStep,
    tools: List[BaseTool],
):
    """Run tool and process tool output."""
    # TODO: take tool retriever from args
    tool_runner_component = ToolRunnerComponent(
        tools, callback_manager=task.callback_manager
    )
    tool_output = tool_runner_component.run_component(
        tool_name=reasoning_step.action,
        tool_input=reasoning_step.action_input,
    )
    observation_step = ObservationReasoningStep(observation=str(tool_output))
    state["current_reasoning"].append(observation_step)

    return {"response_str": observation_step.get_content(), "is_done": False}


def process_response_fn(
    task: Task, state: Dict[str, Any], response_step: ResponseReasoningStep
):
    """Process response."""
    state["current_reasoning"].append(response_step)
    response_str = response_step.response
    # Now that we're done with this step, put into memory
    state["memory"].put(ChatMessage(content=task.input, role=MessageRole.USER))
    state["memory"].put(ChatMessage(content=response_str, role=MessageRole.ASSISTANT))

    return {"response_str": response_str, "is_done": True}


def process_agent_response_fn(task: Task, state: Dict[str, Any], response_dict: dict):
    """Process agent response."""
    return (
        AgentChatResponse(response_dict["response_str"]),
        response_dict["is_done"],
    )


def create_chat_agent_query_pipeline(
    llm: LLM, tools: BaseTool = [], context: str = None
):
    qp = QueryPipeline(verbose=True)

    qp.add_modules(
        {
            "agent_input": AgentInputComponent(fn=agent_input_fn),
            "react_prompt": AgentFnComponent(
                fn=react_prompt_fn, partial_dict={"tools": tools, "context": context}
            ),
            "llm": llm,
            "react_output_parser": AgentFnComponent(fn=parse_react_output_fn),
            "run_tool": AgentFnComponent(fn=run_tool_fn, partial_dict={"tools": tools}),
            "process_response": AgentFnComponent(fn=process_response_fn),
            "process_agent_response": AgentFnComponent(fn=process_agent_response_fn),
        }
    )

    # link input to react prompt to parsed out response (either tool action/input or observation)
    qp.add_chain(["agent_input", "react_prompt", "llm", "react_output_parser"])

    # add conditional link from react output to tool call (if not done)
    qp.add_link(
        "react_output_parser",
        "run_tool",
        condition_fn=lambda x: not x["done"],
        input_fn=lambda x: x["reasoning_step"],
    )
    # add conditional link from react output to final response processing (if done)
    qp.add_link(
        "react_output_parser",
        "process_response",
        condition_fn=lambda x: x["done"],
        input_fn=lambda x: x["reasoning_step"],
    )

    # whether response processing or tool output processing, add link to final agent response
    qp.add_link("process_response", "process_agent_response")
    qp.add_link("run_tool", "process_agent_response")

    return qp


def create_chat_agent(qp: QueryPipeline, chat_history: List[ChatMessage]):
    agent_worker = QueryPipelineAgentWorker(qp)

    return agent_worker.as_agent(
        callback_manager=CallbackManager([]),
        chat_history=chat_history,
        verbose=True,
    )


# start task
# await agent.achat("What are my chances at UGA?")
