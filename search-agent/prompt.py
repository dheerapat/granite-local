sum_prompt = """
Based on the following search results, please provide a comprehensive and accurate answer to the user's question.

User Question: {user_question}
        
Search Results:
{context}
        
Instructions:
1. Provide a direct and informative answer to the user's question
2. Use information from the search results to support your answer
3. If the search results don't contain enough information, mention what information is missing
4. Be concise but thorough
5. Include relevant details and examples when available
6. If there are conflicting information in the results, mention the different perspectives

Answer:
"""
