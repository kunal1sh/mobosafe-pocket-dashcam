# 🚗 MoboSafe Pocket Dashcam - Dual-Feed Smart Client

A lightweight edge streaming dashcam application engineered for the **MoboSafe Pocket Dashcam Challenge**. The system captures dual synchronized feeds (Road/Front & Cabin/Rear) with live audio, renders HUD telemetry overlays, prevents mobile screen timeout, and streams low-latency feeds via RTMP.

---

## 📌 Features & Architecture

* **Dual-View Ingestion**: Simultaneous 1080p @ 30fps capture from Road (environment) and Cabin (user) perspectives.
* **Audio Pipeline**: Hardware microphone capture encoded into synchronized stereo AAC/Opus streams.
* **HUD Telemetry**: Real-time overlays for timestamps, live status, and student roll number metadata.
* **Screen WakeLock**: Integrated Wake Lock API preventing mobile screen dimming or timeout during active capture.
* **Direct RTMP Transport**: Pre-configured pipelines routing to `rtmp://15.207.177.194:1936/hackathon/`.

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
* Python 3.9+ and FFmpeg installed in system `PATH`
* Dependencies:
```bash
pip install flask pyopenssl opencv-python

2. Run the Edge Server
Bash
python app.py
The server binds to 0.0.0.0:3000 with local SSL enabled.

Mobile Device (Android / iOS) Setup
Network Sync: Connect both phone and laptop to the same Wi-Fi or mobile hotspot.

Retrieve Laptop IP:

Open Command Prompt on Windows, run ipconfig.

Locate the active IPv4 Address under your adapter (e.g., 192.168.1.33).

Open Mobile Client:

On mobile Chrome/Safari, navigate to:

https://<LAPTOP_LOCAL_IP>:3000

Accept Certificate & Permissions:

Tap Advanced → Proceed (unsafe) to accept the self-signed certificate.

Tap Allow for Camera and Microphone prompts.

Start Stream: Tap ▶ START DUAL STREAM to activate cameras and begin live transmission.

Edge Challenges & Troubleshooting
1. Mobile Camera Access Blocked (getUserMedia Undefined)
Cause: Modern mobile browsers restrict hardware access strictly to Secure Contexts (https:// or localhost).

Fix: Enabled Flask ad-hoc SSL (ssl_context='adhoc') via pyopenssl, allowing mobile devices to access camera hardware over the local network.

2. SSL Protocol Mismatch on HTTP Port
Cause: Sending HTTPS requests to an HTTP-only socket caused TLS handshake failure and raw byte errors (\x16\x03\x01...).

Fix: Configured SSL at the transport layer on port 3000 to complete handshakes seamlessly.

3. Server Ingestion & Stream Mapping
Cause: Root API /api/session returned HTTP 401 Unauthorized.

Fix: Bypassed redundant session authentications by directly piping streams to the RTMP ingestion port (:1936):

Road Feed: rtmp://15.207.177.194:1936/hackathon/btech2519523_front

Cabin Feed: rtmp://15.207.177.194:1936/hackathon/btech2519523_back

👨‍💻 Submission Info
Roll Number: btech2519523

Repository: mobosafe-pocket-dashcam