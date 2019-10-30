from flask import Flask, send_from_directory
import os
import json

img_path = "img"
img_file_ending = ".jpg"

static_path = "static"
scripts_path = os.path.join(static_path, "js")
styles_path = os.path.join(static_path, "css")

index_file_name = "index.html"
script_file_name = "script.js"
style_file_name = "style.css"

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(static_path, index_file_name)

@app.route("/" + script_file_name)
def send_script():
    return send_from_directory(scripts_path, script_file_name)

@app.route("/" + style_file_name)
def send_style():
    return send_from_directory(styles_path, style_file_name)

@app.route("/" + img_path + "/<path:path>")
def send_img(path):
    return send_from_directory(img_path, path)

@app.route("/images")
def get_images():
    return json.dumps(get_image_paths())

def get_last_image_path():
    image_paths = get_image_paths()
    if len(image_paths) == 0:
        return ""

    return image_paths[0]

def get_image_paths():
    filepaths = []
    for file in os.listdir(img_path):
        if file.endswith(img_file_ending):
            filepaths.append(os.path.join(img_path, file))
    filepaths.sort(reverse=True)
    return filepaths

