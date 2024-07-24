from flask import Flask, request, jsonify, send_file, send_from_directory
from pdf2image import convert_from_path
import os
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['CONVERTED_FOLDER'] = 'converted/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure the upload and converted folders exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['CONVERTED_FOLDER']):
    os.makedirs(app.config['CONVERTED_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def hash_file(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha1.update(chunk)
    return sha1.hexdigest()


@app.route('/')
def upload_page():
    return send_from_directory('static', 'upload.html')


@app.route('/img/<string:hash>/<int:page>.png')
def download_png(hash, page):
    png_path = os.path.join(app.config['CONVERTED_FOLDER'], hash, f"{page}.png")
    if os.path.exists(png_path):
        return send_file(png_path, mimetype='image/png')
    return jsonify({'error': 'File not found'}), 404


@app.route('/conv', methods=['POST'])
def convert_pdf_to_png():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        try:
            images = convert_from_path(pdf_path)
            if len(images) > 0:
                file_hash = hash_file(pdf_path)
                png_path = os.path.join(app.config['CONVERTED_FOLDER'], file_hash)
                os.makedirs(png_path, exist_ok=True)
                for i, image in enumerate(images):
                    image.save(os.path.join(png_path, f"{i}.png"), "PNG")
                return jsonify({'hash': file_hash, 'pages': len(images)}), 200
            else:
                return jsonify({'error': 'PDF conversion failed, no images generated'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(debug=True)
