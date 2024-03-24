import pyodbc
from flask import Flask, request, jsonify, render_template
from chat import get_response

app = Flask(__name__)

feedback_requested = False  # Initialize feedback_requested variable
feedback_text = ""  # Initialize feedback_text variable

@app.get("/")
def index_get():
    return render_template("base.html")

def store_feedback(feedback_text):
    try:
        print("Feedback:", feedback_text)
        # Connect to the database
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-K653L1C\SQLEXPRESS;DATABASE=chatbot;UID=siriahk;PWD=123')

        cursor = conn.cursor()
        
        # Insert the feedback into the table
        cursor.execute("INSERT INTO review1_table (review) VALUES (?)", (feedback_text,))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        print("Feedback successfully inserted into the database.")
    except Exception as e:
        print("Error:", e)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data["message"]
    
    global feedback_requested, feedback_text  # Access the global variables
    
    if feedback_requested:
        # If the user is responding to the feedback request
        store_feedback(text)  # Pass the feedback_text to the store_feedback function
        feedback_requested = False  # Reset the feedback_requested flag
        return jsonify({"answer": "Thank you for your feedback!"})

    response = get_response(text)
    print(text)

    # Ensure response is a string
    if isinstance(response, tuple):
        response = response[0]  # Get the first element of the tuple

    if response.startswith("Goodbye! Before you go, could you please provide some feedback?"):
        # If the response is asking for feedback, set the feedback_requested flag
        feedback_requested = True
        return jsonify({"answer": response})
    else:
        # For all other responses, return the response to the user interface
        return jsonify({"answer": response})


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback_text = request.form.get("feedbackText")
    store_feedback(feedback_text)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)
