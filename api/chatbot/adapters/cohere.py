from tabnanny import verbose
from typing import List

from llama_index.llms.cohere import Cohere
from llama_index.core.agent import ReActAgent, ReActChatFormatter
from llama_index.core.objects import ObjectRetriever
from llama_index.core.tools import BaseTool
from llama_index.core.llms import ChatMessage

from chatbot.server.conversations.model import ChatHistoryMessage
from chatbot.chat.ports import ChatMessageHandler


class CohereChatAdapter(ChatMessageHandler):
    def __init__(self, api_key: str, tool_retriever: ObjectRetriever) -> None:
        self.llm = Cohere(model="command-r-plus", api_key=api_key)
        self.tool_retriever = tool_retriever
        self.context = """
        Answer questions like you are Mark Cuban who has become a high school guidance counselor.
        Never say "I am Mark Cuban" or identify yourself though.
        Disuade the student if they are not qualified for what they are asking.
        """

    def reply(self, message: str, chat_history: List[ChatHistoryMessage]) -> str:
        # TODO: add tool retriever
        # worker = FunctionCallingAgentWorker(
        #     tools=[
        #         get_booking_state_tool,
        #         update_booking_tool,
        #         create_booking_tool,
        #         confirm_booking_tool,
        #     ],
        #     llm=llm,
        #     prefix_messages=prefix_messages,
        #     max_function_calls=10,
        #     allow_parallel_tool_calls=False,
        #     verbose=True,
        # )
        system_header = """
        You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

        ## Tools

        You have access to the following tools:
        {tool_desc}

        Here is some context to help you answer the question and plan:
        {context}

        If the task is appropriate for of the tools, use it.
        This may require breaking the task into subtasks and using different tools to complete each subtask.


        ## Output Format

        Please answer in the same language as the question and use the following format:

        ```
        Thought: The current language of the user is: (user's language). I need to use a tool to help me answer the question.
        Action: tool name (one of {tool_names}) if using a tool.
        Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})
        ```

        Please ALWAYS start with a Thought.

        Please use a valid JSON format for the Action Input. Do NOT do this {{'input': 'hello world', 'num_beams': 5}}.

        If this format is used, the user will respond in the following format:

        ```
        Observation: tool response
        ```

        Repeat the above unless the task can be completed without any of the tools provided.
        At that point, you MUST respond in the following format:

        ```
        Thought: I can answer without using any more tools. I'll use the user's language to answer
        Answer: [your answer here (In the same language as the user's question)]
        ```
        """
        # TODO: put everything in knowledge base with routers + prompt
        # TODO: query pipeline
        # TODO: check if no answer

        chat_engine = ReActAgent.from_tools(
            tool_retriever=self.tool_retriever,
            react_chat_formatter=ReActChatFormatter(
                system_header=system_header,
                context=self.context,
            ),
            llm=self.llm,
            chat_history=[
                ChatMessage.from_str(msg.text, role=str(msg.role.value).lower())
                for msg in chat_history
            ],
            # context=self.context,
            verbose=True,
        )

        return chat_engine.chat(message).response
