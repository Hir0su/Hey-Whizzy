from flask import Flask, request ,render_template, jsonify, send_from_directory, session, redirect, url_for, flash
import os, re, smtplib, secrets, string
from email.mime.text import MIMEText
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


app = Flask(__name__, static_folder='static')

# Configuration for MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testwhizzy'
app.secret_key = 'owensecret'  # Set a secret key for session handling


# Initialize MySQL
mysql = MySQL(app)

# Directory for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for serving static files eg. CSS/JS files
app.static_folder = 'static'

# Route for accessing uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload_form', methods=['POST'])
def upload_data():
    if request.method == 'POST':
        file = request.files.get('file')
        question = request.form.get('question')
        answer = request.form.get('answer')
        category_id = request.form.get('category')

        if question and answer and category_id:
            # Insert question, answer, and category_id into the "entries" table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO entries (question, answer, category_id) VALUES (%s, %s, %s)", (question, answer, category_id))
            entry_id = cur.lastrowid  # Get the auto-generated entry_id

            # If a file was uploaded, save it and update the "entries" table with the file details
            if file:
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                cur.execute("UPDATE entries SET file_name = %s, file_path = %s WHERE entry_id = %s", (filename, filepath, entry_id))

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

# Route for Forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        if email:
            # Check if the email exists in the database
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

            if user:
                # Generate a random token
                token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

                # Store the token in the database
                cur.execute("UPDATE users SET reset_token = %s WHERE email = %s", (token, email))
                mysql.connection.commit()

                # Construct the email message
                reset_url = url_for('reset_password', token=token, _external=True)
                msg = MIMEText(f'Please click the following link to reset your password: {reset_url}')
                msg['Subject'] = 'Password Reset Request'
                msg['From'] = 'Whizzy'
                msg['To'] = email

                try:
                    # Send the email
                    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp_server.starttls()
                    smtp_server.login('2023it07@gmail.com', 'knpn ssqa wedd dvuy')
                    smtp_server.send_message(msg)
                    smtp_server.quit()
                    flash('An email has been sent with instructions to reset your password.', 'success')
                except smtplib.SMTPException as e:
                    print(f"SMTP Error: {str(e)}")
                    flash('An error occurred while sending the email. Please try again later.', 'error')
            else:
                flash('The email address you entered is not registered.', 'error')

            cur.close()
        else:
            flash('Please enter your email address.', 'error')

    return render_template('PasswordReset.html')

# Route for Reset Password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password == confirm_password:
            # Check if the token is valid
            cur = mysql.connection.cursor()
            cur.execute("SELECT user_id FROM users WHERE reset_token = %s", (token,))
            user = cur.fetchone()

            if user:
                user_id = user[0]  # Assuming the first column is the user_id

                try:
                    # Update the user's password
                    hashed_password = generate_password_hash(new_password)
                    cur.execute("UPDATE users SET password = %s, reset_token = NULL WHERE user_id = %s", (hashed_password, user_id))
                    mysql.connection.commit()
                    flash('Your password has been reset successfully.', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    print(f"Error resetting password: {str(e)}")
                    flash('An error occurred while resetting your password. Please try again later.', 'error')
            else:
                flash('The password reset link is invalid or has expired.', 'error')

            cur.close()
        else:
            flash('The new password and confirmation password do not match.', 'error')

    return render_template('PasswordReset.html', token=token)


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


# Route to fetch data eg.Files/images,Faq/Answers for index.html it also includes the search function
@app.route('/fetch_form')
def fetch_form():
    query = request.args.get('q', '').strip()  # Get the search query from the request
    keywords = query.split()  # Split the query into individual keywords

    if keywords:
        cur = mysql.connection.cursor()
        conditions = []
        for keyword in keywords:
            # Escape the keyword to treat special characters as literals
            escaped_keyword = re.escape(keyword)
            
            # Create conditions with and without special characters
            condition_without_special_chars = f"e.question LIKE '%{keyword}%'"
            condition_with_special_chars = f"e.question LIKE '%{escaped_keyword}%'"
            
            # Add both conditions to the list
            conditions.append(condition_without_special_chars)
            conditions.append(condition_with_special_chars)
        
        conditions_str = " OR ".join(conditions)
        cur.execute(f"SELECT e.file_path, e.file_name, e.question, e.answer, e.category_id "
                    f"FROM entries e "
                    f"WHERE {conditions_str}")
        search_results = cur.fetchall()
        cur.close()
        return render_template('index.html', entries=search_results)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT file_path, file_name, question, answer, category_id FROM entries")
        entries = cur.fetchall()
        cur.close()
        return render_template('index.html', entries=entries)


# Route to fetch data eg. Files/images, Faq/Answers for editEvents.html
@app.route('/fetch_events')
def fetch_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT entry_id, question, answer, file_name, file_path, category_id FROM entries")
    entries = cur.fetchall()
    cur.close()
    return render_template('editEvents.html', entries=entries)

# Route to fetch data from Archive database for restoreFile.html
@app.route('/fetch_archive')
def fetch_archive():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ar_entry_id, archived_question, archived_answer, archived_file_name, archived_file_path, category_id FROM archived_entries")
    archived_entries = cur.fetchall()
    cur.close()
    return render_template('restoreFile.html', archived_entries=archived_entries)

    
# Route to fetch category data
@app.route('/fetch_categories')
def fetch_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT category_id, category_name FROM category")
    categories = cur.fetchall()
    cur.close()
    return jsonify(categories)
    

# Route for Archiving files from entries table.
@app.route('/archive_data', methods=['POST'])
def archive_data():
    try:
        entry_id = request.json['entryId']  # Get the Entry ID from the request payload
        
        print(f"Archiving data for entry ID: {entry_id}")
        
        with mysql.connection.cursor() as cursor:
            try:
                # Archive specific entry from 'entries' table to 'archived_entries' table
                cursor.execute("INSERT INTO archived_entries (archived_question, archived_answer, archived_file_name, archived_file_path, category_id) SELECT question, answer, file_name, file_path, category_id FROM entries WHERE entry_id = %s", (entry_id,))
                print("Archived Entry")
                
                # Check if any rows were affected by the INSERT statement
                if cursor.rowcount == 0:
                    raise ValueError(f"No entry found with ID: {entry_id}")
                
                cursor.execute("DELETE FROM entries WHERE entry_id = %s", (entry_id,))  # Remove specific entry from original table
                print("Deleted Entry from original table")
                
                mysql.connection.commit()
                
            except Exception as e:
                print(f"Error archiving data: {str(e)}")
                mysql.connection.rollback()  # Rollback the transaction if an error occurs
                raise e

        print("Data archived successfully")
        return jsonify({"message": "Data archived successfully"}), 200

    except Exception as e:
        print(f"Error archiving data: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    
# Route for Restoring files from archive database
@app.route('/restore_data', methods=['POST'])
def restore_data():
    try:
        entry_id = request.json['entryId']  # Get the entry ID from the request payload
        
        print(f"Restoring data for entry ID: {entry_id}")
        
        with mysql.connection.cursor() as cursor:
            # Restore specific entry from 'archived_entries' to 'entries' table
            cursor.execute("INSERT INTO entries (question, answer, file_name, file_path, category_id) SELECT archived_question, archived_answer, archived_file_name, archived_file_path, category_id FROM archived_entries WHERE ar_entry_id = %s", (entry_id,))
            print("Restored Entry")
            
            cursor.execute("DELETE FROM archived_entries WHERE ar_entry_id = %s", (entry_id,))  # Remove specific entry from archive table
            print("Deleted entry from archived_entries table")
            
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
