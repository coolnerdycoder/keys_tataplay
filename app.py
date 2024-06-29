from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load keys from keys.json file
def load_keys():
    with open('keys.json', 'r') as file:
        return json.load(file)

@app.route('/keys/<key_id>', methods=['GET'])
def get_key(key_id):
    keys = load_keys()
    if key_id in keys:
        return jsonify({key_id: keys[key_id]})
    else:
        return jsonify({"error": "Key not found"}), 404

if __name__ == '__main__':
    app.run()