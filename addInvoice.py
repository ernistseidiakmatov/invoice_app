import base64, codecs, json, requests
from dotenv import load_dotenv, dotenv_values
import os


load_dotenv()

REST_HOST = os.getenv('REST_HOST')
MACAROON_PATH = os.getenv('MACAROON_PATH')
TLS_PATH = os.getenv('TLS_PATH')
url = f'https://{REST_HOST}/v1/invoices'
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon}

def add_invoice(memo, value):
        data = {'memo': memo, 'value': value}
        r = requests.post(url, headers=headers, data=json.dumps(data),verify=TLS_PATH)
        return r.json()['payment_request']
