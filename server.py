from flask import Flask, render_template, request, jsonify
from causal_graph import process_causal
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recieve_property", methods = ["POST"])
def receive_data():
    print(request.get_json())
    return "OK"
@app.route("/recieve_causal", methods=["POST"])
def receive_causal_data():
    content = request.get_json()
    print(content)
    process_causal(content)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
