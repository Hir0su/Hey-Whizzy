from flask import Flask, request ,render_template, jsonify, send_from_directory
import os
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='static')

# Configuration for MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testwhizzy'

# Initialize MySQL
mysql = MySQL(app)

# Directory for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for serving static files
app.static_folder = 'static'

# Route for accessing uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Insert file path into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO files (file_path, files_name) VALUES (%s, %s)", (filepath, filename))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'message': 'No file provided'}), 400

# Route for adding FAQs
@app.route('/add_faq', methods=['POST'])
def add_faq():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        if question and answer:
            # Insert FAQ into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO faqs (question, answer) VALUES (%s, %s)", (question, answer))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'FAQ added successfully'}), 200
        else:
            return jsonify({'message': 'No question or answer provided'}), 400
        
# Route to fetch files/images
@app.route('/fetch_data')
def fetch_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_path FROM files")
    files = cur.fetchall()
    cur.close()
    return render_template('readFile.html', files=files)

# Route to fetch FAQ/Answers
@app.route('/fetch_faqs')
def fetch_faqs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM faqs")
    faqs = cur.fetchall()
    cur.close()
    return render_template('readFaqText.html', faqs=faqs)

# Route to fetch the FAQs/Answers for editFaq.html
@app.route('/fetch_archive_faqs')
def fetch_archive_faqs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM faqs")
    faqs = cur.fetchall()
    return render_template('editFaq.html', faqs=faqs)

# Route to archive FAQs from "faqs" table
@app.route('/archive_faq/<string:answer>', methods=['POST'])
def archive_faq(answer):
    cur = mysql.connection.cursor()
    # Retrieve FAQ data from faqs table based on answer
    cur.execute("SELECT * FROM faqs WHERE answer = %s", (answer,))
    faq_data = cur.fetchone()
    if faq_data:
        # Retrieve FAQ data from faqs table based on answer
        cur.execute("INSERT INTO archived_faqs (archived_question, archived_answer) VALUES (%s, %s)", (faq_data[1], faq_data[2]))
        mysql.connection.commit()
        # Delete FAQ data from faqs table based on answer
        cur.execute("DELETE FROM faqs WHERE answer = %s", (answer,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'FAQ archived successfully'}), 200
    else:
        cur.close()
        return jsonify({'message': 'FAQ not found'}), 404



# Route to fetch the images/files from "files" table for the editFile.html
@app.route('/fetch_archive')
def fetch_archive():
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_path, files_name FROM files")
    files = cur.fetchall()
    cur.close()
    return render_template('editFile.html', files=files)

# Route to archive files from "files" table for the editFile.html
@app.route('/archive_file/<filename>', methods=['POST'])
def archive_file(filename):
    cur = mysql.connection.cursor()
    # Retrieve file data from files table
    cur.execute("SELECT * FROM files WHERE files_name = %s", (filename,))
    file_data = cur.fetchone()
    if file_data:
        # Retrieve file data from files table based on filename
        cur.execute("INSERT INTO archived_data (archived_files_name, archived_file_path) VALUES (%s, %s)", (file_data[2], file_data[1]))
        mysql.connection.commit()
        # Delete file data from files table
        cur.execute("DELETE FROM files WHERE file_id = %s", (file_data[0],))  # Assuming file_id is the first column
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'File archived successfully'}), 200
    else:
        cur.close()
        return jsonify({'message': 'File not found'}), 404


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addFile')
def addFile():
    return render_template('addFile.html')

@app.route('/editFile')
def editFile():
    return fetch_archive() # Fetch data before rendering the template

@app.route('/editFaq')
def editFaq():
    return fetch_archive_faqs() # Fetch data before rendering the template

@app.route('/readFile')
def readFile():
    return fetch_data()  # Fetch data before rendering the template

@app.route('/readFaq')
def readFaqText():
    return fetch_faqs() # Fetch data before rendering the template

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)