from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result = subprocess.run(
                ['python', 'predict_video.py', '--input', filepath],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            return f"<h3>Error in video analysis:</h3><pre>{e.stderr}</pre>"
            
        output_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        # Validate output format
        if len(output_lines) < 3:
            return f"""<h3>Invalid analysis output format</h3>
                      <p>Expected 3 result lines, got {len(output_lines)}:</p>
                      <pre>{result.stdout}</pre>"""
        
        try:
           
            total_frames = output_lines[-3].split(": ")[1].strip()
            suspicious_frames = output_lines[-2].split(": ")[1].strip()
            percentage = output_lines[-1].split(": ")[1].strip()
            
            results = {
                'video_path': filename,
                'total_frames': total_frames,
                'suspicious_frames': suspicious_frames,
                'percentage': percentage
            }
            
        except Exception as e:
            return f"""<h3>Error parsing results</h3>
                      <p>{str(e)}</p>
                      <pre>Full output:\n{result.stdout}</pre>"""
        
        return render_template('results.html', results=results)
    
    return redirect(request.url)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)