import os
import base64
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from processor import Processor
from threading import Thread
from flask import send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # CORS 활성화

UPLOAD_FOLDER = "input_sounds"
RESULTS_FOLDER = "results"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULTS_FOLDER"] = RESULTS_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

# 작업 상태 저장
tasks = {}

def background_task(task_id, file_path):
    """Processor 작업을 백그라운드에서 처리"""
    processor = Processor(file_path)
    try:
        processor.process()
        result = processor.run_model()

        if not result:
            tasks[task_id] = {"status": "failed", "error": "Processing failed or no results"}
            return

        results = []
        spectrogram_folder = os.path.join("processing/spectrograms", file_path)

        for spectrogram_name, predicted_class, prediction_all in result:
            spectrogram_path = os.path.join(spectrogram_folder, spectrogram_name)

            with open(spectrogram_path, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

            # if hasattr(prediction_all, "tolist"):  # 텐서인지 확인
            #     prediction_all = prediction_all.tolist()

            prediction_all_numbers = [float(value) for value in prediction_all]

            results.append({"predicted_class": predicted_class, "image": encoded_image, "prediction_all" : prediction_all_numbers})

        tasks[task_id] = {
            "status": "completed",
            "results": results,
            "filename": file_path
        }
    except Exception as e:
        tasks[task_id] = {"status": "failed", "error": str(e)}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 저장할 원래 파일 이름
    original_name = file.filename
    secure_name = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_name)
    file.save(file_path)

    # 작업 ID 생성 및 백그라운드 실행
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "filename": secure_name, "original_filename": original_name}
    thread = Thread(target=background_task, args=(task_id, secure_name))
    thread.start()

    return jsonify({"task_id": task_id}), 202

@app.route('/stream/<filename>', methods=['GET'])
def stream_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    print(f"file_path : {file_path}")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(os.path.abspath(file_path), mimetype='audio/wav')  # 적절한 MIME 타입 설정

@app.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Invalid task ID"}), 404
    return jsonify(task)  # 작업 상태 반환

if __name__ == '__main__':
    app.run(debug=True)
