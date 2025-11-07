#!/usr/bin/env python3
"""
YOLO12 Rune Detection Script
Detects runes in images, videos, or webcam feed using YOLOv12
"""

import argparse
import cv2
import time
from pathlib import Path
from ultralytics import YOLO
import numpy as np


class RuneDetector:
    """Rune detection using YOLO12 model"""

    def __init__(self, model_path='yolo12n.pt', conf_threshold=0.25, iou_threshold=0.45):
        """
        Initialize the rune detector

        Args:
            model_path: Path to YOLO12 model weights
            conf_threshold: Confidence threshold for detections
            iou_threshold: IoU threshold for NMS
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

        print(f"Loading YOLO12 model from {model_path}...")
        self.model = YOLO(model_path)
        print("Model loaded successfully!")

    def detect_image(self, image_path, output_path=None, show=True):
        """
        Detect runes in a single image

        Args:
            image_path: Path to input image
            output_path: Path to save output image (optional)
            show: Whether to display the result
        """
        print(f"\nProcessing image: {image_path}")

        # Run inference
        results = self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            save=False,
            verbose=False
        )

        # Get annotated image
        annotated_img = results[0].plot()

        # Print detection results
        detections = results[0].boxes
        print(f"Found {len(detections)} rune(s)")

        for i, box in enumerate(detections):
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            class_name = self.model.names[cls]
            print(f"  Rune {i+1}: {class_name} (confidence: {conf:.2f})")

        # Save output
        if output_path:
            cv2.imwrite(output_path, annotated_img)
            print(f"Saved result to: {output_path}")

        # Display
        if show:
            cv2.imshow('Rune Detection', annotated_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return results

    def detect_video(self, video_path, output_path=None, show=True):
        """
        Detect runes in a video file

        Args:
            video_path: Path to input video
            output_path: Path to save output video (optional)
            show: Whether to display the result
        """
        print(f"\nProcessing video: {video_path}")

        cap = cv2.VideoCapture(video_path)

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Setup video writer
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        start_time = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Run detection
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                save=False,
                verbose=False
            )

            # Get annotated frame
            annotated_frame = results[0].plot()

            # Add FPS counter
            elapsed = time.time() - start_time
            current_fps = frame_count / elapsed if elapsed > 0 else 0
            cv2.putText(annotated_frame, f'FPS: {current_fps:.1f}',
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Write frame
            if writer:
                writer.write(annotated_frame)

            # Display
            if show:
                cv2.imshow('Rune Detection', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nStopped by user")
                    break

            # Progress
            if frame_count % 30 == 0:
                print(f"Processed {frame_count}/{total_frames} frames ({frame_count/total_frames*100:.1f}%)")

        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()

        print(f"\nProcessed {frame_count} frames")
        if output_path:
            print(f"Saved result to: {output_path}")

    def detect_webcam(self, camera_id=0):
        """
        Detect runes in real-time from webcam

        Args:
            camera_id: Camera device ID (default: 0)
        """
        print(f"\nStarting webcam detection (camera {camera_id})")
        print("Press 'q' to quit")

        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_id}")
            return

        frame_count = 0
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            frame_count += 1

            # Run detection
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                save=False,
                verbose=False
            )

            # Get annotated frame
            annotated_frame = results[0].plot()

            # Add FPS counter
            elapsed = time.time() - start_time
            current_fps = frame_count / elapsed if elapsed > 0 else 0
            cv2.putText(annotated_frame, f'FPS: {current_fps:.1f}',
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Add detection count
            num_detections = len(results[0].boxes)
            cv2.putText(annotated_frame, f'Runes: {num_detections}',
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display
            cv2.imshow('Rune Detection - Webcam', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nStopped by user")
                break

        cap.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='YOLO12 Rune Detection')
    parser.add_argument('--source', type=str, help='Path to image or video file, or "webcam" for camera')
    parser.add_argument('--model', type=str, default='models/best.pt', help='Path to YOLO12 model (default: models/best.pt)')
    parser.add_argument('--conf', type=float, default=0.25, help='Confidence threshold (default: 0.25)')
    parser.add_argument('--iou', type=float, default=0.45, help='IoU threshold (default: 0.45)')
    parser.add_argument('--output', type=str, help='Output path for result')
    parser.add_argument('--no-show', action='store_true', help='Do not display results')
    parser.add_argument('--camera-id', type=int, default=0, help='Camera device ID (default: 0)')

    args = parser.parse_args()

    # Initialize detector
    detector = RuneDetector(
        model_path=args.model,
        conf_threshold=args.conf,
        iou_threshold=args.iou
    )

    # Process based on source type
    if not args.source:
        print("Error: --source is required")
        print("Examples:")
        print("  python detect_rune.py --source image.jpg")
        print("  python detect_rune.py --source video.mp4 --output output.mp4")
        print("  python detect_rune.py --source webcam")
        return

    if args.source.lower() == 'webcam':
        detector.detect_webcam(camera_id=args.camera_id)
    else:
        source_path = Path(args.source)
        if not source_path.exists():
            print(f"Error: Source file not found: {args.source}")
            return

        # Determine if image or video
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv'}

        ext = source_path.suffix.lower()

        if ext in image_extensions:
            detector.detect_image(
                str(source_path),
                output_path=args.output,
                show=not args.no_show
            )
        elif ext in video_extensions:
            detector.detect_video(
                str(source_path),
                output_path=args.output,
                show=not args.no_show
            )
        else:
            print(f"Error: Unsupported file format: {ext}")
            print(f"Supported image formats: {', '.join(image_extensions)}")
            print(f"Supported video formats: {', '.join(video_extensions)}")


if __name__ == '__main__':
    main()
