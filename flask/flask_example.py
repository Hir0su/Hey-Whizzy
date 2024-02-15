from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("your_database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create a new FAQ
@app.route("/faq", methods=["POST"])
def create_faq():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

    return jsonify({"message": "FAQ created successfully"}), 201

# Update an existing FAQ
@app.route("/faq/<int:faq_id>", methods=["PUT"])
def update_faq(faq_id):
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE faqs SET question = ?, answer = ? WHERE id = ?", (question, answer, faq_id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"FAQ with ID {faq_id} updated successfully"})

# Delete an existing FAQ
@app.route("/faq/<int:faq_id>", methods=["DELETE"])
def delete_faq(faq_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"FAQ with ID {faq_id} deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
