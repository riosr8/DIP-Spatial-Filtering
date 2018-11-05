from flask import render_template, flash, redirect, url_for, request, session
from app import app
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import ntpath


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


@app.route('/filter', defaults={'img_name': None})
@app.route('/filter/<img_name>')
def filter_image(img_name):
    print(img_name)
    print(photos.url(ntpath.basename(request.path)))
    # redirect to home if no images to display
    if "file_urls" not in session:
        return redirect(url_for('upload'))

    # file_urls = session['file_urls']
    session['selected_image_url'] = photos.url(ntpath.basename(request.path))
    # session.pop('file_urls', None)

    return render_template('filter.html', file_urls=session['file_urls'], selected_image_url=session['selected_image_url'])
