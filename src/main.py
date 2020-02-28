import cv2
from flask import Flask, render_template, Response
from camera import VideoCamera
import threading
import time
import datetime
import os
from upload import upload_images
from notify import send_notif

lock = threading.Lock()

email_update_interval = 20  # sends an email only once in this time interval
video_camera = VideoCamera(flip=False)  # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")  # an opencv classifier

# App Globals (do not edit)
app = Flask(__name__)


def timestamp():
    tstring = datetime.datetime.now()
    print("Filename generated ...")
    return tstring.strftime("%Y%m%d_%H%M%S")


# def upload():
#     dbx = dropbox.Dropbox("FvWjZpwuN3AAAAAAAAAQljaj3x8TkRzxgeUR_5Y3kdRg-232MlZXkOrkxySWIrBn")
#     print(local_file)
#     uploadPath = "C:/Users/Haryanto/Documents/smart-security-camera/" + name_file
#     with open(uploadPath, 'rb') as f:
#         print("Uploading " + name_file + " to Dropbox ...")
#         dbx.files_upload(f.read(), "/" + name_file, mute=True)


def delete(image):
    name_file = image
    print("find file " + name_file + "to delete")
    os.system("rm " + name_file)
    print("File: " + name_file + " deleted ...")


def check_for_object():
    last_epoch = 0
    while True:
        frame, found_object = video_camera.get_frame()
        if found_object and (time.time() - last_epoch) > email_update_interval:
            last_epoch = time.time()
            local_file = timestamp()
            name_file = local_file + ".jpeg"
            video_camera.get_image(local_file)
            upload_images(local_file)
            send_notif(name_file)
            # upload()
            delete(name_file)
            # print(image)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame, found_object = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    t = threading.Thread(target=check_for_object, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
