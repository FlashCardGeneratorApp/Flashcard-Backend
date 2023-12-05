from flask import Flask, request, jsonify
from utils import client, dbname, collection_name  # for Azure Cosmos DB
import json
from  questionGenerator import generate_questions
from bson import ObjectId

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Home Page"})

# Create a new note in our collection
@app.route('/notes/', methods=['POST'])
def create_new_note():
    # '''
    # Recieves: 
    # {
    #     userid: string,
    #     questions: [
    #         {question: "WHat is htis...?",
    #         options: ["a", "b", "c","D"],
    #         answer: ["a"],
    #         userid : "asijodasjdios"
    #         }
    #     ]
    # }
    # '''
    try:
        note_data = request.json
        if not note_data["user_id"]:
            return jsonify({"message": "Missing User ID"},500)
        for question in note_data["questions"]:
            question['user_id'] = note_data["user_id"]
        collection_name.insert_many(note_data["questions"])
        return jsonify({"message": "Notes created successfully"})
    except Exception as e:
        return str(e), 500
    
# Get all notes using user_id
@app.route('/notes/<user_id>', methods=['GET'])
def get_all_notes_by_user_id(user_id):
    questions = []
    try:
        notes_cursor = collection_name.find({'user_id': user_id})
        for note in notes_cursor:
            print(note["_id"])
            note["_id"] = str(note["_id"])
            questions.append(note)
        
        return {"questions": questions}
    
    except Exception as e:
        return str(e), 500


# Delete note
@app.route('/notes', methods=['DELETE'])
def delete_note():
    notes = request.json
    try:
        for note_id in notes["question_id"]:
            result = collection_name.delete_one({'_id': ObjectId(note_id)})
            if result.deleted_count:
                return jsonify({'message': 'Note deleted successfully'})
            else:
                return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return str(e), 500

@app.route('/notes/generate/<topic>', methods=['GET'])
def question__generator(topic):
    generated_questions = generate_questions(topic)
    return jsonify({"questions": json.loads(generated_questions)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
