import cv2
import numpy as np
from flask import Flask, render_template, Response
from mavi1 import MAVI1

mavi:MAVI1 = MAVI1(20, 1, 0.6, target_file='target.jpg')

app = Flask(__name__, template_folder='templates')

def gen_frames():  
    while True:
        pos, success, frame = MAVI1.get_target(MAVI1)  # read the camera frame
        cv2.imshow("Video", frame)
        """if not success:
            break
        else:
            buffer = cv2.imencode('.jpg', frame)[1]
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)