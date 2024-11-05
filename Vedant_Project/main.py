from flask import Flask, render_template, redirect, url_for, request, jsonify
import mysql.connector

app = Flask(__name__)

db = {
    'host': 'localhost',
    'database': 'test',
    'user': 'root',
    'password': 'HashedStrong@6904'
}

try:
    connection = mysql.connector.connect(**db)
    if connection.is_connected():
        print("Database connected successfully")
except mysql.connector.Error as e:
    print("Error:", e)

cursor = connection.cursor()

@app.route('/')
def login_redirect():
    return redirect(url_for("landing"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username != '':
            cursor.execute("SELECT password FROM login WHERE username=%s", (username,))
            user = cursor.fetchone()
            if user:
                if password == user[0]:
                    return render_template("home.html")
                else:
                    return render_template('login.html', message='Invalid password')
            else:
                return render_template('login.html', message='Invalid username')
        else:
            return render_template('login.html', message="Please enter a username.")
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if 'new_username' in request.form and 'new_password' in request.form: 
            new_username = request.form["new_username"]
            new_password = request.form["new_password"]
            if new_username != '' and new_username != new_password:
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, new_password))  # Store plain password
                    connection.commit()
                    return redirect(url_for('login'))
                except mysql.connector.IntegrityError:
                    return render_template('register.html', message='Username already exists')
            else:
                return render_template('register.html', message="Invalid entry!")
        else:
            return render_template('register.html')
    return render_template("register.html")

@app.route('/landing', methods=['GET', 'POST'])
def landing():
    if request.method == "POST":
        return redirect(url_for('login'))
    else:
        return render_template("landing.html")

if __name__ == "__main__":
    app.run(debug=True)
