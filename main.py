from flask import Flask, request, send_file, jsonify, render_template_string
from PIL import Image
import io
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route for HTML frontend
#@app.route('/')
#def index():
#    return render_template_string(HTML_PAGE)  # Use inline HTML string

@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        quality = int(request.form.get('quality', 85))  # Default to 85 if not provided
        if not (1 <= quality <= 100):
            return jsonify({'error': 'Quality must be between 1 and 100'}), 400

        img = Image.open(image_file)

        # Create in-memory bytes buffer
        img_io = io.BytesIO()

        # Compress depending on format
        if img.format == 'JPEG':
            img.save(img_io, format='JPEG', quality=quality, optimize=True)
        elif img.format == 'PNG':
            img.save(img_io, format='PNG', optimize=True)
        else:
            return jsonify({'error': f'Unsupported format: {img.format}'}), 400

        img_io.seek(0)

        # Send file with appropriate mimetype
        return send_file(img_io, mimetype=f'image/{img.format.lower()}')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
