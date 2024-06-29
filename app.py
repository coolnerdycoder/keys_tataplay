from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load keys from keys.json file
def load_keys():
    with open('keys.json', 'r') as file:
        return json.load(file)

@app.route('/keys/<channel_id>', methods=['GET'])
def get_keys_by_channel_id(channel_id):
    keys_data = load_keys()
    for item in keys_data:
        if item['channel_id'] == channel_id:
            response_data = {
                "keys": item['keys'],
                "type": "temporary"
            }
            return jsonify(response_data)
    return jsonify({"error": "Keys not found for this channel_id"}), 404

if __name__ == '__main__':
    app.run()
