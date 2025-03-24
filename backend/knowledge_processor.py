import os
import json
import uuid
import datetime
from typing import List, Dict, Any, Optional

from ollama_service import OllamaService
from vector_store import VectorStore
from prompt_templates import PromptTemplates


class KnowledgeProcessor:
    def __init__(self):
        self.ollama = OllamaService()
        self.vector_store = VectorStore()
        self.prompt_templates = PromptTemplates()
    
    def add_knowledge(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add new knowledge to the Second Brain"""
        # Generate a unique ID
        document_id = str(uuid.uuid4())
        
        # Create embedding
        embedding = self.ollama.create_embeddings(content)
        
        # Add timestamp
        metadata["created_at"] = datetime.datetime.now().isoformat()
        
        # Extract entities if not provided
        if "entities" not in metadata:
            entities_prompt = self.prompt_templates.extract_entities_template(content)
            entities_json = self.ollama.generate_response(entities_prompt)
            try:
                entities = json.loads(entities_json)
                metadata["entities"] = json.dumps(entities)  # Convert to JSON string
            except:
                metadata["entities"] = "[]"  # Empty JSON array as string
        
        # Add to vector store
        self.vector_store.add_document(document_id, content, embedding, metadata)
        
        return document_id
    
    def query_knowledge(self, query: str, filter_criteria: Optional[Dict[str, Any]] = None, n_results: int = 5):
        """Query the Second Brain"""
        # Create query embedding
        query_embedding = self.ollama.create_embeddings(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, n_results, filter_criteria)
        
        # If we have results, use them as context
        if results["documents"] and results["documents"][0]:
            context = "\n\n".join(results["documents"][0])
            prompt = self.prompt_templates.query_template(query, context)
        else:
            prompt = self.prompt_templates.query_template(query)
        
        # Generate response
        response = self.ollama.generate_response(prompt)
        
        return {
            "response": response,
            "sources": [
                {"id": doc_id, "text": doc_text[:200] + "...", "metadata": doc_metadata}
                for doc_id, doc_text, doc_metadata in zip(
                    results["ids"][0], results["documents"][0], results["metadatas"][0]
                )
            ] if results["documents"] and results["documents"][0] else []
        }
    def remove_knowledge(self, document_id: str) -> bool:
        """Remove knowledge from the Second Brain"""
        try:
        # Remove from vector store
            self.vector_store.delete_document(document_id)
            return True
        except Exception as e:
            print(f"Error removing knowledge: {e}")
            raise e
    def get_all_knowledge(self):
        """Get all knowledge from the Second Brain"""
        try:
            # Get all documents from the vector store
            results = self.vector_store.get_all_documents()
            
            # Format the results for the frontend
            knowledge_list = []
            for i in range(len(results["ids"])):
                knowledge_list.append({
                    "id": results["ids"][i],
                    "content": results["documents"][i],
                    "metadata": results["metadatas"][i]
                })
                
            return knowledge_list
        except Exception as e:
            print(f"Error getting all knowledge: {e}")
            raise e

    def suggest_connections(self, content: str):
        """Suggest connections to existing knowledge"""
        # Get some existing entities
        # In a real implementation, you would have a more sophisticated way to get relevant entities
        results = self.vector_store.collection.get(limit=10)
        existing_entities = []
        
        for metadata in results["metadatas"]:
            if "entities" in metadata:
                try:
                    entities = json.loads(metadata["entities"])
                    existing_entities.extend(entities)
                except:
                    pass
        
        # If we have entities, suggest connections
        if existing_entities:
            prompt = self.prompt_templates.suggest_connections_template(content, existing_entities)
            suggestions_json = self.ollama.generate_response(prompt)
            try:
                return json.loads(suggestions_json)
            except:
                return []
        
        return []


# Test the knowledge processor
if __name__ == "__main__":
    processor = KnowledgeProcessor()
    
    # Add some test knowledge
    test_content = """
    The Second Brain is a methodology for saving and systematically reminding us of the ideas, inspirations, insights, and connections we've gained through our experience. It's a methodology for knowledge management and a set of habits for leveraging your knowledge.
    
    The Second Brain methodology consists of four steps, known as the CODE method:
    1. Capture: Save ideas and insights you come across
    2. Organize: Sort information into logical categories
    3. Distill: Find the essence of your notes
    4. Express: Share your ideas with others
    """
    
    test_metadata = {
        "title": "Second Brain Methodology",
        "tags": ",".join(["PKM", "productivity", "CODE method"]),
        "source": "Test"
    }
    
    doc_id = processor.add_knowledge(test_content, test_metadata)
    print(f"Added document with ID: {doc_id}")
    
    # Test querying
    query = "What is the CODE method in Second Brain?"
    result = processor.query_knowledge(query)
    
    print("\nQuery:", query)
    print("Response:", result["response"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source['metadata']['title']}: {source['text']}")
    
    # Test suggesting connections
    new_content = "Personal Knowledge Management (PKM) systems help individuals organize and retrieve information effectively."
    connections = processor.suggest_connections(new_content)
    
    print("\nSuggested connections for new content:")
    for connection in connections:
        print(f"- {connection['entity']}: {connection['reason']}")