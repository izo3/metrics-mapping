from flask import Flask, jsonify, request
import re
import json

app = Flask(__name__)

# Load the contents of metrics file into a variable
with open('metrics.json', 'r') as file:
    metrics_data = json.load(file)['data']

def filter_metrics(match):
    if not match:
        return metrics_data

    match_pattern = re.search(r'{__name__=~"([^"]+)"}', match)
    if match_pattern:
        pattern = match_pattern.group(1)
        regex = re.compile(pattern)
        return [metric for metric in metrics_data if regex.match(metric)]
    
    return metrics_data

# Handle the incorrect paths
@app.route('/api/v1/label/__name__/values', methods=['GET'])
@app.route('/values/label/__name__/values', methods=['GET']) 
def get_metrics():
    match = request.args.get('match[]')
    filtered_metrics = filter_metrics(match)
    return jsonify({"status": "success", "data": filtered_metrics})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9090)

