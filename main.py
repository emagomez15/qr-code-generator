
from flask import Flask, render_template, request
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generateQR():
    memory = BytesIO()
    link = request.form.get('link')
    bcolor = request.form.get('bcolor')
    fcolor = request.form.get('fcolor')
    
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=15,
                       border=1)

    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fcolor, back_color=bcolor)
    img.save(memory)

    memory.seek(0)

    base64_img = "data:image/png;base64," + \
        b64encode(memory.getvalue()).decode('ascii')

    return render_template('index.html', link=base64_img)

if __name__ == '__main__':
    app.run(debug=True)