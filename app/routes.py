from flask import render_template, flash, redirect, url_for, request, session, json, make_response
from app import app
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import ntpath
import cv2
import base64
from datetime import datetime
import numpy as np

dropzone = Dropzone(app)
# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


@app.route('/', methods=['POST', 'GET'])
def upload():
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = {}
    # list to hold our uploaded image urls
    file_urls = session['file_urls']

    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)

            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename
            )

            file_urls[filename] = photos.url(filename)
            # print(file_urls)
        session['file_urls'] = file_urls
        session['selected_image_url'] = next(iter(file_urls.values()))

    return render_template('index.html')


@app.route('/filter', defaults={'img_name': None}, methods=['POST', 'GET'])
@app.route('/filter/<img_name>', methods=['POST', 'GET'])
def filter_image(img_name):
    print(img_name)
    print(photos.url(ntpath.basename(request.path)))
    # redirect to home if no images to display
    if "file_urls" not in session:
        return redirect(url_for('upload'))

    if img_name is not None:
        session['selected_image_url'] = photos.url(ntpath.basename(request.path))

    return render_template('filter.html', file_urls=session['file_urls'],
                           selected_image_url=session['selected_image_url'])


@app.route('/processImage', methods=['POST'])
def processImage():
    print(request.form)
    selected_filter = request.form['filters']
    img_to_filter = ntpath.basename(request.form['original'])
    img_name = img_to_filter.split(".")[0]
    img = cv2.imread(os.getcwd() + '/uploads/' + img_to_filter, 0)

    # just a random image for proof of concept
    test_img = np.zeros(img.shape)
    print(test_img)
    retval, buffer = cv2.imencode('.jpg', test_img)
    png_as_text = base64.b64encode(buffer)
    response = make_response(png_as_text)
    response.headers['Content-Type'] = 'image/jpg'

    return response
