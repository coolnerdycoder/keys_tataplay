from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from flask_cors module
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Load keys from keys.json file
def load_keys():
    with open('keys.json', 'r') as file:
        return json.load(file)

@app.route('/keys/<channel_id>', methods=['GET'])
def get_keys_by_channel_id(channel_id):
    keys_data = load_keys()
    for item in keys_data:
        if item['channel_id'] == channel_id:
            try:
                # Transform keys data into desired format
                transformed_keys = {
                    "keys": [{"kty": key["kty"], "k": key["k"], "kid": key["kid"]} for key in item["keys"]],
                    "type": "temporary"
                }
                return jsonify(transformed_keys)
            except KeyError as e:
                return jsonify({"error": f"Invalid keys format in keys.json: Missing key field ({str(e)})"}), 500  # Server error

    return jsonify({"error": "Keys not found for this channel_id"}), 404

if __name__ == '__main__':
    app.run()
