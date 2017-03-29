window.onload = function() {
    //videoタグを取得
    var video = document.getElementById('video');
    //カメラが起動できたかのフラグ
    var localMediaStream = null;
    //カメラ使えるかチェック
    var hasGetUserMedia = function() {
        return (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
    };

    // 動画描画領域のサイズ決定
    //var videoWidth = window.innerWidth;
    //var videoHeight = window.innerWidth / 4 * 3;
    var videoWidth = 600;
    var videoHeight = 450;

    // canvasタグ取得
    var canvas = document.getElementById('canvas');
    canvas.setAttribute("width", videoWidth);
    canvas.setAttribute("height", videoHeight);
    var context = canvas.getContext('2d');

    // Websocket
    var ws = new WebSocket('ws://localhost:5000/echo');
    ws.addEventListener('message', function(e) {
        console.log(e.data.size);
        socketSending = false;
    }, false);
    var socketSending = false;

    //エラー
    var onFailSoHard = function(e) {
        console.log('エラー!', e);
    };

    if(!hasGetUserMedia()) {
        alert("未対応ブラウザです。");
    } else {
        window.URL = window.URL || window.webkitURL;
        navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        navigator.getUserMedia({video: true}, function(stream) {
            video.src = window.URL.createObjectURL(stream);
            localMediaStream = stream;
            video.style.display = 'none';
            video.addEventListener('canplaythrough', function() {
                setInterval(function() {
                    context.drawImage(video, 0, 0, videoWidth, videoHeight);

                    // blob取得
                    if(!socketSending) {
                        var blob = toBlob(canvas);
                        ws.send(blob);
                        socketSending = true;
                    }
                }, 50);
            });
        }, onFailSoHard);
    }

    $("#canvas").click(function() {
        if (localMediaStream) {
            //canvas画像のバイナリー化
            var blob = toBlob(canvas);
        }
    });

    function toBlob(canvas) {
        var base64 = canvas.toDataURL('image/png');
        // Base64からバイナリへ変換
        var bin = atob(base64.replace(/^.*,/, ''));
        var buffer = new Uint8Array(bin.length);
        for (var i = 0; i < bin.length; i++) {
            buffer[i] = bin.charCodeAt(i);
        }
        // Blobを作成
        var blob = new Blob([buffer.buffer], {
            type: 'image/png'
        });
        return blob;
    }
}
