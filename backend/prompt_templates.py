class PromptTemplates:
    @staticmethod
    def query_template(query, context=None):
        """Template for querying the Second Brain"""
        if context:
            return f"""You are a helpful assistant that helps users access their Second Brain.
            
Based on the following information from the user's Second Brain:
{context}

Answer the user's question:
{query}

If the information provided doesn't answer the question, say so clearly.
"""
        else:
            return f"""You are a helpful assistant that helps users access their Second Brain.
            
The user has asked: {query}

If you don't have specific information from their Second Brain to answer this, 
provide a helpful general response and suggest they might want to add this information to their Second Brain.
"""

    @staticmethod
    def summarize_template(content):
        """Template for summarizing content"""
        return f"""Summarize the following content in a concise way that captures the main points:

{content}

Provide the summary in a single paragraph.
"""

    @staticmethod
    def extract_entities_template(content):
        """Template for extracting entities from content"""
        return f"""Extract the key entities (people, organizations, concepts, places, etc.) from the following content:

{content}

Return the entities as a JSON array of objects with 'entity' and 'type' fields.
Example: [{{"entity": "Albert Einstein", "type": "person"}}, {{"entity": "Theory of Relativity", "type": "concept"}}]
"""

    @staticmethod
    def suggest_connections_template(content, existing_entities):
        """Template for suggesting connections between content"""
        entities_str = ", ".join([e["entity"] for e in existing_entities[:10]])
        return f"""Based on the following content:

{content}

Suggest connections to these existing entities in the user's Second Brain: {entities_str}

Return the suggestions as a JSON array of objects with 'entity' and 'reason' fields.
Example: [{{"entity": "Albert Einstein", "reason": "Both discuss physics concepts"}}, {{"entity": "Quantum Mechanics", "reason": "Related scientific field"}}]
"""
