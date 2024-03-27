# app.py
from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from yolov5 import YOLOv5
import cv2
import os
import base64
from datetime import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
db = SQLAlchemy(app)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100), nullable=False)
    result_filename = db.Column(db.String(100), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'<Result {self.original_filename} -> {self.result_filename}>'
    
model = YOLOv5("yolov5x.pt", device="cpu")


@app.route('/')
def index():
    results_history = Result.query.order_by(Result.upload_time.desc()).all()
    return render_template('index.html', results_history=results_history)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Обработка изображения

        img = cv2.imread(file_path)
        results = model.predict(img)
        result_filename = f"result_{filename}"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        cv2.imwrite(result_path, results.render()[0])

        # Сохранение информации о результате в базе данных

        new_result = Result(original_filename=filename, result_filename=result_filename)
        db.session.add(new_result)
        db.session.commit()

        # Кодирование изображения в Base64

        with open(result_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return jsonify({'image': encoded_image, 'result_filename': result_filename, 'upload_time': new_result.upload_time.strftime('%Y-%m-%d %H:%M:%S')})


@app.route('/result/<filename>')
def result(filename):
    return send_file(os.path.join(app.config['RESULTS_FOLDER'], filename), mimetype='image/jpeg')


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['RESULTS_FOLDER']):
        os.makedirs(app.config['RESULTS_FOLDER'])
    with app.app_context():
        db.create_all()
    app.run(debug=True)
