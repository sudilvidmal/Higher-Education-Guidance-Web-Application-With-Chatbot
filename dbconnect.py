import pyodbc


def insert_user_info(name, email,image):
    # Connect to the database
    connection_string = "DRIVER={SQL Server};SERVER=DESKTOP-3OVJ75D\SQLEXPRESS;DATABASE=chatbot;UID=siriahk;PWD=123"
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        # Insert user information into the user_table
        cursor.execute("INSERT INTO user_table (Name, Email,image) VALUES (?, ?,?)", (name, email,image))
        conn.commit()
        print("User information inserted into the database successfully!")
    except pyodbc.Error as e:
        print(f"Error inserting user information into the database: {e}")
    finally:
        cursor.close()
        conn.close()
        
