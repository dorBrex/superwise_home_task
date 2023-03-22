from typing import Dict

from flask import Flask, request, jsonify
from parse_and_recall import main_functionality

"""
    Flask server logic
"""

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


def build_response_for_client(version_id: int, segment_id: int = None) -> Dict:
    generic_resp = f'success calculating the recall for version {version_id}'
    if segment_id:
        expanded_resp = generic_resp + f"and segment {segment_id}"
        return {'message': expanded_resp}
    return {'message': generic_resp}


# /v1/recall/version/{version_id}?segment_id={segment_id}
# @app.route('/v1/recall/version/<version_id>', defaults={'segment_id': None})
# @app.route('/v1/recall/version/<version_id>/<segment_id>', methods=['GET'])
@app.route('/v1/recall/version', methods=['GET'])
def v1():
    version_id = int(request.args.get('version_id'))
    segment_id = request.args.get('segment_id', None)
    if segment_id:
        segment_id = int(segment_id)

    # Main Logic: connect this logic to ->  main parsing request ->
    # db retrival data ->  parse data from db and calculate recall ->
    # send the result of the recall to kafka -> send a response back to the client

    recall_status = main_functionality(version_id=version_id, segment_id=segment_id)
    if recall_status:
        resp = build_response_for_client(version_id=version_id, segment_id=segment_id)
        return jsonify(resp)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
