from flask import Flask, request, jsonify
from utils import client, dbname, collection_name  # for Azure Cosmos DB
import json
from  questionGenerator import generate_questions
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
        result = collection_name.insert_many(note_data)
        return jsonify({"message": "Notes created successfully"})
    except Exception as e:
        return str(e), 500

# Get all notes associated with a user
@app.route('/notes/<user_id>', methods=['GET'])
def get_all_notes(user_id):
    try:
        notes_cursor = collection_name.find()
        notes = list(notes_cursor)
        return json.dumps(notes, default=str), 200, {'Content-Type': 'application/json'}
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


@app.route('/notes/generate/<topic>', methods=['GET'])
def question_helper(topic):
    return generate_questions(topic)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
