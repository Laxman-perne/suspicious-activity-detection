import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import sys

# Load the trained model
model = load_model('suspicious_activity_model.h5')

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"[ERROR] Could not open video: {video_path}")
        sys.exit(1)

    frame_count = 0
    suspicious_frames = 0
    
    while True:
        # Read frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
            
        # Preprocess the frame
        try:
            image = cv2.resize(frame, (128, 128))
            image = img_to_array(image) / 255.0
            image = np.expand_dims(image, axis=0)
            
            # Predict
            prediction = model.predict(image, verbose=0)[0][0]
            label = 'Suspicious' if prediction > 0.5 else 'Normal'
            
            if label == 'Suspicious':
                suspicious_frames += 1
                
            frame_count += 1
            
        except Exception as e:
            print(f"[WARNING] Error processing frame {frame_count}: {str(e)}")
            continue

    cap.release()
    
    if frame_count == 0:
        print(f"[ERROR] No frames processed from {video_path}")
        sys.exit(1)
        
    return frame_count, suspicious_frames

if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] != '--input':
        print("Usage: python predict_video.py --input <video_path>")
        sys.exit(1)
        
    video_path = sys.argv[2]
    frame_count, suspicious_frames = process_video(video_path)
    
    print(f"[RESULT] Total Frames: {frame_count}")
    print(f"[RESULT] Suspicious Frames: {suspicious_frames}")
    print(f"[RESULT] Suspicious Activity Detected Percentage: {suspicious_frames/frame_count*100:.2f}% of video")