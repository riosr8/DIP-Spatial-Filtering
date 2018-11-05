from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config.update(
    # UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_UPLOAD_MULTIPLE=True,
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=3,
    DROPZONE_REDIRECT_VIEW='filter_image'  # set redirect view
)

from app import routes

