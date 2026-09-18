import os
from typing import List
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


class WebSearcher:

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY environment variable is not set."
            )

        self.client = TavilyClient(
            api_key=api_key
        )

    def search(self, query: str) -> List[str]:

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=self.max_results
        )

        urls = [
            result["url"]
            for result in response["results"]
        ]

        print("\nFound URLs:")

        for url in urls:
            print(f"- {url}")

        return urls
