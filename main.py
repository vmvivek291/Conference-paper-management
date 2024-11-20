from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, flash
import mysql.connector
from mysql.connector import Error
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'vivek2024',
    'database': 'CPMS'
}



# Helper function to establish a new database connection for each request
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    return connection, cursor

@app.route('/')
def login_redirect():
    return redirect(url_for("landing"))

@app.route('/landing', methods=['GET', 'POST'])
def landing():
    if request.method == "POST":
        return redirect(url_for('login'))
    else:
        return render_template("landing.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    connection, cursor = get_db_connection()
    if request.method == "POST":
        data = request.get_json()
        role = data.get("role")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        try:
            if role == "author":
                cursor.execute("SELECT * FROM Authors WHERE Email = %s AND Name = %s", (email, name))
                existing_user = cursor.fetchone()
                if existing_user:
                    return jsonify({"message": "Author already registered. Redirecting to login.", "redirect": True})

                age = data.get("age")
                bio = data.get("bio")
                cursor.execute(
                    "INSERT INTO Authors (Name, Age, Email, Bio, Password) VALUES (%s, %s, %s, %s, %s)",
                    (name, age, email, bio, password)
                )
                connection.commit()

                cursor.execute("SELECT Author_ID FROM Authors WHERE Email = %s AND Name = %s", (email, name))
                author_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO Registration (RegistrationType, Name, Password, Author_ID) VALUES (%s, %s, %s, %s)",
                    ('Author', name, password, author_id)
                )
                connection.commit()

                return jsonify({"message": "Author registered successfully!", "redirect": True})

            elif role == "reviewer":
                cursor.execute("SELECT * FROM Reviewer WHERE Email = %s AND Name = %s", (email, name))
                existing_user = cursor.fetchone()
                if existing_user:
                    return jsonify({"message": "Reviewer already registered. Redirecting to login.", "redirect": True})

                conference_id = data.get("conference_id")
                cursor.execute(
                    "INSERT INTO Reviewer (Name, Password, Email, Conference_ID) VALUES (%s, %s, %s, %s)",
                    (name, password, email, conference_id)
                )
                connection.commit()

                cursor.execute("SELECT Reviewer_ID FROM Reviewer WHERE Email = %s AND Name = %s", (email, name))
                reviewer_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO Registration (RegistrationType, Name, Password, Reviewer_ID) VALUES (%s, %s, %s, %s)",
                    ('Reviewer', name, password, reviewer_id)
                )
                connection.commit()

                return jsonify({"message": "Reviewer registered successfully!", "redirect": True})

            return jsonify({"message": "Invalid role", "redirect": False})

        finally:
            cursor.close()
            connection.close()

    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        connection, cursor = get_db_connection()
        try:
            data = request.get_json()
            role = data.get("role")
            name = data.get("name")
            password = data.get("password")

            if role == "author":
                query = """
                    SELECT Author_ID FROM Registration 
                    WHERE Name = %s AND Password = %s AND RegistrationType = 'Author'
                """
                cursor.execute(query, (name, password))
                result = cursor.fetchone()
                if result:
                    author_id = result[0]
                    # Return JSON response with the redirect URL for the author profile
                    return jsonify({
                        "message": "Login successful!",
                        "redirect": url_for('author_home', author_id=author_id)
                    })
                else:
                    return jsonify({"message": "Invalid author credentials"}), 401

            elif role == "reviewer":
                query = """
                    SELECT Reviewer_ID FROM Registration 
                    WHERE Name = %s AND Password = %s AND RegistrationType = 'Reviewer'
                """
                cursor.execute(query, (name, password))
                result = cursor.fetchone()
                if result:
                    reviewer_id = result[0]
                    # Return JSON response with the redirect URL for the reviewer profile
                    return jsonify({
                        "message": "Login successful!",
                        "redirect": url_for('reviewer_profile', reviewer_id=reviewer_id)
                    })
                else:
                    return jsonify({"message": "Invalid reviewer credentials"}), 401

            return jsonify({"message": "Invalid role specified"}), 400

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return jsonify({"message": "Database error"}), 500
        finally:
            cursor.close()
            connection.close()
    return render_template("login.html")

