from __future__ import print_function
import os
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
import shutil
import re
import base64
import cv2
import numpy as np
import pandas as pd
import predict

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "D:\\Final_project_flask\\static\\upload_image"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["RESULT"] = "D:\\Final_project_flask\\submit"
app.config["FINISH"] = "D:\\Final_project_flask\static\\finish"

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print("image", image)
            print("image name", image.filename)

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image saved")
                return redirect(url_for("predict",filename=filename))

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("index.html")


@app.route("/predict/<filename>", methods=["GET"])
def predict(filename):
    cmd_line = f'''python predict.py static/upload_image/{filename}'''
    print(cmd_line)
    os.system(cmd_line)
    shutil.move(os.path.join(app.config["RESULT"], filename), os.path.join(app.config["FINISH"], filename))
    return render_template('result.html', filename=filename)

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug= True)