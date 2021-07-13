import base64
from json import dumps
import json
import os

def jsonify_photos(ENCODING='utf-8',FOLDER_NAME = 'photos',JSON_NAME='output.json'):
    tree = {FOLDER_NAME:[]}
    image_names = [f for f in os.listdir(FOLDER_NAME) if f.endswith('.jpg')]
    for img_name in image_names:
        with open(FOLDER_NAME+'/'+img_name, 'rb') as open_file:
            byte_content = open_file.read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode(ENCODING)
        raw_data = {"ID": img_name,"img_code": base64_string}
        tree[FOLDER_NAME].append(raw_data)
    json_data = dumps(tree, indent=2)
    with open(JSON_NAME, 'w') as file:
        file.write(json_data)

def decode_img(dir_decoded='images',FOLDER_NAME = 'photos',JSON_NAME='output.json',uploaded_file=None):
    if uploaded_file==None:
        with open(JSON_NAME) as f:
            data = json.load(f)
    else:
        data = json.load(uploaded_file)
    if not os.path.isdir(dir_decoded):
        os.mkdir(dir_decoded)
    for img_dict in data[FOLDER_NAME]:
        encoded_img = img_dict["img_code"]
        decoded_img = open(dir_decoded+'/'+img_dict["ID"],'wb')
        decoded_img.write(base64.b64decode((encoded_img)))
        decoded_img.close()
    return data

