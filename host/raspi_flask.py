from flask import Flask, request, send_from_directory, render_template_string, send_file
import os
from flask_mysqldb import MySQL
from text_preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__, static_folder='static')

# Configuration for MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testwhizzy'

# Initialize MySQL
mysql = MySQL(app)

# Global variables to store updated TF-IDF vectors and vectorizer
updated_vectorizer = None
updated_question_vectors = None

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_file(os.path.join('uploads', filename))

@app.route('/raspi_fetch')
def raspi_fetch():
    user_input = request.args.get('user_input')
    if user_input:
        cur = mysql.connection.cursor()
        cur.execute("SELECT question, answer, file_name FROM entries")
        faqs = cur.fetchall()
        questions = [faq[0] for faq in faqs]
        answers = [faq[1] for faq in faqs]
        file_names = [faq[2] for faq in faqs]

        # Preprocess the questions
        preprocessed_questions = [preprocess_text(question) for question in questions]

        # Use the updated TF-IDF vectors if available, else create new ones
        if updated_vectorizer is not None and updated_question_vectors is not None:
            vectorizer = updated_vectorizer
            question_vectors = updated_question_vectors
        else:
            vectorizer = TfidfVectorizer()
            question_vectors = vectorizer.fit_transform(preprocessed_questions)

        # Preprocess the user's query
        preprocessed_query = preprocess_text(user_input)

        # Calculate the similarity between the user's query and the database questions
        user_query_vector = vectorizer.transform([preprocessed_query])
        similarities = cosine_similarity(user_query_vector, question_vectors)

        # Get the index of the most similar question
        most_similar_index = np.argmax(similarities)

        # Set a similarity threshold
        similarity_threshold = 0.7

        if similarities[0][most_similar_index] > similarity_threshold:
            best_match_answer = answers[most_similar_index]
            best_match_file_name = file_names[most_similar_index]

            if best_match_file_name:
                # Render a template with both the image and the text answer
                template = """
                    <div>
                        <p>{{ answer }}</p>
                        <img src="{{ url_for('serve_uploaded_file', filename=file_name) }}" alt="Image">
                    </div>
                """
                return render_template_string(template, answer=best_match_answer, file_name=best_match_file_name)
            else:
                return best_match_answer
        else:
            return "Sorry, I couldn't find an answer for that question."
    else:
        return "No user input provided."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)