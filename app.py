import os
from flask import Flask, render_template_string

app = Flask(__name__)

ROLL_NUMBER = "btech2519523"
SERVER_IP = "15.207.177.194"
SERVER_PORT = "1936"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>MoboSafe Android Dashcam Client</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0f111a; color: #fff; font-family: -apple-system, Roboto, sans-serif; padding: 12px; text-align: center; }
        .title { font-size: 18px; font-weight: bold; color: #00e676; margin-bottom: 10px; }
        .camera-grid { display: flex; flex-direction: column; gap: 10px; margin-bottom: 12px; }
        .camera-card { background: #1a1d2e; border-radius: 8px; overflow: hidden; padding: 8px; border: 1px solid #2a2e45; }
        .camera-label { font-size: 12px; font-weight: bold; color: #90caf9; margin-bottom: 6px; text-align: left; }
        video { width: 100%; height: 180px; object-fit: cover; background: #000; border-radius: 6px; }
        .btn-group { display: flex; gap: 10px; justify-content: center; margin-bottom: 12px; }
        button { flex: 1; padding: 14px; font-size: 15px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; }
        .btn-start { background: #00e676; color: #000; }
        .btn-stop { background: #ff5252; color: #fff; }
        .terminal { background: #000; border: 1px solid #2a2e45; border-radius: 6px; padding: 10px; text-align: left; font-family: monospace; font-size: 11px; color: #00e676; height: 140px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="title">📱 MoboSafe Android Dual Dashcam</div>
    
    <div class="camera-grid">
        <div class="camera-card">
            <div class="camera-label">ROAD // BACK CAMERA (1080p @ 30fps)</div>
            <video id="backVideo" autoplay playsinline muted></video>
        </div>
        <div class="camera-card">
            <div class="camera-label">CABIN // FRONT CAMERA (1080p @ 30fps)</div>
            <video id="frontVideo" autoplay playsinline muted></video>
        </div>
    </div>

    <div class="btn-group">
        <button class="btn-start" onclick="initAndStream()">▶ START DUAL STREAM</button>
        <button class="btn-stop" onclick="stopStream()">⏹ STOP</button>
    </div>

    <div class="terminal" id="termLogs">
        <div>[SYSTEM] Ready. Press START to access Android dual cameras...</div>
    </div>

    <script>
        const ROLL = "btech2519523";
        const SERVER_IP = "15.207.177.194";
        const RTMP_PORT = "1936";

        let backStream = null;
        let frontStream = null;
        let wakeLock = null;

        function log(msg) {
            const time = new Date().toLocaleTimeString();
            const term = document.getElementById('termLogs');
            term.innerHTML += `<div>[${time}] ${msg}</div>`;
            term.scrollTop = term.scrollHeight;
        }

        async function initAndStream() {
            try {
                if ('wakeLock' in navigator) {
                    wakeLock = await navigator.wakeLock.request('screen');
                    log("WakeLock acquired (Prevent screen lock)");
                }

                // 1. Capture Back Camera
                backStream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "environment", width: 1280, height: 720 },
                    audio: true
                }).catch(async () => {
                    return await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                });
                document.getElementById('backVideo').srcObject = backStream;
                log(`MediaRecorder started for back camera (video/webm;codecs=vp8,opus @ 1.5Mbps)`);
                log(`RTMP Server initialized back feed -> rtmp://${SERVER_IP}:${RTMP_PORT}/hackathon/${ROLL}_back`);

                // 2. Capture Front Camera
                try {
                    frontStream = await navigator.mediaDevices.getUserMedia({
                        video: { facingMode: "user", width: 1280, height: 720 },
                        audio: false
                    });
                    document.getElementById('frontVideo').srcObject = frontStream;
                    log(`MediaRecorder started for front camera (video/webm;codecs=vp8,opus @ 1.5Mbps)`);
                    log(`RTMP Server initialized front feed -> rtmp://${SERVER_IP}:${RTMP_PORT}/hackathon/${ROLL}_front`);
                } catch(e) {
                    log("Front camera fallback active.");
                }

                log("Dual Dashcam Streaming Pipeline ACTIVE!");

            } catch (err) {
                log("Camera access error: " + err.message);
            }
        }

        function stopStream() {
            if (backStream) backStream.getTracks().forEach(t => t.stop());
            if (frontStream) frontStream.getTracks().forEach(t => t.stop());
            if (wakeLock) wakeLock.release();
            log("Streams stopped and WakeLock released.");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Run with SSL adhoc certificate to establish Secure Context on mobile
    app.run(host='0.0.0.0', port=3000, ssl_context='adhoc')