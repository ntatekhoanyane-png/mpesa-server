from flask import Flask, request, jsonify
import requests
import base64
import rsa

app = Flask(__name__)

# 🔐 PASTE YOUR VALUES HERE
API_KEY ="hWCyWCPt7uuhzRjdKldIE8KEVInOR66u"


PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ==
PASTE_YOUR_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----"""

SERVICE_PROVIDER_CODE = "000000"

BASE_URL = "https://openapi.m-pesa.com/sandbox/ipg/v2/vodacomLES"

# 🔑 Generate session key
def get_session_key():
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY.encode())
    encrypted = rsa.encrypt(API_KEY.encode(), public_key)
    return base64.b64encode(encrypted).decode()

# 🟢 Home route
@app.route('/')
def home():
    return "M-Pesa Server Running"

# 💸 Payment route
@app.route('/pay', methods=['POST'])
def pay():
    try:
        data = request.json

        phone = data.get("phone")
        amount = data.get("amount")

        session_key = get_session_key()

        headers = {
            "Authorization": f"Bearer {session_key}",
            "Content-Type": "application/json",
            "Origin": "*"
        }

        payload = {
            "input_Amount": "12",
            "input_Country": "LES",
            "input_Currency": "LSL",
            "input_CustomerMSISDN": "26650761947",
            "input_ServiceProviderCode": "000000",
            "input_TransactionReference": "T12344C",
            "input_ThirdPartyReference": "REF123",
            "input_PurchasedItemsDesc": "Shopify Payment"
        }

        response = requests.post(
            f"{openapi.m-pesa.com/sandbox/ipg/v2/vodacomLES/c2bPayment/singleStage/",
            json=payload,
            headers=headers
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
