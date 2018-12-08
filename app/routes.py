"""
This module handles the routes for the Flask application.
"""
import time
import os
import ntpath
import base64
import cv2
from flask import render_template, redirect, url_for, request, session, make_response
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from app import app
from app.smoothing import averaging_yourchoice, gaussian_yourchoice
from app.sharp_image import pos_zero, pos_nonzero, neg_zero, neg_nonzero, hist_equalization
# from app.first_order_filter import prewitt_filter, sobel_filter
from app.first_order_filter import prewitt_filter, sobel_filter
from app.unsharp_mask import unsharp_mask #**

DROPZONE = Dropzone(app)
# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
PHOTOS = UploadSet('photos', IMAGES)
configure_uploads(app, PHOTOS)
patch_request_class(app)  # set maximum file size, default is 16MB

FILTER_DISPATCHER = {'avg_smoothing': averaging_yourchoice,
                     'guass_smoothing': gaussian_yourchoice,
                     'laplacian_pos_zero': pos_zero,
                     'laplacian_pos_nonzero': pos_nonzero,
                     'laplacian_neg_zero': neg_zero,
                     'laplacian_neg_nonzero': neg_nonzero,
                     'first_order_prewitt': prewitt_filter,
                     'first_order_sobel': sobel_filter,
                     'unsharp_mask': unsharp_mask} #**


@app.route('/', methods=['POST', 'GET'])
def upload():
    """
    Handle request to upload files.
    """
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = {}
    # list to hold our uploaded image urls
    file_urls = session['file_urls']

    if request.method == 'POST':
        file_obj = request.files
        for f_obj in file_obj:
            file = request.files.get(f_obj)

            # save the file with to our photos folder
            filename = PHOTOS.save(
                file,
                name=file.filename
            )

            file_urls[filename] = PHOTOS.url(filename)
            # print(file_urls)
        session['file_urls'] = file_urls
        session['selected_image_url'] = next(iter(file_urls.values()))

    return render_template('index.html', file_urls=file_urls)


@app.route('/filter', defaults={'img_name': None}, methods=['POST', 'GET'])
@app.route('/filter/<img_name>', methods=['POST', 'GET'])
def filter_image(img_name):
    """
    Handle request to display the filter page.
    """
    print(img_name)
    print(PHOTOS.url(ntpath.basename(request.path)))
    # redirect to home if no images to display
    if "file_urls" not in session:
        return redirect(url_for('upload'))

    if img_name is not None:
        session['selected_image_url'] = PHOTOS.url(ntpath.basename(request.path))

    return render_template('filter.html', file_urls=session['file_urls'], selected_image_url=session['selected_image_url'])


@app.route('/processImage', methods=['POST'])
def process_image():
    """
    Handle ajax request to filter an image.
    """
    print(request.form)
    selected_filter = request.form.get('filters', 'avg_smoothing')
    mask_size = int(request.form.get('mask_size', 3))
    k_value = float(request.form.get('k_value', 1.0))
    threshold = int(request.form.get('threshold', 1))
    img_to_filter = ntpath.basename(request.form['original'])
    img = cv2.imread(os.getcwd() + '/uploads/' + img_to_filter, 0)
    t0 = time.time()
    if selected_filter in ['first_order_sobel']:
        output = FILTER_DISPATCHER[selected_filter](img, mask_size, threshold)
    elif selected_filter in ['unsharp_mask']:
        output = FILTER_DISPATCHER[selected_filter](img, mask_size, k_value, threshold)
    else:
        output = FILTER_DISPATCHER[selected_filter](img, mask_size)
    t1 = time.time()
    total = t1-t0
    # print(output)
    # prep the filtered image to be sent back as the response
    # retval, buffer = cv2.imencode('.jpg', output[0])
    print('DONE!!!!!')
    print(total)
    retval, buffer = cv2.imencode('.jpg', output)
    png_as_text = base64.b64encode(buffer)
    response = make_response(png_as_text)
    response.headers['Content-Type'] = 'image/jpg'

    return response
