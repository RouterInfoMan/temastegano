from flask import Flask, render_template, request, send_file, redirect
from PIL import Image
import base64
import io
import stegano

app = Flask(__name__)

last_encoded_img = None
last_decoded_img = None
redirect_string = None

@app.route('/')
def index():
    global redirect_string
    temp = redirect_string
    redirect_string = None
    return render_template('index.html', redirect_string = temp)

@app.route('/image/encode', methods = ['POST', 'GET'])
def image_encode():
    if request.method == "POST":
        message = request.form['message']
        file = request.files['file-encode']
        out_image = stegano.stegano_encrypt(file, message)
        buffer = io.BytesIO()
        # Tell PIL to save as PNG into buffer
        out_image.save(buffer, 'PNG')
        PNG = buffer.getvalue()
        base64_img = base64.b64encode(PNG).decode("utf-8")
        global last_encoded_img
        last_encoded_img = buffer.getvalue()

        return render_template('encode.html', image = base64_img)
    if request.method == "GET":
        return render_template('encode.html', image = None)

@app.route('/image/last/encoded')
def last_encoded():
   if last_encoded_img == None:
       global redirect_string
       redirect_string = "No last encoded image!"
       return redirect('/')
   return send_file(io.BytesIO(last_encoded_img), as_attachment=True, download_name="last_encoded_image.png", mimetype='image/png')


@app.route('/image/decode', methods = ['POST', 'GET'])
def image_decode():
    if request.method == "POST":
        file = request.files['file-decode']
        out = stegano.stegano_decrypt(file)
        img = Image.open(file)
        buffer = io.BytesIO()
        # Tell PIL to save as PNG into buffer
        img.save(buffer, 'PNG')
        PNG = buffer.getvalue()
        global last_decoded_img
        last_decoded_img = PNG
        return render_template('decode.html', mesaj= out)
    if request.method == "GET":
        return render_template('decode.html', mesaj = "")
      
@app.route('/image/last/decoded')
def last_decoded():
    if last_decoded_img == None:
       global redirect_string
       redirect_string = "No last decoded image!"
       return redirect('/')
    return send_file(io.BytesIO(last_decoded_img), as_attachment=True, download_name="last_decoded_image.png", mimetype='image/png')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)