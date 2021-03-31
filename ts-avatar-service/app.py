from flask import Flask, request, jsonify
import numpy as np
import urllib
import cv2
import os
import json
import base64
import traceback

from face_detect import check
from upload import upload_file


app = Flask(__name__)


@app.route('/api/v1/avatar', methods=["POST"])
def hello():
    # receive file
    data = request.get_data().decode('utf-8')
    data = json.loads(data)
    image_b64 = data.get("img")
    if image_b64 is None or len(image_b64) < 1:
        return jsonify({"msg": "need img in request body"}), 400

    try:
        image_decode = base64.b64decode(image_b64)
        nparr = np.fromstring(image_decode, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # if normal, result is a path of file, otherwise its a dict of error message.
        result = check(image)
    except Exception as e:
        return jsonify({"msg": "exception:" + str(traceback.format_exc())}), 500

    if type(result) == dict and result.get("msg") is not None:
        return jsonify(result), 400

    try:
        address = upload_file(result)
    except Exception as e:
        return jsonify({"msg": "exception:" + str(traceback.format_exc())}), 500

    msg = {
        "address": address
    }
    return jsonify(msg), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=17001, debug=True)
