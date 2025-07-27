from flask import Flask, request, jsonify, send_from_directory
import subprocess

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/run-core', methods=['POST'])
def run_core():
    try:
        result = subprocess.run(['python', 'core.py'], capture_output=True, text=True)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
