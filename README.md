# Suspicious Activity Detection from Video using Deep Learning

This project uses a Convolutional Neural Network (CNN) to detect suspicious activity in video footage. It processes videos frame-by-frame, classifies each frame as "Normal" or "Suspicious", and reports the percentage of suspicious frames detected.

---

## 📁 Project Structure

```
.
├── predict_video.py              # Detects suspicious frames in a video
├── train_model.py                # Trains the CNN using labeled frame data
├── extract_frames.py             # (Optional) Extracts frames from videos
├── static/                       # For static assets (if using a web UI)
├── templates/                    # For HTML templates (if using Flask)
├── frames/                       # Training data: /Normal, /Suspicious
├── suspicious_activity_model.h5  # Trained model
├── test_video.mp4                # Sample input video (optional)
└── requirements.txt              # Dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/suspicious-activity-detector.git
cd suspicious-activity-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Train the Model

Ensure your `frames/` directory is structured like:

```
frames/
├── Normal/
├── Suspicious/
```

Then train the model:

```bash
python train_model.py
```

The trained model will be saved as `suspicious_activity_model.h5`.

---

## 🎥 Run a Prediction

```bash
python predict_video.py --input test_video.mp4
```

Sample output:

```
[RESULT] Total Frames: 300
[RESULT] Suspicious Frames: 42
[RESULT] Suspicious Activity Detected Percentage: 14.00% of video
```

...

---

## 📃 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
