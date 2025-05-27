import cv2
import os

def extract_frames(video_path, output_folder, label):
    cap = cv2.VideoCapture(video_path)
    count = 0
    success, frame = cap.read()

    label_folder = os.path.join(output_folder, label)
    os.makedirs(label_folder, exist_ok=True)

    while success:
        frame_path = os.path.join(label_folder, f"{label}_{count}.jpg")
        cv2.imwrite(frame_path, frame)
        success, frame = cap.read()
        count += 1

    cap.release()
    print(f"[INFO] Extracted {count} frames from {video_path}")

base_path = "dataset"
output_path = "frames"

for label in ["normal", "suspicious"]:
    folder = os.path.join(base_path, label)
    for video_file in os.listdir(folder):
        video_path = os.path.join(folder, video_file)
        extract_frames(video_path, output_path, label)