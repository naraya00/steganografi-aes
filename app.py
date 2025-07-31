from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from stegano_aes import encode_message, decode_message

app = Flask(__name__)

# Konfigurasi folder upload dengan path absolut
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Buat folder jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['image']
    message = request.form['message']
    password = request.form['password']

    if image.filename == '':
        return render_template('index.html', decoded_message='Tidak ada gambar yang dipilih.')

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    stego_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'stego_' + filename)

    try:
        encode_message(image_path, stego_image_path, message, password)
        return render_template('index.html', stego_image='uploads/stego_' + filename)
    except Exception as e:
        return render_template('index.html', decoded_message='Gagal encode: ' + str(e))

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['image']
    password = request.form['password']

    if image.filename == '':
        return render_template('index.html', decoded_message='Tidak ada gambar yang dipilih.')

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    try:
        extracted_message = decode_message(image_path, password)
        return render_template('index.html', decoded_message=extracted_message)
    except Exception as e:
        return render_template('index.html', decoded_message='Gagal dekripsi: ' + str(e))

if __name__ == '__main__':
    app.run(debug=True)
