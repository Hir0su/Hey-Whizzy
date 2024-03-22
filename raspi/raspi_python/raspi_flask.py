from flask import Flask, request, render_template, jsonify, send_from_directory
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

@app.route('/raspi_fetch')
def raspi_fetch():
    user_input = request.args.get('user_input')  # Get the user input from request
    if user_input:
        cur = mysql.connection.cursor()
        cur.execute("SELECT answer FROM faqs WHERE question = %s", (user_input,))
        answer = cur.fetchone()
        cur.close()
        
        if answer:
            return answer[0]  # Return the answer
        else:
            return "Sorry, I couldn't find an answer for that question."
    else:
        return "No user input provided."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')