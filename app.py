from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data["message"]
    
    response = get_response(text)
    message = {"answer": response}  # Fixed the dictionary syntax
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
