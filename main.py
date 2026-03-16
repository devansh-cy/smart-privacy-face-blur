"""
main.py
=======
Smart Privacy Face Blur System – Entry Point

This is the main script that ties everything together.  It supports two
modes of operation:
Keyboard Controls (during display)
-----------------------------------
  Q  –  Quit the program
  S  –  Save the current processed frame
  T  –  Toggle between Blur and Pixelation effects
"""

import argparse
import cv2
import sys
import os

# Import our custom modules
from face_detector import detect_faces
from effects import apply_blur, apply_pixelation
from utils import draw_face_count, display_side_by_side, save_image


# ──────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────
OUTPUT_DIR = "output"          # folder where saved images go
EFFECT_BLUR = "Blur"
EFFECT_PIXEL = "Pixelation"


def process_image(image_path):
    """
    Load a single image, detect faces, apply the privacy effect,
    and display the result.  The user can toggle effects, save, or quit.
    """
    # --- Load the image ---------------------------------------------------
    if not os.path.isfile(image_path):
        print(f"[ERROR] File not found: {image_path}")
        sys.exit(1)

    frame = cv2.imread(image_path)
    if frame is None:
        print(f"[ERROR] Could not read image: {image_path}")
        sys.exit(1)

    print(f"[INFO] Image loaded: {image_path}")
    print("[INFO] Controls:  Q = Quit  |  S = Save  |  T = Toggle Effect")

    # --- Detect faces -----------------------------------------------------
    faces = detect_faces(frame)
    print(f"[INFO] Faces detected: {len(faces)}")

    # --- Main display loop ------------------------------------------------
    current_effect = EFFECT_BLUR  # start with Gaussian Blur

    while True:
        # Apply the chosen effect
        if current_effect == EFFECT_BLUR:
            processed = apply_blur(frame, faces)
        else:
            processed = apply_pixelation(frame, faces)

        # Draw info text on the processed frame
        display_frame = processed.copy()
        draw_face_count(display_frame, len(faces), current_effect)

        # Show original and processed side by side
        display_side_by_side(frame, display_frame)

        # Wait for a key press
        key = cv2.waitKey(0) & 0xFF

        if key == ord("q") or key == ord("Q"):
            print("[INFO] Quitting...")
            break
        elif key == ord("s") or key == ord("S"):
            save_image(processed, OUTPUT_DIR)
        elif key == ord("t") or key == ord("T"):
            # Toggle the effect
            if current_effect == EFFECT_BLUR:
                current_effect = EFFECT_PIXEL
            else:
                current_effect = EFFECT_BLUR
            print(f"[INFO] Effect switched to: {current_effect}")

    cv2.destroyAllWindows()


def process_webcam():
    """
    Open the default webcam, detect and blur faces in real-time,
    and display the live feed until the user quits.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        sys.exit(1)

    print("[INFO] Webcam opened. Press Q to quit, S to save, T to toggle.")

    current_effect = EFFECT_BLUR  # start with Gaussian Blur

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame from webcam.")
            break

        # Detect faces in the current frame
        faces = detect_faces(frame)

        # Apply the chosen privacy effect
        if current_effect == EFFECT_BLUR:
            processed = apply_blur(frame, faces)
        else:
            processed = apply_pixelation(frame, faces)

        # Draw info overlay
        display_frame = processed.copy()
        draw_face_count(display_frame, len(faces), current_effect)

        # Show original and processed side by side
        display_side_by_side(frame, display_frame)

        # Handle keyboard input (waitKey 1 ms for real-time)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == ord("Q"):
            print("[INFO] Quitting webcam...")
            break
        elif key == ord("s") or key == ord("S"):
            save_image(processed, OUTPUT_DIR)
        elif key == ord("t") or key == ord("T"):
            if current_effect == EFFECT_BLUR:
                current_effect = EFFECT_PIXEL
            else:
                current_effect = EFFECT_BLUR
            print(f"[INFO] Effect switched to: {current_effect}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


def parse_arguments():
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments with 'mode' and optionally 'input'.
    """
    parser = argparse.ArgumentParser(
        description="Smart Privacy Face Blur System – "
                    "Detect and blur faces in images or webcam video.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["image", "webcam"],
        required=True,
        help="Input mode: 'image' for a single image, 'webcam' for live video.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to the input image (required when mode is 'image').",
    )

    args = parser.parse_args()

    # Validate: image mode requires --input
    if args.mode == "image" and args.input is None:
        parser.error("--input is required when mode is 'image'.")

    return args


if __name__ == "__main__":
    print("=" * 55)
    print("   Smart Privacy Face Blur System")
    print("=" * 55)

    args = parse_arguments()

    if args.mode == "image":
        process_image(args.input)
    else:
        process_webcam()

    print("[INFO] Program finished.")
