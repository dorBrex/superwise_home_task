from flask import Flask, request, jsonify

"""
    Flask server logic
"""

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


success_referring_kafka = None


def build_response_for_client(version_id: int, segment_id: int = None):
    generic_resp = f'success calculating the recall for version {version_id}'
    if segment_id:
        expanded_resp = generic_resp + f"and segment {segment_id}"
        return {message: expanded_resp}
    return {message: generic_resp}


# /v1/recall/version/{version_id}?segment_id={segment_id}
@app.route('/v1/recall/version/<version_id>', defaults={'segment_id': None})
@app.route('/v1/recall/version/<version_id>/<segment_id>', methods=['GET'])
def get_data():
    version_id = request.args.get('version_id')  # must receive it.
    # ToDo: connect this logic to ->main parsing request -> db retrival data -> parse data from db and calculate recall
    #  -> send the result of the recall to kafka -> send a response back to the client

    try:
        segment_id = request.args.get('segment_id')  # optionally recieve it.
    except Exception as e:
        pass  # no segment id recieved

    if success_referring_kafka:
        resp = build_response_for_client
        return resp


if __name__ == '__main__':
    app.run(port=8080, debug=True)
