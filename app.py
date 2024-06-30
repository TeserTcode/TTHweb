from flask import Flask, request, send_file, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    with open('main.tth', 'w') as f:
        f.write(text)

    executable_path = os.path.join(os.getcwd(), 'interpeter.exe')

    if os.path.exists('test.bmp'):
        os.remove('test.bmp')

    try:
        result = subprocess.run([executable_path], check=True, capture_output=True, text=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = f"Error running the executable: {e}"
    except FileNotFoundError as e:
        output = f"File not found: {e}"

    bmp_exists = os.path.exists('test.bmp')

    return jsonify({
        'bmp_exists': bmp_exists,
        'output': output
    })

@app.route('/show_picture')
def show_picture():
    if os.path.exists('test.bmp'):
        return send_file('test.bmp', mimetype='image/bmp')
    else:
        return "BMP file not found", 404

@app.route('/example/<filename>')
def example(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