@app.route('/author/home/<author_id>')
def author_home(author_id):
    connection, cursor = get_db_connection()
    try:
        # Get author details
        author_query = "SELECT * FROM authors WHERE author_id = %s"
        cursor.execute(author_query, (author_id,))
        author = cursor.fetchone()
        
        if not author:
            flash("Author not found", "error")
            return redirect(url_for('login'))
            
        # Get conference list
        conf_query = "SELECT DISTINCT Conference_ID, Name, Location, Date, Organizer FROM conference"
        cursor.execute(conf_query)
        conferences = cursor.fetchall()
        
        return render_template(
            'author_home.html',
            author={
                'id': author[0],
                'name': author[1],
                'age': author[2],
                'email': author[3],
                'bio': author[4]
            },
            conferences=conferences,
        )
        
    except mysql.connector.Error as err:
        flash(f"Database error: {str(err)}", "error")
        return redirect(url_for('login'))
    finally:
        cursor.close()
        connection.close()

@app.route('/author/select_conference/<author_id>', methods=['POST'])
def select_conference(author_id):
    conference_id = request.form.get('conference_id')
    if not conference_id:
        flash("Please select a conference", "error")
        return redirect(url_for('author_home', author_id=author_id))
    return redirect(url_for('upload_pdf', authorid=author_id, conferenceid=conference_id))


