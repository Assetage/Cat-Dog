import base64
from json import dumps
import json
import os
from keras.preprocessing import image
from keras.models import load_model
import pandas as pd
import numpy as np
from utils import *
import streamlit as st
import time

# making the current directory our working one
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# place the main title
st.title('Cat-Dog classification')
# initiate the select box between the default json and the custom one
option1 = st.sidebar.selectbox(
    'Choose JSON file',
    ('Default file','Upload file'))
st.write('You selected:', option1)

# once the one file is chosen, the following lines will generate images from the base64 encoded strings
# both for default and custom json
if option1 == 'Upload file':
    uploaded_file = st.sidebar.file_uploader("Please upload the file")
    if uploaded_file:
        st.success("You successfully uploaded the file")
        st.markdown("The uploaded json:")
        up_file = decode_img(uploaded_file=uploaded_file)
        st.write(up_file)
elif option1 == "Default file":
    jsonify_photos()
    st.markdown("The default json:")
    default_file = decode_img(uploaded_file=None)
    st.write(default_file)

# if the user is ready for the next step, we could proceed with making predictions
if st.button("Continue classifying images"):
    ENCODING = 'utf-8'
    FOLDER_NAME = 'images'
    JSON_NAME = 'results.json'
    results = {"Results":[]}
    counter = 1
    model = load_model('model.h5')
    df = pd.DataFrame()
    preds = []
    trues = []
    dogs = []
    cats = []

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    image_names = [f for f in os.listdir(FOLDER_NAME) if f.endswith('.jpg')]
    for img_name in image_names:
        iter = int(counter/len(image_names) * 100)
        latest_iteration.text(f'Please wait! Progress: {iter}%')
        bar.progress(iter)
        time.sleep(0.1)
        test_image = image.load_img(FOLDER_NAME+'/'+img_name, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)

        dog_prob = result[0][1]
        cat_prob = result[0][0]
        if cat_prob > dog_prob:
            prediction = 'cat'
        else:
            prediction = 'dog'

        preds.append(prediction)
        trues.append(img_name.split('.')[0])
        dogs.append(dog_prob)
        cats.append(cat_prob)
        store_data = {"ID": img_name,"cat_prob": str(np.round(cat_prob,3)),"dog_prob":str(np.round(dog_prob,3))}

        results["Results"].append(store_data)
        print(str(counter),'/',str(len(image_names)))
        counter+=1
    # creating a json file from a dictionary with predictions
    json_results = dumps(results, indent=2)
    with open(JSON_NAME, 'w') as results_file:
        results_file.write(json_results)
    # filling the dataframe with information
    df["ID"] = image_names
    df["Predictions"] = preds
    df["Dog_prob"] = dogs
    df["Cat_prob"] = cats
    df["Trues"] = trues
    true_bin = [1 if i==j else 0 for i,j in zip(preds,trues)]

    df['True_bin'] = true_bin
    # creating a raw excel file with predictions for further analysis
    df.to_excel("output_excel.xlsx")
    st.success("The output excel file has been created")

    # printing the part of the resulting json
    st.markdown("A part of the resulting JSON:")
    st.write(results["Results"][0:5])