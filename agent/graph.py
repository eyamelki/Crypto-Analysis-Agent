from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools.crypto_list import crypto_list_tool
from tools.crypto_data import crypto_data_tool
from tools.crypto_news import crypto_news_tool

from agent.prompts import SYSTEM_PROMPT


# 1. Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0
)


# 2. Register the tools
tools = [
    crypto_list_tool,
    crypto_data_tool,
    crypto_news_tool
]


# 3. Create the ReAct agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)


def run_agent(question: str) -> str:
    """
    Run the cryptocurrency analysis agent.

    Args:
        question: User's question.

    Returns:
        The agent's final response.
    """
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    return result["messages"][-1].content