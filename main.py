from flask import Flask, render_template, redirect, request, session, url_for
import json
import base64, codecs, requests, qrcode
from addInvoice import add_invoice
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import os

app = Flask(__name__, static_folder='static')

load_dotenv()

REST_HOST = os.getenv('REST_HOST')
MACAROON_PATH = os.getenv('MACAROON_PATH')
TLS_PATH = os.getenv('TLS_PATH')

url = f'https://{REST_HOST}/v1/invoices'
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Meatadata-macaroon': macaroon}

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)


@app.route('/', methods=['POST', 'GET'])
def hello():

    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        amount = request.form['amount']
        if name == '' or desc == '' or amount == '':
            return render_template('index.html')
        message = add_invoice(desc, amount)
        qr.add_data(message)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        now = str(datetime.now())
        img_name = 'static/qr_invoices/'+name+now+'.png'
        img.save(img_name)
        messages = json.dumps({'invoice': message, 'qr': img_name})
        return redirect(url_for('.invoice', messages=messages))


@app.route('/invoice')
def invoice():

    messages = request.args.get('messages')
    messages = json.loads(messages)
    p_invoice = messages['invoice']
    qr_ = messages['qr']
    return render_template("invoice.html", p_invoice=p_invoice, qr=qr_)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
