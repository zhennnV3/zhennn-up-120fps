from flask import Flask, request, render_template, send_file
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proses', methods=['POST'])
def proses_video():
    video = request.files['video']
    input_path = os.path.join(UPLOAD_FOLDER, video.filename)
    output_path = os.path.join(OUTPUT_FOLDER, 'hd_120fps_' + video.filename)

    video.save(input_path)

    # FFmpeg: 1080x1920, 120fps, bitrate tinggi
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
        '-c:v', 'libx264',
        '-b:v', '50M',
        '-preset', 'slow',
        '-r', '120',
        '-c:a', 'aac',
        '-b:a', '192k',
        output_path
    ]
    subprocess.run(cmd, check=True)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)