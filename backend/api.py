from flask import Flask, request, jsonify
from knowledge_processor import KnowledgeProcessor
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
processor = KnowledgeProcessor()

@app.route('/api/knowledge', methods=['POST'])
def add_knowledge():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    content = data['content']
    metadata = data.get('metadata', {})
    
    document_id = processor.add_knowledge(content, metadata)
    
    return jsonify({"id": document_id, "status": "success"})

@app.route('/api/knowledge/<document_id>', methods=['DELETE'])
def remove_knowledge(document_id):
    try:
        processor.remove_knowledge(document_id)
        return jsonify({"status": "success", "message": "Knowledge removed successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/api/knowledge', methods=['GET'])
def get_all_knowledge():
    try:
        # Retrieve all documents from the vector store
        results = processor.get_all_knowledge()
        return jsonify(results)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query_knowledge():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400
    
    query = data['query']
    filter_criteria = data.get('filter', None)
    n_results = data.get('n_results', 5)
    
    result = processor.query_knowledge(query, filter_criteria, n_results)
    
    return jsonify(result)

@app.route('/api/suggest', methods=['POST'])
def suggest_connections():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    content = data['content']
    
    suggestions = processor.suggest_connections(content)
    
    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
