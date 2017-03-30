from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template
from werkzeug.exceptions import abort
from chainer import serializers, Variable
import chainer.functions as F
from yolov2_darknet_predict import CocoPredictor
import pdb
import numpy as np
import cv2

app = Flask(__name__)
app.static_folder = 'static'
img = None
#coco_predictor = CocoPredictor()

@app.route('/')
def index():
    return render_template('index.html', titlename="camera")

@app.route('/view')
def view():
    return render_template('view.html', titlename="view")

@app.route('/download')
def download():
    global img
    ws = request.environ['wsgi.websocket']
    if not ws:
        abort(400)

    while True:
        data = ws.receive()
        if img is None:
            ws.send(False)
        else:
            binary_array = bytearray(cv2.imencode('.jpeg', img)[1].tobytes())
            ws.send(binary_array)
            print("send", len(binary_array))

@app.route('/upload')
def upload():
    global img

    # environ['wsgi.websocket'] から WebSocket オブジェクトが得られる
    ws = request.environ['wsgi.websocket']
    if not ws:
        abort(400)

    while True:
        # 入力うけつけ
        binary_array = ws.receive()  
        print("receive", len(binary_array))
        data = np.fromstring(bytes(binary_array), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        '''
        nms_results = coco_predictor(img)
        for result in nms_results:
            left, top = result["box"].int_left_top()
            right, bottom = result["box"].int_right_bottom()
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 5)
            text = '%s(%2d%%)' % (result["label"], result["probs"].max()*result["conf"]*100)
            cv2.putText(img, text, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
            print(text)
        '''

        #cv2.imshow("w", img)
        cv2.waitKey(1)

        #cv2.imwrite("result.jpg", img)

        # 入力をエコーバックする
        ws.send(1)

if __name__ == '__main__':
    # WebSocketHandler が environ['wsgi.websocket'] をセットする
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
