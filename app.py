from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from flask_cors module
import json
from collections import OrderedDict

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Load keys from keys.json file
def load_keys():
    with open('keys.json', 'r') as file:
        return json.load(file)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dict):
            return OrderedDict(
                sorted(obj.items(), key=lambda t: ['kty', 'k', 'kid'].index(t[0]))
            )
        return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/keys/<channel_id>', methods=['GET'])
def get_keys_by_channel_id(channel_id):
    keys_data = load_keys()
    for item in keys_data:
        if item['channel_id'] == channel_id:
            try:
                # Transform keys data into desired format
                transformed_keys = {
                    "keys": item["keys"],
                    "type": "temporary"
                }
                return jsonify(transformed_keys)
            except KeyError as e:
                return jsonify({"error": f"Invalid keys format in keys.json: Missing key field ({str(e)})"}), 500  # Server error

    return jsonify({"error": "Keys not found for this channel_id"}), 404

if __name__ == '__main__':
    app.run()
