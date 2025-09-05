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
  - `mediapipe`
  - `opencv-python`
  - `numpy`
  - `pyserial`

Install them with:
```bash
pip install mediapipe opencv-python numpy pyserial
