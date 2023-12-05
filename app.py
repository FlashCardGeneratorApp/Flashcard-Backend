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
            question = note_data["user_id"]
        result = collection_name.insert_many(note_data.questions)
        return jsonify({"message": "Notes created successfully"})
    except Exception as e:
        return str(e), 500
    
# Get all notes using user_id
@app.route('/notes/<user_id>', methods=['GET'])
def get_all_notes_by_user_id(user_id):
#     '''TODO
# Respond with a JSON = 
# {
#     questions:
#     [
#         {
        # id: 1,
#       question: "What dynasty did Qin Shi Huang Found?",
#       options: ["Qing Dynasty", "Han Dynasty", "Song Dynasty", "Zhou Dynasty"],
#       answer: "Han Dynasty",
#     },
#     {
        # id:2
#       question: "Who orchestrated the Long March?",
#       options: ["Bo Gu", "Mao Ze Dong", "Chiang Kai Shek", "Zhou Enlai"],
#       answer: "Chiang Kai Shek",
#     },
#     ...
#     ]
    
# }
# '''
    try:
        notes_cursor = collection_name.find({'user_id': user_id })
        notes = list(notes_cursor)
        for note in notes:
            note['user_id'] = str(note['user_id'])
        return json.dumps(notes, default=str), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return str(e), 500


# Delete note
@app.route('/notes', methods=['DELETE'])
def delete_note():
    # {questions_id: [id,id,id]} for
    try:
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
    # for question in generated_questions:
    #     if 'Question' not in question or 'Options' not in question or 'Answer' not in question:
    #         return f'Try again', 400
    # '''
    # {questions: [
    #     {
    #         question:
    #         options:
    #         answer:
    #     },
    #     ...
    # ]}
    # '''
     
    return jsonify({"questions": generated_questions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
