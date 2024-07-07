# Optical-Instrument-Player
Overview
The Optical Instrument Player is a unique musical instrument designed to aid people with physical or cognitive disabilities in creating music. Utilizing eye-tracking technology, this instrument enables users to play piano and drums using only their eye movements.

Features
Eye-Tracking Technology: Integrated using the mediapipe library to track eye movements.
Camera Integration: Achieved using the cv2 library to capture and process real-time video input.
User Interface: Built with the Qt5 library for a seamless and interactive experience.
Musical Instruments: Includes a virtual piano and drums that can be played through eye movements.
Installation
To set up the project locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/addydaipuria/Optical-Instrument-Player.git
cd Optical-Instrument-Player
Install the required libraries:

bash
Copy code
pip install -r requirements.txt
Usage
Running the Application:

bash
Copy code
python main.py
Interacting with the Instrument:

Ensure your webcam is connected and properly configured.
Launch the application and follow the on-screen instructions to calibrate eye-tracking.
Use your eye movements to interact with the virtual piano and drums displayed on the screen.
Libraries and Tools
OpenCV (cv2): Used for camera integration and image processing.
MediaPipe: Utilized for accurate and efficient eye-tracking.
Qt5: Provides the framework for building the graphical user interface.
Development
Survey and Research
We conducted surveys with individuals who have physical or cognitive disabilities to understand their needs and preferences. This feedback was instrumental in designing an accessible and user-friendly musical instrument.

Frontend Development
The frontend of the Optical Instrument Player was developed with a focus on simplicity and usability. The piano and drums are visually represented, and users can interact with these instruments through intuitive eye movements.

Eye Tracking
By leveraging the mediapipe library, we achieved precise eye-tracking, allowing users to play notes on the piano and beats on the drums by simply looking at different parts of the screen.

Camera Integration
The cv2 library is used to integrate the camera feed into the application, providing real-time video input that is processed to track eye movements and translate them into musical notes.

Contributing
We welcome contributions from the community. If you would like to contribute, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
