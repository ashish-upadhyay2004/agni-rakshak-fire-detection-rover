# Agni Rakshak – Autonomous Forest Fire Detection Rover

<img width="864" height="1227" alt="rover4" src="https://github.com/user-attachments/assets/9b52a62b-4195-4946-a5be-0d84fec0bf07" />
<img width="1280" height="960" alt="rover3" src="https://github.com/user-attachments/assets/ce248d96-c73d-4595-b5d4-383d565656c8" />
<img width="1280" height="960" alt="rover2" src="https://github.com/user-attachments/assets/cb9b0723-fb8d-4383-baeb-2fe9ae1b83aa" />
<img width="960" height="1280" alt="roverimage" src="https://github.com/user-attachments/assets/f0a3936d-7b98-4781-94af-2df4bc1b64a1" />



## Overview

Agni Rakshak is an autonomous forest fire detection and response rover developed to support early wildfire identification and mitigation. The system combines computer vision, embedded systems, robotics, and IoT technologies to detect fire in real time, navigate autonomously, avoid obstacles, and communicate with external systems.

The project was developed as a major academic project with the objective of exploring practical applications of AI and robotics in environmental protection.

---

## Features

* Real-time fire detection using computer vision
* Autonomous navigation and decision making
* Obstacle detection and avoidance
* ESP32-based hardware control
* Wireless communication between modules
* Real-time monitoring and alert generation
* Modular software architecture for scalability

---

## System Architecture

```text
Camera Module
      │
      ▼
Fire Detection Engine
      │
      ▼
Decision Logic
      │
      ├────────► Motor Control
      │
      ├────────► Obstacle Avoidance
      │
      └────────► Alert System
```

---

## Technologies Used

### Programming

* Python

### Computer Vision

* OpenCV
* YOLO-based Fire Detection

### Hardware

* ESP32
* Camera Module
* Ultrasonic Sensors
* Motor Drivers
* DC Motors

### Software Engineering

* Object-Oriented Design
* Modular Architecture
* Automated Testing

---

## Project Structure

```text
agni-rakshak-fire-detection-rover
│
├── actuators/
├── logic/
├── sensors/
├── utils/
├── logs/
├── runs/
│
├── config.py
├── decisions.py
├── esp32_connection.py
├── main.py
│
├── test.py
├── test_flow.py
├── test_fire_detection.py
├── test_ir_sensor.py
└── test_actuators.py
```

---

## Key Components

### Fire Detection Module

Detects potential fire hazards using computer vision techniques and triggers emergency actions when fire is identified.

### Navigation System

Processes sensor data and determines rover movement decisions.

### Obstacle Avoidance

Uses sensor inputs to avoid collisions while navigating autonomous routes.

### ESP32 Communication Layer

Handles communication between the control software and embedded hardware components.

### Decision Engine

Coordinates information from sensors and detection modules to determine rover actions.

---

## Applications

* Forest fire monitoring
* Disaster prevention systems
* Environmental monitoring
* Autonomous inspection systems
* Smart agriculture monitoring

---

## Future Improvements

* GPS-based location tracking
* Cloud dashboard for monitoring
* Mobile application integration
* Multi-rover coordination
* Edge AI optimization

---

## Author

Ashish Upadhyay

B.Tech Information Technology
Amity University
Expected Graduation: June 2026
