window.onload = function() {
    var ws = new WebSocket('ws://' + window.location.host + '/download');

    var socketSending = false;
    ws.addEventListener('message', function(e) {
        var binary = e.data;

        if(binary.size) {
            var blob = new Blob([binary], {type: 'image/jpeg'});
            var img = document.getElementById("image");
            img.src = URL.createObjectURL(blob);
        }

        socketSending = false;
        //context.drawImage(video, 0, 0, videoWidth, videoHeight);
    }, false);

    ws.addEventListener('open', function(e) {
        setInterval(function() {
            if(!socketSending) {
                ws.send(1);
                socketSending = true;
            }
        }, 50);
    }, false);
}
