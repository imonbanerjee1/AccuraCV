from flask import Flask

app = Flask(__name__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

import os
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


from app import routes