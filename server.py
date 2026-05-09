from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/send', methods=['POST'])
def send():

    data = request.json

    messages.append(data)

    return jsonify({
        "status": "Message Stored"
    })

@app.route('/receive/<username>', methods=['GET'])
def receive(username):

    for msg in messages:

        if msg["to"] == username:

            messages.remove(msg)

            return jsonify(msg)

    return jsonify({
        "message": None
    })

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=5000
    )