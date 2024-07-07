import cv2
import mediapipe as mp
from PyQt5.QtCore import Qt, QTimer, QUrl, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
import os
import pyautogui
import sys
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

class LiveServerPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if isMainFrame and url.scheme() == "http":
            return True
        return super().acceptNavigationRequest(url, _type, isMainFrame)

class HttpServerThread(QThread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        handler = SimpleHTTPRequestHandler
        with TCPServer(("localhost", self.port), handler) as httpd:
            print(f"Serving at port {self.port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        print(script_dir)
        html_file_path = os.path.join(script_dir,"index.html")

        self.live_server_port = 8000  # Choose any available port

        # Start the local server in a separate thread
        self.server_thread = HttpServerThread(self.live_server_port)
        self.server_thread.start()

        self.html_view = QWebEngineView(self)
        self.page = LiveServerPage(self.html_view)
        self.html_view.setPage(self.page)
        self.html_view.setUrl(QUrl(f"http://localhost:{self.live_server_port}"))

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout(self.central_widget)

        self.html_view.setFixedHeight(820)
        self.video_label.setFixedHeight(180)

        self.layout.addWidget(self.html_view)

        camera_button_layout = QHBoxLayout()

        button_layout = QVBoxLayout()
        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedHeight(60)
        self.start_button.clicked.connect(self.start_capture)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setFixedHeight(60)
        self.stop_button.clicked.connect(self.stop_capture)
        button_layout.addWidget(self.stop_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFixedHeight(60)
        self.exit_button.clicked.connect(self.exit_app)
        button_layout.addWidget(self.exit_button)

        camera_button_layout.addLayout(button_layout)

        camera_button_layout.addWidget(self.video_label)

        self.layout.addLayout(camera_button_layout)

        self.cam = cv2.VideoCapture(0)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)

        self.screen_w, self.screen_h = pyautogui.size()

    def start_capture(self):
        self.timer.start(30)

    def stop_capture(self):
        self.timer.stop()

    def update_video(self):
        ret, frame = self.cam.read()
        if not ret:
            print("Exit")
            return
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = self.face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = self.screen_w * landmark.x
                    screen_y = self.screen_h * landmark.y
                    print(landmark.x, landmark.y)
                    pyautogui.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.01:
                pyautogui.click()
                print("Button Clicked")
                pyautogui.sleep(1)

        frame = cv2.resize(frame, (240, 180))
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(pixmap)

    def exit_app(self):
        if self.cam.isOpened():
            self.cam.release()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
