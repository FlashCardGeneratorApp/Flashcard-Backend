from flask import Flask, request, jsonify
from utils import client, dbname, collection_name  # for Azure Cosmos DB
import json
from bson import ObjectId

app = Flask(__name__)

# Create a new note in our collection
@app.route('/notes/', methods=['POST'])
def create_new_note():
    try:
        note_data = request.get_json()
        if not note_data.user_id:
            return jsonify({"message": "Missing User ID"},500)
        for question in note_data.questions:
            question.user_id = note_data.user_id
            result = collection_name.insert_one(note_data)
        return jsonify({"message": "Note created successfully"})
    except Exception as e:
        return str(e), 500

# Get all notes
@app.route('/notes/', methods=['GET'])
def get_all_notes():
    try:
        notes_cursor = collection_name.find()
        notes = list(notes_cursor)
        return json.dumps(notes, default=str), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return str(e), 500

# Get note by ID
@app.route('/notes/<note_id>', methods=['GET'])
def get_note_by_id(note_id):
    try:
        note = collection_name.find_one({'_id': ObjectId(note_id)})
        if note:
            note['_id'] = str(note['_id'])
            return jsonify(note)
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return str(e), 500

# Update note
@app.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    try:
        update_data = request.get_json()
        collection_name.update_one({'_id': ObjectId(note_id)}, {'$set': update_data})
        return jsonify({'message': 'Note updated successfully'})
    except Exception as e:
        return str(e), 500

# Delete note
@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        result = collection_name.delete_one({'_id': ObjectId(note_id)})
        if result.deleted_count:
            return jsonify({'message': 'Note deleted successfully'})
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return str(e), 500

# Notes handler for both POST and GET requests to the same URL
@app.route('/notes/', methods=['POST', 'GET'])
def notes_handler():
    if request.method == 'POST':
        return create_new_note()
    elif request.method == 'GET':
        return get_all_notes()
    else:
        return jsonify({'error': 'Invalid HTTP method'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
