from flask import Flask, Response
import cv2
import time
from threading import Thread

app = Flask(__name__)

class ImageGenerator:
    def __init__(self):
        self.image_paths = ['C:/projects/rtsp/images/10.jpg', 'C:/projects/rtsp/images/9.jpg', 'C:/projects/rtsp/images/7.jpg', 'C:/projects/rtsp/images/6.jpg', 'C:/projects/rtsp/images/5.jpg', 'C:/projects/rtsp/images/4.jpg', 'C:/projects/rtsp/images/3.jpg']
        self.num_images = len(self.image_paths)
        self.current_image_index = 0
        self.images = [cv2.imread(image_path) for image_path in self.image_paths]

    def load_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % self.num_images
        return cv2.imread(self.image_paths[self.current_image_index])

    def switch_images(self):
        while True:
            time.sleep(5)
            self.load_next_image()

    def generate(self):
        while True:
            # Load the current image
            img = self.images[self.current_image_index]

            # Encode the image to JPEG
            _, jpeg = cv2.imencode('.jpg', img)

            # Convert JPEG to bytes
            frame = jpeg.tobytes()

            # Yield the frame for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Global variable for the image generator
generator = ImageGenerator()

# Create a separate thread for image switching
switch_thread = Thread(target=generator.switch_images)
switch_thread.start()

@app.route('/video_feed')
def video_feed():
    return Response(generator.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
