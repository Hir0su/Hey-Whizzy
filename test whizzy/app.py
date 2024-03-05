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
@app.route('/upload_form', methods=['POST'])
def upload_data():
    if request.method == 'POST':
        file = request.files.get('file')
        question = request.form.get('question')
        answer = request.form.get('answer')
        
        if file and question and answer:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Insert file path into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO faqs (question, answer) VALUES (%s, %s)", (question, answer))
            cur.execute("INSERT INTO files (file_path, files_name) VALUES (%s, %s)", (filepath, filename))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Submission uploaded successfully'}), 200
        else:
            return jsonify({'message': 'No file provided'}), 400

# Route to fetch data eg.Files/images,Faq/Answers for index.html
@app.route('/fetch_form')
def fetch_form():
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_path FROM files")
    files = cur.fetchall()
    cur.execute("SELECT * FROM faqs")
    faqs = cur.fetchall()
    cur.close()
    return render_template('index.html', files=files, faqs=faqs)

# Route to fetch data eg. Files/images, Faq/Answers for editEvents.html
@app.route('/fetch_events')
def fetch_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_path FROM files")
    files = cur.fetchall()
    cur.execute("SELECT * FROM faqs")
    faqs = cur.fetchall()
    cur.close()
    return render_template('editEvents.html', files=files, faqs=faqs)

# Route to fetch data from Archive database for restoreFile.html
@app.route('/fetch_archive')
def fetch_archive():
    cur = mysql.connection.cursor()
    cur.execute("SELECT archived_file_path FROM archived_data")
    archived_files = cur.fetchall()
    cur.execute("SELECT * FROM archived_faqs")
    archived_faqs = cur.fetchall()
    cur.close()
    return render_template('restoreFile.html', archived_files=archived_files, archived_faqs=archived_faqs)
    

# Route for Archiving in editEvents.html
@app.route('/archive_data', methods=['POST'])
def archive_data():
    try:
        with mysql.connection.cursor() as cursor:
            # Archive data from 'faqs' table to 'archived_faqs' table
            cursor.execute("INSERT INTO archived_faqs (archived_question, archived_answer) SELECT question, answer FROM faqs")
            cursor.execute("DELETE FROM faqs")  # Remove data from original table
            mysql.connection.commit()

            # Archive data from 'files' table to 'archived_data' table
            cursor.execute("INSERT INTO archived_data (archived_files_name, archived_file_path) SELECT files_name, file_path FROM files")
            cursor.execute("DELETE FROM files")  # Remove data from original table
            mysql.connection.commit()

        return jsonify({"message": "Data archived successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for Restoring files from archive database
@app.route('/restore_data', methods=['POST'])
def restore_data():
    try:
        with mysql.connection.cursor() as cursor:
            # Restore data from 'archived_faqs' to 'faqs' table
            cursor.execute("INSERT INTO faqs (question, answer) SELECT archived_question, archived_answer FROM archived_faqs")
            cursor.execute("DELETE FROM archived_faqs") # Remove data from original table
            mysql.connection.commit()
            
            # Archive data from 'files' table to 'archived_data' table
            cursor.execute("INSERT INTO files (files_name, file_path) SELECT archived_files_name, archived_file_path FROM archived_data")
            cursor.execute("DELETE FROM archived_data") # Remove data from original table
            mysql.connection.commit()
            
        return jsonify({"message": "Data restored successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return fetch_form() # Fetch data before rendering the template

@app.route('/editEvents')
def editEvents():
    return fetch_events() # Fetch data before rendering the template

@app.route('/restoreFile')
def restoreFile():
    return fetch_archive() # Fetch data before rendering the template

@app.route('/addFile')
def addFile():
    return render_template('addFile.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)