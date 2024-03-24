import pyodbc
from flask import Flask, request, jsonify, render_template, session, redirect
from chat import get_response
from flask_cors import CORS  # Import CORS from flask_cors module

app = Flask(__name__)
CORS(app)  # Apply CORS to your Flask app
app.secret_key = "siri"

feedback_requested = False  # Initialize feedback_requested variable
feedback_text = ""  # Initialize feedback_text variable

@app.get("/")
def index_get():
    return render_template("base.html")

@app.get("/maps")
def map():
    return render_template("map.html")

# Add a new route to handle review submission
@app.route("/submit_review", methods=["POST"])
def submit_review():
    try:
        if "user_info" in session:
            # Extract user information from the session
            user_info = session["user_info"]
            name = user_info.get("name", "")
            email = user_info.get("email", "")
            image = user_info.get("image", "")

            # Extract review text from the request
            review_text = request.json.get("review_text", "")

            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=NEETHILA-PC\\SQLEXPRESS;DATABASE=chatbot;UID=knkchat;PWD=knk123')
            cursor = conn.cursor()

            # Insert the review into the database
            # Assuming you have a table named "reviews" with columns: name, email, image, review_text
            cursor.execute("INSERT INTO reviews (name, email, image, review_text) VALUES (?, ?, ?, ?)",
                           (name, email, image, review_text))
            conn.commit()

            # Return success response
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "User not logged in"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.route("/review")
def review():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=NEETHILA-PC\\SQLEXPRESS;DATABASE=chatbot;UID=knkchat;PWD=knk123')
        cursor = conn.cursor()
        # Fetch only 5 reviews from the database initially
        cursor.execute("SELECT TOP 5 name, image, review_text FROM reviews ORDER BY review_id DESC")
        initial_reviews = cursor.fetchall()

        # Pass initial reviews data to the template for rendering
        return render_template("review.html", initial_reviews=initial_reviews)

    except Exception as e:
        return str(e)


@app.route("/all_reviews")
def all_reviews():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=NEETHILA-PC\\SQLEXPRESS;DATABASE=chatbot;UID=knkchat;PWD=knk123')
        cursor = conn.cursor()
        # Fetch all reviews from the database
        cursor.execute("SELECT name, image, review_text FROM reviews ORDER BY review_id DESC")
        reviews = cursor.fetchall()

        # Convert reviews to a list of dictionaries for JSON response
        reviews_list = [{'name': review[0], 'image': review[1], 'review_text': review[2]} for review in reviews]

        # Return reviews data as JSON
        return jsonify({'reviews': reviews_list})

    except Exception as e:
        return str(e)




def store_feedback(feedback_text):
    try:
        print("Feedback:", feedback_text)
        # Connect to the database
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=NEETHILA-PC\\SQLEXPRESS;DATABASE=chatbot;UID=knkchat;PWD=knk123')

        # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};NEETHILA-PC\SQLEXPRESS\\SQLEXPRESS;DATABASE=chatbot;UID=knkchat;PWD=knk123')

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

@app.route("/search_reviews", methods=["GET"])
def search_reviews():
    try:
        keyword = request.args.get("keyword")  # Get the keyword from the query parameters
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=NEETHILA-PC\\SQLEXPRESS;DATABASE=chatbot;UID=knkchat;PWD=knk123')
        cursor = conn.cursor()

        # Fetch reviews from the database that contain the keyword in their review_text
        cursor.execute("SELECT name, image, review_text FROM reviews WHERE review_text LIKE ?", ('%'+keyword+'%',))
        
        searched_reviews = cursor.fetchall()

        # Convert searched reviews to a list of dictionaries for JSON response
        reviews_list = [{'name': review[0], 'image': review[1], 'review_text': review[2]} for review in searched_reviews]

        # Return searched reviews data as JSON
        return jsonify({'reviews': reviews_list})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback_text = request.form.get("feedbackText")
    store_feedback(feedback_text)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    # Run the main Flask app (app.py)
    app.run(debug=True)