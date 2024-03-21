from flask import Flask, request ,render_template, jsonify, send_from_directory, session, redirect
import os
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


app = Flask(__name__, static_folder='static')

# Configuration for MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testwhizzy'
app.secret_key = 'owen'  # Set a secret key for session handling


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
        category_id = request.form.get('category')
        
        if file and question and answer and category_id:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Insert file path into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO faqs (question, answer, category_id) VALUES (%s, %s, %s)", (question, answer, category_id))
            cur.execute("INSERT INTO files (file_path, files_name, category_id) VALUES (%s, %s, %s)", (filepath, filename, category_id))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Submission uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Missing required fields'}), 400
        
# Route for logging in users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember_me')
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[3], password):
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if remember_me:
                session.permanent = True  # Set session to be permanent if "Remember me" is checked
                
            return redirect('/index')
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html')


# Route for registering users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/login')
    
    return render_template('register.html')

# Route for checking session time
@app.route('/check_session')
def check_session():
    if 'last_activity' in session:
        last_activity = datetime.strptime(session['last_activity'], '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()
        
        if current_time - last_activity > timedelta(minutes=5) and not session.permanent:
            session.clear()  # Clear session data if inactive for more than 5 minutes and not "Remember me"
            return jsonify({'status': 'logged_out'})
    
    session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Update last activity time
    return jsonify({'status': 'active'})


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

# Route to fetch category data
@app.route('/fetch_categories')
def fetch_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT category_id, category_name FROM category")
    categories = cur.fetchall()
    cur.close()
    return jsonify(categories)


# Route to fetch data eg. Files/images, Faq/Answers for editEvents.html
@app.route('/fetch_events')
def fetch_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT file_path, category_id FROM files")
    files = cur.fetchall()
    cur.execute("SELECT * FROM faqs")
    faqs = cur.fetchall()
    cur.close()
    return render_template('editEvents.html', files=files, faqs=faqs)

# Route to fetch data from Archive database for restoreFile.html
@app.route('/fetch_archive')
def fetch_archive():
    cur = mysql.connection.cursor()
    cur.execute("SELECT archived_file_path, category_id FROM archived_data")
    archived_files = cur.fetchall()
    cur.execute("SELECT * FROM archived_faqs")
    archived_faqs = cur.fetchall()
    cur.close()
    return render_template('restoreFile.html', archived_files=archived_files, archived_faqs=archived_faqs)
    

# Route for Archiving in editEvents.html
@app.route('/archive_data', methods=['POST'])
def archive_data():
    try:
        faq_id = request.json['faqId']  # Get the FAQ ID from the request payload
        
        print(f"Archiving data for FAQ ID: {faq_id}")
        
        with mysql.connection.cursor() as cursor:
            # Archive specific entry from 'faqs' table to 'archived_faqs' table
            cursor.execute("INSERT INTO archived_faqs (archived_question, archived_answer, category_id) SELECT question, answer, category_id FROM faqs WHERE faq_id = %s", (faq_id,))
            print("Archived FAQ entry")
            
            cursor.execute("DELETE FROM faqs WHERE faq_id = %s", (faq_id,))  # Remove specific entry from original table
            print("Deleted FAQ entry from original table")
            
            mysql.connection.commit()

            # Archive specific entry from 'files' table to 'archived_data' table
            cursor.execute("INSERT INTO archived_data (archived_files_name, archived_file_path, category_id) SELECT files_name, file_path, category_id FROM files WHERE file_id = %s", (faq_id,))
            print("Archived file entry")
            
            cursor.execute("DELETE FROM files WHERE file_id = %s", (faq_id,))  # Remove specific entry from original table
            print("Deleted file entry from original table")
            
            mysql.connection.commit()

        print("Data archived successfully")
        return jsonify({"message": "Data archived successfully"}), 200

    except Exception as e:
        print(f"Error archiving data: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Route for Restoring files from archive database
@app.route('/restore_data', methods=['POST'])
def restore_data():
    try:
        faq_id = request.json['faqId']  # Get the FAQ ID from the request payload
        
        print(f"Restoring data for FAQ ID: {faq_id}")
        
        with mysql.connection.cursor() as cursor:
            # Restore specific entry from 'archived_faqs' to 'faqs' table
            cursor.execute("INSERT INTO faqs (question, answer, category_id) SELECT archived_question, archived_answer, category_id FROM archived_faqs WHERE ar_faq_id = %s", (faq_id,))
            print("Restored FAQ entry")
            
            cursor.execute("DELETE FROM archived_faqs WHERE ar_faq_id = %s", (faq_id,))  # Remove specific entry from archive table
            print("Deleted FAQ entry from archive table")
            
            mysql.connection.commit()
            
            # Restore specific entry from 'archived_data' to 'files' table
            cursor.execute("INSERT INTO files (files_name, file_path, category_id) SELECT archived_files_name, archived_file_path, category_id FROM archived_data WHERE ar_data_id = %s", (faq_id,))
            print("Restored file entry")
            
            cursor.execute("DELETE FROM archived_data WHERE ar_data_id = %s", (faq_id,))  # Remove specific entry from archive table
            print("Deleted file entry from archive table")
            
            mysql.connection.commit()
        
        print("Data restored successfully")
        return jsonify({"message": "Data restored successfully"}), 200
    
    except Exception as e:
        print(f"Error restoring data: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return redirect('/index')  # Redirect to the index page if already logged in
    else:
        return redirect('/login')  # Redirect to the login page if not logged in

@app.route('/index')
def index():
    if 'logged_in' in session and session['logged_in']:
        return fetch_form()  # Fetch data before rendering the template
    else:
        return redirect('/login')  # Redirect to the login page if not logged 
    
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect('/login')  # Redirect to the login page

@app.route('/editEvents')
def editEvents():
    return fetch_events() # Fetch data before rendering the template

@app.route('/restoreFile')
def restoreFile():
    return fetch_archive() # Fetch data before rendering the template

@app.route('/addFile')
def addFile():
    return render_template('addFile.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)