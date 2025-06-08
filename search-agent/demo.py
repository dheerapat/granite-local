"""
This file is AI generated. Reviewed by human
"""

from typing import List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel
import logging
from prompt import sum_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchEngineKeywords(BaseModel):
    """Model for extracting search keywords from user questions"""

    keywords: List[str]


class SearchResult(BaseModel):
    """Model for individual search results"""

    title: str
    url: str
    snippet: str


class AgenticSearchService:
    """
    A complete agentic search service that:
    1. Extracts keywords from user questions
    2. Performs web searches
    3. Summarizes results using LLM
    """

    def __init__(
        self,
        base_url: str = "http://192.168.110.142:1234/v1",
        api_key: str = "local",
        model: str = "granite-3.3-8b-instruct",
    ):
        """
        Initialize the search service

        Args:
            base_url: OpenAI API compatible base URL
            api_key: API key for the LLM service
            model: Model name to use
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def extract_keywords(self, user_question: str) -> List[str]:
        """
        Extract search keywords from user question using structured output

        Args:
            user_question: The user's original question

        Returns:
            List of keywords suitable for search engines
        """
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a search engine expert with unmatched skill in finding the right keywords.
                        From the user's question, extract 3-5 keywords that would be most effective for searching.
                        Focus on the core concepts, specific terms, and important context.
                        Avoid common words like 'what', 'how', 'the', etc.""",
                    },
                    {"role": "user", "content": user_question},
                ],
                response_format=SearchEngineKeywords,
            )

            keywords = response.choices[0].message.parsed
            if keywords is not None and keywords.keywords:
                logger.info(f"Extracted keywords: {keywords.keywords}")
                return keywords.keywords
            else:
                logger.warning("No keywords extracted, using fallback method")
                return self._fallback_keyword_extraction(user_question)

        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            # Fallback: simple keyword extraction
            return self._fallback_keyword_extraction(user_question)

    def _fallback_keyword_extraction(self, question: str) -> List[str]:
        """Fallback method for keyword extraction if LLM fails"""
        import re

        # Remove common question words and extract meaningful terms
        stop_words = {
            "what",
            "how",
            "when",
            "where",
            "why",
            "is",
            "are",
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "for",
            "of",
            "to",
            "in",
            "on",
            "at",
        }
        words = re.findall(r"\b\w+\b", question.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords[:5]  # Return top 5 keywords

    def search_web(
        self, keywords: List[str], num_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform web search using the extracted keywords

        Args:
            keywords: List of search keywords
            num_results: Number of results to return

        Returns:
            List of search results
        """
        # Combine keywords into search query
        search_query = " ".join(keywords)

        # Here you would integrate with your preferred search API
        # Options include:
        # 1. Google Custom Search API
        # 2. Bing Search API
        # 3. DuckDuckGo API
        # 4. Brave Search API
        # 5. SerpAPI

        # Example using a hypothetical search API
        try:
            # This is a placeholder - replace with your actual search implementation
            results = self._perform_search(search_query, num_results)
            logger.info(f"Found {len(results)} search results")
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return self._mock_search_results(search_query)

    def _perform_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Placeholder for actual search implementation
        Replace this with your preferred search API
        """
        # Example for Google Custom Search API:
        """
        api_key = "YOUR_GOOGLE_API_KEY"
        cx = "YOUR_SEARCH_ENGINE_ID"
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&num={num_results}"
        
        response = requests.get(url)
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            results.append({
                'title': item.get('title', ''),
                'url': item.get('link', ''),
                'snippet': item.get('snippet', '')
            })
        return results
        """

        # For now, return mock results
        return self._mock_search_results(query)

    def _mock_search_results(self, query: str) -> List[Dict[str, Any]]:
        """Mock search results for testing purposes"""
        return [
            {
                "title": f"Sample Result 1 for: {query}",
                "url": "https://example1.com",
                "snippet": "This is a sample search result snippet that would contain relevant information about the search query.",
            },
            {
                "title": f"Sample Result 2 for: {query}",
                "url": "https://example2.com",
                "snippet": "Another sample search result with different information that might be useful for answering the user question.",
            },
            {
                "title": f"Sample Result 3 for: {query}",
                "url": "https://example3.com",
                "snippet": "A third sample result providing additional context and information related to the search terms.",
            },
        ]

    def summarize_results(
        self, user_question: str, search_results: List[Dict[str, Any]]
    ) -> str:
        """
        Summarize search results to answer the user's question

        Args:
            user_question: Original user question
            search_results: List of search results

        Returns:
            Summarized answer based on search results
        """
        # Prepare context from search results
        context = self._prepare_context(search_results)

        # Create prompt for summarization
        prompt = sum_prompt.format(user_question=user_question, context=context)

        print(prompt)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=1000,
            )

            answer = (
                response.choices[0].message.content
                if response.choices and response.choices[0].message.content
                else "No answer generated"
            )
            logger.info("Successfully generated summary")
            return answer

        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"I apologize, but I encountered an error while processing the search results. The search found information about: {', '.join([r['title'] for r in search_results[:3]])}, but I couldn't generate a proper summary."

    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Prepare formatted context from search results"""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_part = f"""
Result {i}:
Title: {result.get('title', 'N/A')}
Source: {result.get('url', 'N/A')}
Content: {result.get('snippet', 'N/A')}
"""
            context_parts.append(context_part)

        return "\n".join(context_parts)

    def search_and_answer(self, user_question: str) -> Dict[str, Any]:
        """
        Complete search and answer pipeline

        Args:
            user_question: The user's question

        Returns:
            Dictionary containing the complete response
        """
        logger.info(f"Processing question: {user_question}")

        # Step 1: Extract keywords
        keywords = self.extract_keywords(user_question)

        # Step 2: Perform search
        search_results = self.search_web(keywords)

        # Step 3: Generate answer
        answer = self.summarize_results(user_question, search_results)

        return {
            "question": user_question,
            "keywords": keywords,
            "search_results": search_results,
            "answer": answer,
            "num_results": len(search_results),
        }


# Example usage and testing
def main():
    """Example usage of the AgenticSearchService"""

    # Initialize the service
    search_service = AgenticSearchService()

    # Test questions
    test_questions = [
        "What is the target blood pressure for healthy population?",
        "How does artificial intelligence work in modern cars?",
        "What are the latest developments in renewable energy?",
        "Best practices for Python web development in 2024?",
    ]

    print("=== Agentic Search Service Demo ===\n")

    for question in test_questions:
        print(f"Question: {question}")
        print("-" * 50)

        try:
            result = search_service.search_and_answer(question)

            print(f"Keywords: {', '.join(result['keywords'])}")
            print(f"Found {result['num_results']} results")
            print(f"\nAnswer:\n{result['answer']}")
            print("\n" + "=" * 80 + "\n")

        except Exception as e:
            print(f"Error processing question: {e}")
            print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
