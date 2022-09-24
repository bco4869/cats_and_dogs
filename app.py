from flask import Flask, render_template, request, session
import os
import keras
from keras.preprocessing import image
import numpy as np
import pickle
from werkzeug.utils import secure_filename


# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'

filename = 'cats-dogs_small_2.pkl'
model = pickle.load(open(filename, 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

        return render_template('home2.html')

@app.route('/result')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)

    # Display image in Flask application web page
    return render_template('result.html', user_image = img_file_path, prediction_text='This is cat')

if __name__ == '__main__':
    app.run(debug=True)
