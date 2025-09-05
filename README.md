# Gesture-Controlled Robotic Arm

A robotic arm controlled in real time using **MediaPipe** (Python) for human pose and hand gesture tracking, and **Arduino** for servo actuation. The system maps body and hand movements to the robotic arm’s joints, allowing intuitive, camera-based control without physical joysticks.

---

## Features
- 🎥 **Real-time tracking** using MediaPipe Holistic (pose + hand landmarks).  
- 🤖 **Servo control** via Arduino for claw, base, and arm joints.  
- 🔗 **Serial communication** between Python and Arduino.  
- 📏 Smoothed movement using moving averages for stable control.  
- 🖐 Gesture-based claw control (thumb + index finger distance).  

---

## Requirements

### Python Side
- Python 3.8+
- Libraries:
  - mediapipe
  - opencv-python
  - numpy
  - pyserial

Install them with:
```bash
pip install mediapipe opencv-python numpy pyserial
```

### Arduino Side
- Arduino IDE
- Servo library (`#include <Servo.h>`) – comes pre-installed with the IDE.

---

## Hardware Setup
- Arduino board (e.g., UNO/Nano/MEGA).  
- Servos connected to pins:
  - Claw → Pin 11  
  - Right Servo → Pin 10  
  - Left Servo → Pin 6  
  - Base Servo → Pin 5  
- Webcam or laptop camera for gesture tracking.  

---

## Usage

1. Upload the Arduino sketch (`arduino/robotic_arm.ino`) to your Arduino.  
2. Run the Python script (`python/gesture_control.py`).  
3. Make sure the correct COM port is set in the Python file:
   ```python
   arduino = serial.Serial("COM9", 9600)
   ```
   Adjust `"COM9"` as needed for your setup.  
4. Move your arm and hand in front of the camera — the robotic arm will follow.  

---

## Project Structure
```
.
├── main.py   # MediaPipe + OpenCV tracking, sends data to Arduino
├── roboticarmcv.ino      # Arduino sketch controlling servos



## License
This project is open-source and available under the **MIT License**.  

---
## Author
git-hub: [github.com/abelbajeh]
contact: [chidejohn63@gmail.com]


## Author
Developed by [Your Name].
