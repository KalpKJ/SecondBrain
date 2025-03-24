import chromadb
import os
import json
from typing import List, Dict, Any, Optional

class VectorStore:
    def __init__(self, persist_directory="C:/SecondBrain/data/chroma_db"):
        # Ensure the directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize the persistent client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="second_brain",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_document(self, document_id: str, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """Add a document to the vector store"""
        self.collection.add(
            ids=[document_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )
    
    def search(self, query_embedding: List[float], n_results: int = 5, filter_criteria: Optional[Dict[str, Any]] = None):
        """Search for similar documents"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_criteria
        )
        
        return results
    
    def delete_document(self, document_id: str):
        """Delete a document from the vector store"""
        try:
            # Get the document's position in the collection
            response = self.collection.get(where={"document_id": document_id})
            if "ids" in response and len(response["ids"]) > 0:
                # Delete the document by ID
                self.collection.delete(ids=response["ids"])
            else:
                # If not found by document_id, try direct deletion
                self.collection.delete(ids=[document_id])
        except Exception as e:
            print(f"Error deleting document: {e}")
            raise e
    
    def update_document(self, document_id: str, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """Update a document in the vector store"""
        self.delete_document(document_id)
        self.add_document(document_id, text, embedding, metadata)
    
    def get_document(self, document_id: str):
        """Get a document by ID"""
        results = self.collection.get(ids=[document_id])
        if results["ids"]:
            return {
                "id": results["ids"][0],
                "text": results["documents"][0],
                "metadata": results["metadatas"][0]
            }
        return None
    
    def get_all_documents(self):
        """Get all documents from the vector store"""
        try:
            return self.collection.get(include=["documents", "metadatas"])
        except Exception as e:
            print(f"Error getting all documents: {e}")
            raise e

# Test the vector store
if __name__ == "__main__": 
    from ollama_service import OllamaService
    
    # Initialize services
    ollama = OllamaService()
    vector_store = VectorStore()
    
    # Create a test document
    test_text = "The Second Brain is a methodology for saving and systematically reminding us of the ideas, inspirations, insights, and connections we've gained through our experience."
    test_embedding = ollama.create_embeddings(test_text)
   # Convert the list of tags to a comma-separated string
    test_metadata = {
    "title": "Second Brain Concept",
    "tags": ",".join(["PKM", "productivity", "knowledge management"]),
    "source": "Test",
    "created_at": "2025-03-22"
    }
    
    # Add to vector store
    vector_store.add_document("test-doc-1", test_text, test_embedding, test_metadata)
    print("Document added to vector store")
    
    # Test search
    query = "What is a second brain?"
    query_embedding = ollama.create_embeddings(query)
    results = vector_store.search(query_embedding)
    
    print("\nSearch Results:")
    for i, (doc_id, doc_text, doc_metadata) in enumerate(zip(
        results["ids"][0], results["documents"][0], results["metadatas"][0]
    )):
        print(f"Result {i+1}:")
        print(f"ID: {doc_id}")
        print(f"Text: {doc_text}")
        print(f"Metadata: {json.dumps(doc_metadata, indent=2)}")
        print()
