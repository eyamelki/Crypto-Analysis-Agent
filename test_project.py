
from agent.graph import run_agent


def test_crypto_list():
    print("\n" + "=" * 60)
    print("TEST 1: CRYPTO LIST TOOL")
    print("=" * 60)

    response = run_agent(
        "Give me 5 available cryptocurrencies with their names and symbols.",
        thread_id="test-list"
    )

    print(response)


def test_crypto_data():
    print("\n" + "=" * 60)
    print("TEST 2: CRYPTO DATA TOOL")
    print("=" * 60)

    response = run_agent(
        "Give me the latest available market data for Bitcoin (BTC). "
        "Present the results as bullet points.",
        thread_id="test-data"
    )

    print(response)


def test_crypto_news():
    print("\n" + "=" * 60)
    print("TEST 3: CRYPTO NEWS TOOL")
    print("=" * 60)

    response = run_agent(
        "Find 5 recent news articles about Ethereum. "
        "Include each article's title, source, publication date and URL.",
        thread_id="test-news"
    )

    print(response)


def test_multi_tool_analysis():
    print("\n" + "=" * 60)
    print("TEST 4: MULTI-TOOL ANALYSIS")
    print("=" * 60)

    response = run_agent(
        "Compare Bitcoin (BTC) and Ethereum (ETH) using their latest "
        "available market data and recent news. "
        "Retrieve market data for both cryptocurrencies and recent "
        "news about each one. Explain their short-term market situation, "
        "compare their performance and identify potential risks. "
        "Clearly distinguish API facts from your analysis. "
        "Do not invent missing data.",
        thread_id="test-analysis"
    )

    print(response)


if __name__ == "__main__":

    print("\n===== CRYPTO ANALYSIS AGENT - PROJECT TESTS =====")

    test_crypto_list()

    test_crypto_data()

    test_crypto_news()

    test_multi_tool_analysis()

    print("\n===== ALL TESTS EXECUTED =====")
