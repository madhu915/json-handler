from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
import redis

app = Flask(__name__)
app.secret_key = 'e824ba3c-dd15-4e0b-9cf7-768ab0be5312'

# Configure Flask-Session to use Redis for session storage
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True

# Create a Redis connection
redis_url = 'redis://localhost:6379/0'  # Replace with your Redis server URL
app.config['SESSION_REDIS'] = redis.StrictRedis.from_url(redis_url)

# Initialize Flask-Session
Session(app)

# Dummy JSON data to be stored in the session
initial_result = {
    "key1": "value1",
    "key2": "value2"
}

@app.before_request
def before_first_request():
    # Initialize the 'result' JSON data in the session
    session.setdefault('result', initial_result)

@app.route('/')
def index():
    # Store some data in the session
    session['key'] = 'value'
    return render_template('index.html', result=session['result'])

@app.route('/update', methods=['POST'])
def update_json():
    key = request.form.get('key')
    value = request.form.get('value')

    # Retrieve the current JSON data from the session
    result = session['result']

    # Update the JSON data with the new key-value pair
    result[key] = value

    # Update the JSON data in the session
    session['result'] = result

    return redirect(url_for('index'))

@app.route('/update2', methods=['POST'])
def update_json2():
    key = request.form.get('key')
    value = request.form.get('value')

    # Retrieve the current JSON data from the session
    result = session['result']

    # Update the JSON data with the new key-value pair
    result[key] = value

    # Update the JSON data in the session
    session['result'] = result

    return redirect(url_for('index'))

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    # Perform DB insert
    # Clear the session data
    session.clear()
    return redirect(url_for('index'))

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    # Clear the session data
    session.clear()
    # return jsonify({'message': 'Session data cleared successfully.'})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
