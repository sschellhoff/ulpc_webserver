from flask import Flask, send_from_directory, jsonify, make_response
import os

img_path = "img"
img_file_ending = ".jpg"

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/" + img_path + "/<path:path>")
def send_img(path):
    return send_from_directory(img_path, path)

@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory('js', path)

@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory('css', path)

@app.route("/images")
def get_images():
    paths = get_image_paths()
    json_data = jsonify(paths)
    response = make_response(json_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def get_last_image_path():
    image_paths = get_image_paths()
    if len(image_paths) == 0:
        return ""

    image_paths.sort(reverse=True)
    return image_paths[0]

def get_image_paths():
    filepaths = []
    for file in os.listdir(img_path):
        if file.endswith(img_file_ending):
            filepaths.append(os.path.join(img_path, file))
    return sorted(filepaths)
