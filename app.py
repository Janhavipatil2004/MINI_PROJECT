from flask import Flask, request, render_template, redirect, url_for
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
model = load_model('trained_model.h5')

class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
               'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
               'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
               'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
               'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
               'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
               'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 
               'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
               'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 
               'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
               'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 
               'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Load treatments data
treatments_df = pd.read_csv('treatments.csv', encoding='ISO-8859-1')

# Load supplements data
supplements_df = pd.read_csv('suppliments.csv', encoding='ISO-8859-1')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home.html')
def home_page():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        img = image.load_img(filepath, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions)]
        
        # Fetch treatment information
        treatment_info = treatments_df[treatments_df['disease_name'] == predicted_class].iloc[0]
        description = treatment_info['description']
        steps = treatment_info['Possible Steps']
        image_url = treatment_info['image_url']
        
        # Fetch supplement information
        supplement_info = supplements_df[supplements_df['disease_name'] == predicted_class].iloc[0]
        fertilizer_recommendation = supplement_info['supplement name']
        fertilizer_image = supplement_info['supplement image']
        fertilizer_link = supplement_info['buy link']
        
        os.remove(filepath)  # Remove the file after prediction
        return render_template('result.html', prediction=predicted_class, description=description, steps=steps, 
                               image_url=image_url, fertilizer_recommendation=fertilizer_recommendation,
                               fertilizer_image=fertilizer_image, fertilizer_link=fertilizer_link)
    return redirect(url_for('home'))

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
