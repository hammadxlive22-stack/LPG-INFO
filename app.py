import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    num = request.args.get("num")

    if not num:
        return jsonify({
            "status": "failed",
            "message": "Mobile number missing! Usage: /?num=9876543210"
        }), 400

    url = "https://apigw.umangapp.in/ioclApi/ws1/consumervalidate"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "subsid": "0",
        "deptid": "186",
        "formtrkr": "0",
        "x-api-key": "VKE9PnbY5k1ZYapR5PyYQ33I26sXTX569Ed7eqyg",
        "srvid": "1123",
        "subsid2": "0",
        "origin": "https://web.umang.gov.in",
        "referer": "https://web.umang.gov.in/"
    }

    payload = {
        "tkn": "dv541a33da-1d3a-4dae-a25e-36e3a56f994f/1",
        "trkr": "213132",
        "lang": "en",
        "lat": "21",
        "lon": "90",
        "lac": "90",
        "usag": "90",
        "apitrkr": "123234",
        "usrid": "09",
        "mode": "web",
        "pltfrm": "android",
        "did": "123234",
        "deptid": "186",
        "formtrkr": "0",
        "srvid": "1123",
        "subsid": "0",
        "subsid2": "0",
        "trackingId": "",
        "source": "UMANG",
        "mobile": str(num),
        "consumerId": "",
        "partnerCode": "",
        "consumerNumber": ""
    }

    try:
        # 10-second timeout to prevent server hanging
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        return jsonify(res.json()), res.status_code
    except requests.exceptions.Timeout:
        return jsonify({"error": "UMANG server didn't respond in time."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Dynamically bind port for cloud platforms like Render/Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
