
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools.crypto_list import crypto_list_tool
from tools.crypto_data import crypto_data_tool
from tools.crypto_news import crypto_news_tool

from agent.prompts import SYSTEM_PROMPT


# 1. Load environment variables
load_dotenv()

# 2. Check Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Please check your .env file."
    )


# 3. Initialize the Groq LLM
llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key,
    temperature=0
)


# 4. Register the tools
tools = [
    crypto_list_tool,
    crypto_data_tool,
    crypto_news_tool
]


# 5. Create the ReAct agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)


# 6. Run the agent
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
