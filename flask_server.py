from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from werkzeug.exceptions import abort
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/echo')
def echo():
    # environ['wsgi.websocket'] から WebSocket オブジェクトが得られる
    ws = request.environ['wsgi.websocket']
    if not ws:
        abort(400)

    while True:
        # 入力うけつけ
        binary_array = ws.receive()  

        data = np.fromstring(bytes(binary_array), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
        cv2.imshow("some window", img)
        cv2.waitKey(1)

        # 入力をエコーバックする
        ws.send(1)

if __name__ == '__main__':
    # WebSocketHandler が environ['wsgi.websocket'] をセットする
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
