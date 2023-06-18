from flask import Flask, render_template, redirect, request, session, url_for, session
import mysql.connector
import PyPDF2
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "this is a secret key"

# MySQL connection setup
connection = mysql.connector.connect(
    host='*****',
    port=*****,
    database='****',
    user='*****',
    password='*****',
    auth_plugin='******',
    use_pure=True
)
cursor = connection.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM testtable WHERE username = %s', (username,))
        record = cursor.fetchone()
        if record and check_password_hash(record[2], password):
            session['username'] = record[1]
            return redirect(url_for('home'))
        else:
            error = 'Incorrect username or password. Please try again.'
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']  # Retrieve the name from the form
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM testtable WHERE username = %s', (username,))
        record = cursor.fetchone()
        if record:
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)
        else:
            hashed_password = generate_password_hash(password)
            # Insert new user into the database with name, username, and hashed password
            cursor.execute('INSERT INTO testtable (name, username, password) VALUES (%s, %s, %s)', (name, username, hashed_password))
            connection.commit()
            session['username'] = username
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Store the feedback in the MySQL database
        connection = mysql.connector.connect(
            host='*****',
            port=*****,
            database='****',
            user='*****',
            password='*****',
            auth_plugin='******',
            use_pure=True
        )
        cursor = connection.cursor()
        insert_query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, message))
        connection.commit()
        cursor.close()
        connection.close()
        success_message = "Thank you for your feedback!"
        return render_template('feedback.html', message=success_message)
    return render_template('feedback.html')


@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('index'))
    
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        # You can retrieve the name from the database based on the username
        cursor.execute('SELECT name FROM testtable WHERE username = %s', (username,))
        record = cursor.fetchone()
        if record:
            name = record[0]
            return render_template('dashboard.html', name=name, username=username)
    return redirect(url_for('index'))


@app.route('/analyse', methods=['POST'])
def analyse():
    # Get the PDF file path from the form data
#pdf_path = open('example.pdf', 'rb')#request.files['pdf']
    
    #fp = open('example.pdf', 'rb')
    
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(request.files['pdf'])

    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)

    # Loop through all pages in the PDF file
    page_text = ""
    for page_num in range(num_pages):

        # Get the text content of the current page
        page_obj = pdf_reader.pages[num_pages-1]
        page_text += page_obj.extract_text()

    # Call the summarizer function to get the summary
    summary, doc, len_rawdocs, len_summary = summarizer(page_text)

    # Render the summary page with the summary and other data
    return render_template('summary.html',page_text=page_text, summary=summary, len_rawdocs=len_rawdocs, len_summary=len_summary,)

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

    # Calculate word frequency
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # Normalize word frequency
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # Calculate sentence scores based on word frequency
    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    # Select the top sentences as summary
    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
