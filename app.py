import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import pickle

app = Flask(__name__)

with open("model/model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            sentiment VARCHAR(20)
        );
        ''')
        mysql.connection.commit()  
        cur.close()

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message, sentiment FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    
    # Predict sentiment
    X = vectorizer.transform([new_message])
    prediction = model.predict(X)[0]
    sentiment = "Positive" if prediction == 1 else "Negative"

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message, sentiment) VALUES (%s, %s)', [new_message, sentiment])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message, 'sentiment': sentiment})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['text']
    X = vectorizer.transform([data])
    prediction = model.predict(X)[0]

    return jsonify({
        "input": data,
        "prediction": "Positive" if prediction == 1 else "Negative"
    })
    
    
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    
