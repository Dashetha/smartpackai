🚀 SmartPack-AI
AI-Powered Intelligent Packing Advisor with Real-Time Object Measurement & Optimization
📌 Project Vision

SmartPack-AI is an AI-powered intelligent packing advisor designed to solve real-world inefficiencies in logistics, e-commerce, and retail packaging.

Traditional packing methods rely on manual estimation, often leading to:

❌ Wasted box space

❌ Increased shipping costs

❌ Higher packaging material consumption

❌ Environmental waste

SmartPack-AI transforms this process using:

🎥 Real-time webcam object scanning

🤖 AI-based dimension estimation

📦 Intelligent bin-packing optimization

🧊 3D visualization of fit

☁️ Cloud-based ML inference (AWS)

🔁 CI/CD automated deployment pipeline

This system combines Computer Vision + Machine Learning + Cloud + DevOps + 3D Graphics into a production-grade architecture.

🧠 System Architecture Overview

SmartPack-AI follows a modular, scalable microservice-inspired architecture.

User → Webcam → Frontend (JS + OpenCV.js)
        ↓
Dimension Data → Backend (FastAPI)
        ↓
ML Inference (TensorFlow Model)
        ↓
Packing Optimization Algorithm
        ↓
3D Visualization (Three.js)
        ↓
Cloud Storage + Logging (AWS)
🎯 Core Features
1️⃣ Webcam-Based Object Scanning

Uses WebRTC / MediaDevices API

Captures object in real time

Frame extraction and preprocessing

Edge detection / contour detection

2️⃣ AI-Driven Dimension Estimation

Trained using Kaggle dataset (Google Colab)

CNN-based regression model

Predicts:

Length

Width

Height

Uses reference calibration object for real-world scale conversion

3️⃣ Smart Packing Recommendation

Implements:

First-Fit Decreasing (FFD) Bin Packing Algorithm

Volume optimization

Space utilization scoring

Packaging efficiency calculation

Outputs:

Recommended box ID

Fit percentage

Wasted space %

Confidence score

4️⃣ 3D Visualization of Packing

Built using Three.js:

Renders selected box

Renders object with predicted dimensions

Shows:

Fit alignment

Rotational possibilities

Unused volume visually

This enhances user trust and transparency.

5️⃣ Cloud-Enabled ML Inference (AWS)

Architecture includes:

S3 → stores scanned images

Lambda → trigger-based processing

EC2 / ECS → model serving

API Gateway → public endpoint

CloudWatch → monitoring

This ensures:

Scalability

Fault tolerance

Production readiness

6️⃣ DevOps & CI/CD Integration

Dockerized backend

GitHub Actions pipeline

Automated build

AWS ECS deployment

Environment variable injection

Rollback strategy

🏗️ Technology Stack
🌐 Frontend

HTML5

CSS3

Vanilla JavaScript

WebRTC API

OpenCV.js

TensorFlow.js (optional inference)

Three.js (3D rendering)

🖥 Backend

Python

FastAPI

TensorFlow / Keras

OpenCV

Pydantic

Uvicorn

Docker

🤖 Machine Learning

CNN Regression Model

Trained in Google Colab

Kaggle dataset

Image augmentation

MinMax normalization

MSE Loss Function

Adam Optimizer

☁️ Cloud

AWS S3

AWS Lambda

AWS EC2 / ECS

AWS CloudWatch

AWS API Gateway

🔁 DevOps

Docker

GitHub Actions

CI/CD pipelines

AWS deployment automation

📂 Project Structure
SmartPack-AI/
│
├── frontend/
│   ├── index.html
│   ├── styles/
│   │   └── style.css
│   ├── js/
│   │   ├── camera.js
│   │   ├── dimension-estimator.js
│   │   └── box-visualizer.js
│   └── assets/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── model/
│   │   │   ├── dimension_model.pkl
│   │   │   └── pack_optimizer.py
│   │   └── utils/
│   │       ├── cv_helpers.py
│   │       └── inference.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── cloud/
│   └── aws/
│
├── ci-cd/
│
├── README.md
└── .gitignore
🧪 Machine Learning Model Development
📊 Dataset

Sourced from Kaggle

Labeled object images

Real-world dimension annotations

🧼 Data Preprocessing

Image resizing (224x224)

Background noise reduction

Contour extraction

Data augmentation:

Rotation

Scaling

Brightness variation

Horizontal flips

🏗 Model Architecture

CNN Architecture:

Conv2D + ReLU

MaxPooling

BatchNormalization

Dropout

Dense layers

Output layer (3 neurons → L, W, H)

Loss: Mean Squared Error
Optimizer: Adam
Metrics: MAE

🎓 Training

Platform: Google Colab

GPU acceleration

50–100 epochs

Early stopping

Model checkpointing

Exported model as .pkl / .h5


🏗️ System Architecture
🔷 High-Level Architecture Diagram

User
  ↓
Webcam Capture (WebRTC + OpenCV.js)
  ↓
Frontend Processing (JS)
  ↓
FastAPI Backend (Dockerized)
  ↓
ML Model Inference (TensorFlow)
  ↓
Packing Optimization Algorithm
  ↓
Response to Frontend
  ↓
3D Visualization (Three.js)
  ↓
AWS Cloud Logging & Storage

🧠 Machine Learning Pipeline Architecture
🔷 ML Training & Inference Flow


<img width="1227" height="960" alt="gitimage" src="https://github.com/user-attachments/assets/35e5f8d6-00e3-414f-a7eb-4f8e9f25e197" />





