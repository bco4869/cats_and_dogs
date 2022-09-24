from flask import Flask, render_template, request, session
import os
import numpy as np
import pickle
from werkzeug.utils import secure_filename
#from keras.preprocessing import image
from tensorflow.keras.utils import load_img, img_to_array
import tensorflow as tf

# WSGI Application
# Defining upload folder path
#UPLOAD_FOLDER = os.path.join('static', 'uploads')
UPLOAD_FOLDER = './static/uploads'
# Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'

#filename = 'cats-dogs_small_2.pkl'
#model = pickle.load(open(filename, 'rb'))
filename = 'cats_and_dogs_small_2.h5'
model = tf.keras.models.load_model(filename)

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

    img = load_img(img_file_path, target_size=(150, 150))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images/255.0, batch_size=8, verbose=0)

    #print(classes) # Be sure that your model is working

    #pic = os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename)

    pic = session.get('uploaded_img_file_path', None)

    chance = int(classes[0] * 100)
    if classes[0] > 0.5:
        return render_template('result.html', user_image=pic,prediction_text='most likely to be a dog: percentage = {}% (~0% = cat, ~100% = dog)'.format(chance))
    else:
        return render_template('result.html', user_image=pic,prediction_text='most likely to be a cat: percentage = {}% (~0% = cat, ~100% = dog)'.format(chance))

if __name__ == '__main__':
    app.run(debug=True,port=9989,use_reloader=False,threaded=False)
