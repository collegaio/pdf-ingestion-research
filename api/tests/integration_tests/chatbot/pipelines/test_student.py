import pytest
from langchain_core.messages import HumanMessage, AIMessage

from chatbot.pipelines.student import pipeline


@pytest.mark.asyncio
async def test_extract_student_info():
    # Use the Runnable
    final_state = await pipeline.ainvoke(
        {
            "messages": [
                AIMessage(
                    content="Hi! it looks like you are wondering where you should go to school. Any idea what you want to want to study?"
                ),
                HumanMessage(content="hey yeah I'm thinking about going into nursing."),
                AIMessage(
                    content="Any idea where you'd like to go to to school? What schools have you looked at already?"
                ),
                HumanMessage(content="Hmm maybe on the east coast?"),
            ]
        },
        # config={"configurable": {"thread_id": 42}}
    )

    print("final state:", final_state)
    assert final_state["student_profile"] is not None
    assert "the east coast" in [
        pref.lower() for pref in final_state["student_profile"].geographic_preferences
    ]