@app.route('/home/author_profile/<author_id>')
def author_profile(author_id):
    connection, cursor = get_db_connection()
    try:
        cursor = connection.cursor()

        # Author details
        cursor.execute("SELECT * FROM authors WHERE author_id = %s", (author_id,))
        author_data = cursor.fetchone()

        if not author_data:
            return "Author not found", 404

        # Published papers
        published_query = """
            SELECT p.Paper_ID, p.Title, c.Name
            FROM Papers p
            JOIN Paper_Uploads pu ON p.Paper_ID = pu.Paper_ID
            JOIN Conference c ON p.Conference_ID = c.Conference_ID
            WHERE pu.Author_ID = %s AND p.Status = 'Accepted'
        """
        cursor.execute(published_query, (author_id,))
        published_papers = [
            {"paper_id": row[0], "title": row[1], "feedback": row[2]}
            for row in cursor.fetchall()
        ]

        # Submissions
        submissions_query = """
            SELECT p.Paper_ID, p.Title, pu.Submission_date
            FROM Papers p
            JOIN Paper_Uploads pu ON p.Paper_ID = pu.Paper_ID
            WHERE pu.Author_ID = %s
            ORDER BY pu.Submission_date DESC
        """
        cursor.execute(submissions_query, (author_id,))
        submitted_papers = [
            {"paper_id": row[0], "title": row[1], "feedback": row[2].strftime('%Y-%m-%d')}
            for row in cursor.fetchall()
        ]

        return render_template(
            'Author_profile.html',
            author=author_data,
            published_papers=published_papers,
            submitted_papers=submitted_papers
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

@app.route('/author/<author_id>/track-paper', methods=['POST'])
def track_paper(author_id):
    connection, cursor = get_db_connection()
    try:
        data = request.get_json()
        paper_id = data.get('paper_id')

        if not paper_id:
            return jsonify({"error": "Paper ID is required"}), 400

        cursor = connection.cursor()
        track_query = """
            SELECT 
                p.Paper_ID,
                p.Title,
                p.Status,
                p.Feedback,
                c.Name as Conference_Name
            FROM Papers p
            JOIN Paper_Uploads pu ON p.Paper_ID = pu.Paper_ID
            JOIN Conference c ON p.Conference_ID = c.Conference_ID
            WHERE p.Paper_ID = %s AND pu.Author_ID = %s
        """
        
        cursor.execute(track_query, (paper_id, author_id))
        paper_details = cursor.fetchone()

        if not paper_details:
            return jsonify({
                "error": "Paper not found or you don't have permission to view this paper"
            }), 404

        response = {
            "Paper ID": paper_details[0],
            "Title": paper_details[1],
            "Status": paper_details[2],
            "Feedback": paper_details[3],
            "Conference Name": paper_details[4]
        }

        return jsonify(response), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({
            "error": "Database error"
        }), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/view_pdf/<paper_id>')
def view_pdf(paper_id):
    connection, cursor = get_db_connection()
    try:
        query = "SELECT Manuscript FROM papers WHERE Paper_ID = %s"
        cursor.execute(query, (paper_id,))
        pdf_data = cursor.fetchone()

        if pdf_data and pdf_data[0]:
            pdf_file = io.BytesIO(pdf_data[0])
            return send_file(pdf_file, mimetype='application/pdf')
        else:
            return "PDF not found", 404

    finally:
        cursor.close()
        connection.close()

@app.route('/home/author/<authorid>/<conferenceid>', methods=['GET', 'POST'])
def upload_pdf(authorid, conferenceid):
    if request.method == 'POST':
        try:

            title = request.form['title']
            abstract = request.form['abstract']
            category = request.form['category']
            version = request.form['version']
            file = request.files['file']

            print(title)
            print(abstract)
            print(category)

            if not all([title, abstract, category, version, file]):
                flash('All fields are required', 'error')
                return redirect(f'/home/author/{authorid}/{conferenceid}')

            if not file or not file.filename.endswith('.pdf'):
                flash('Please upload a valid PDF file.', 'error')
                return redirect(f'/home/author/{authorid}/{conferenceid}')

            pdf_data = file.read()

            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert paper into the Papers table
            query = """
                INSERT INTO Papers (
                    Title, 
                    Abstract, 
                    Category, 
                    Status, 
                    Version, 
                    Conference_ID,
                    Manuscript
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                title,
                abstract,
                category,
                'Submitted',
                version,
                conferenceid,
                pdf_data
            )

            cursor.execute(query, values)
            conn.commit()

            # Retrieve the Paper_ID of the newly inserted paper
            cursor.execute("SELECT Paper_ID FROM Papers ORDER BY Paper_ID DESC LIMIT 1")
            paper_id = cursor.fetchone()[0]
            print(paper_id)

            # Call InsertIntoPaperUploads to link the paper with the author
            query = "CALL InsertIntoPaperUploads(%s, %s)"
            cursor.execute(query, (authorid, paper_id))
            conn.commit()

            # Assign a random reviewer from the same conference
            update_query = """
                UPDATE Papers AS p
                SET Reviewer_ID = (
                    SELECT Reviewer_ID
                    FROM Reviewer AS r
                    WHERE r.Conference_ID = p.Conference_ID
                    ORDER BY RAND()
                    LIMIT 1
                )
                WHERE p.Paper_ID = %s AND p.Conference_ID = %s
            """
            cursor.execute(update_query, (paper_id, conferenceid))
            conn.commit()

            flash('Paper uploaded successfully!', 'success')
            return redirect(f'/home/author/{authorid}/{conferenceid}')

        except mysql.connector.Error as db_error:
            print(f"Database error: {str(db_error)}")
            flash(f'Database error occurred: {str(db_error)}', 'error')
            return redirect(f'/home/author/{authorid}/{conferenceid}')

        except Exception as e:
            print(f"General error: {str(e)}")
            flash('An unexpected error occurred', 'error')
            return redirect(f'/home/author/{authorid}/{conferenceid}')

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template('upload.html', authorid=authorid, conferenceid=conferenceid)

@app.route('/home/reviewer/<reviewer_id>', methods=['GET', 'POST'])
def reviewer_profile(reviewer_id):
    connection,cursor = get_db_connection()
    if not connection:
        return "Database connection error", 500

    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for named access

        # Reviewer details
        cursor.execute("""
            SELECT r.*, c.Name AS c_Name
            FROM Reviewer r
            JOIN Conference c ON r.Conference_ID = c.Conference_ID
            WHERE r.Reviewer_ID = %s;
        """, (reviewer_id,))
        reviewer_data = cursor.fetchone()
        # print(reviewer_data)

        if not reviewer_data:
            return "Reviewer not found", 404
        
        # Get assigned papers
        assigned_papers_query = """
            SELECT p.Paper_ID, p.Title, p.Abstract, p.Category, p.version, p.status
            FROM papers p
            WHERE p.Reviewer_ID = %s 
            AND p.status IN ('Submitted', 'Under review')
            ORDER BY p.Paper_ID DESC
        """
        cursor.execute(assigned_papers_query, (reviewer_id,))
        assigned_papers = cursor.fetchall()

        # Handle feedback submission
        if request.method == 'POST':
            paper_id = request.form.get('paper_id')
            feedback = request.form.get('feedback')
            review_status = int(request.form.get('review_status', 0))  
            
            if paper_id and feedback is not None:
                try:
                    

                    if review_status == 0:
                        
                        cursor.execute("UPDATE Papers SET Status = %s WHERE Paper_ID = %s", ('Rejected', paper_id))
                    else:
                        cursor.execute("UPDATE Papers SET Status = %s WHERE Paper_ID = %s", ('Accepted', paper_id))

                    connection.commit()
                    
                    connection.commit()

                    if paper_id and feedback:
                        update_query = """
                            UPDATE papers 
                            SET feedback = %s
                            WHERE Paper_ID = %s AND Reviewer_ID = %s
                        """
                        cursor.execute(update_query, (feedback, paper_id, reviewer_id))
                        connection.commit()

                    return jsonify({"success": True, "message": "Feedback submitted successfully"})

                except mysql.connector.Error as err:
                    return jsonify({"success": False, "message": str(err)})
            return jsonify({"success": False, "message": "Missing required fields"})

        return render_template(
            'reviewer_profile.html',
            reviewer=reviewer_data,
            assigned_papers=assigned_papers
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return "Database error", 500
    finally:
        cursor.close()
        connection.close()

@app.route('/upload_view_pdf/<paper_id>')
def upload_view_pdf(paper_id):
   
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT Manuscript FROM papers WHERE Paper_ID = %s"
    cursor.execute(query, (paper_id,))
    pdf_data = cursor.fetchone()
    cursor.close()
    conn.close()

    print(pdf_data[0])

   
    if pdf_data and pdf_data[0]:
        pdf_file = io.BytesIO(pdf_data[0])
        print(pdf_file)
        return send_file(pdf_file, as_attachment=False, mimetype='application/pdf')
    else:
        flash('No manuscript found for the given Paper ID!', 'error')
        return redirect('/upload')

@app.route('/landing/<organizer>', methods=['GET', 'POST'])
def display_conferences(organizer):
    connection, cursor = get_db_connection()
    if not connection:
        return "Database connection error", 500
    
    cursor = connection.cursor(dictionary=True)
    
    display_query = """ 
    SELECT Conference_ID, Name
    FROM Conference 
    WHERE Organizer = %s
    ORDER BY Name ASC
    """
    
    try:
        cursor.execute(display_query, (organizer,))
        conferences = cursor.fetchall()
        
        return render_template('Conferences.html', 
                             conferences=conferences,
                             organizer=organizer)
    
    except mysql.connector.Error as err:
        print(f"Error querying database: {err}")
        return "Database query error", 500
    
    finally:
        cursor.close()
        connection.close()


import base64

def convert_blobs(data):
    if isinstance(data, bytes):  # BLOB data is typically in bytes format
        return base64.b64encode(data).decode('utf-8')
    elif isinstance(data, dict):
        return {k: convert_blobs(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_blobs(item) for item in data]
    return data

@app.route('/search', methods=['POST'])
def search_papers():
    data = request.get_json()
    search_term = data.get('searchTerm')
    search_filter = data.get('searchFilter')

    print(data)

    if not search_term or not search_filter:
        return jsonify({"error": "Invalid search parameters"}), 400

    connection, cursor = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection error"}), 500

    cursor = connection.cursor(dictionary=True)
    query = ""
    parameters = (f"%{search_term}%",)

    # Define queries based on filter
    if search_filter == 'author':
        query = """
            SELECT Paper_ID, Author_Name, Conference_Name, Paper_Title, Paper_Category, Manuscript 
            FROM Author_Conference_Papers
            WHERE Author_Name LIKE %s
        """
    elif search_filter == 'title':
        query = """
            SELECT Paper_ID, Author_Name, Conference_Name, Paper_Title, Paper_Category, Manuscript 
            FROM Author_Conference_Papers
            WHERE Paper_Title LIKE %s
        """
    elif search_filter == 'category':
        query = """
            SELECT Paper_ID, Author_Name, Conference_Name, Paper_Title, Paper_Category, Manuscript 
            FROM Author_Conference_Papers
            WHERE Paper_Category LIKE %s
        """
    else:
        return jsonify({"error": "Invalid filter"}), 400

    try:
        cursor.execute(query, parameters)
        results = cursor.fetchall()

        # Log the structure of the response for debugging
        print("Search results:", results)

        results = convert_blobs(results)
        # Ensure the JSON response matches what the frontend expects
        return jsonify(results)

    except mysql.connector.Error as err:
        print(f"Error querying database: {err}")
        return jsonify({"error": "Database query error"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/proceedings/<conference_id>')
def show_conference(conference_id):
    try:
        connection,cursor = get_db_connection()
        if not connection:
            return "Database connection error", 500
        
        cursor = connection.cursor(dictionary=True)

        # Conference details with parameterized query
        conference_query = """
            SELECT Conference_ID, Name, Date, Location,Organizer 
            FROM Conference
            WHERE Conference_ID = %s"""
        
        cursor.execute(conference_query, (conference_id,))
        conference_details = cursor.fetchone()
        
        if not conference_details:
            return "Conference not found", 404

        # Proceeding details
        proceeding_query = """
            SELECT ISSN, Volume, Number_of_pages
            FROM Proceedings 
            WHERE Conference_ID = %s"""

        cursor.execute(proceeding_query, (conference_id,))
        proceeding_details = cursor.fetchone()

        # Paper details
        paper_query = """
            SELECT Papers.Paper_ID, Title, Category, Status, Manuscript, Name
            FROM Papers
            INNER JOIN Paper_Uploads ON Papers.Paper_ID = Paper_Uploads.Paper_ID
            INNER JOIN Authors ON Paper_Uploads.Author_ID = Authors.Author_ID
            WHERE Papers.Conference_ID = %s AND Status = 'Accepted'
        """
        
        cursor.execute(paper_query, (conference_id,))
        paper_details = cursor.fetchall()

        aggregate_query = """
            SELECT COUNT(*) AS AcceptedPaperCount
            FROM Papers
            INNER JOIN Paper_Uploads ON Papers.Paper_ID = Paper_Uploads.Paper_ID
            WHERE Papers.Conference_ID = %s AND Status = 'Accepted'
        """

        cursor.execute(aggregate_query, (conference_id,))
        count = cursor.fetchone()

        print(count)
        proceeding_details["AcceptedPaperCount"] = count['AcceptedPaperCount']  # Store count with a meaningful key
        return render_template('Proceedings.html',
                             conference=conference_details,
                             proceedings=proceeding_details,
                             papers=paper_details)

    except Error as e:
        print(f"Database error: {str(e)}", 500)

if __name__ == "__main__":
    app.run(debug=True)