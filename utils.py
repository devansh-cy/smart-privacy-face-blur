"""
utils.py
========
Utility helpers for display, saving, and text overlay.
"""

import cv2
import numpy as np
import os
from datetime import datetime


def draw_face_count(frame, count, effect_name="Blur"):
    """
    Draw the number of detected faces and current effect name on the frame.

    Parameters
    ----------
    frame : numpy.ndarray
        The processed BGR frame (will be modified in-place).
    count : int
        Number of faces detected.
    effect_name : str
        Name of the active effect ("Blur" or "Pixelation").

    Returns
    -------
    numpy.ndarray
        The frame with text drawn on it.
    """
    text = f"Faces: {count} | Effect: {effect_name}"
    cv2.putText(
        frame,
        text,
        (10, 30),                         # position (x, y)
        cv2.FONT_HERSHEY_SIMPLEX,         # font
        0.8,                               # font scale
        (0, 255, 0),                       # green colour
        2,                                 # thickness
        cv2.LINE_AA,                       # anti-aliased
    )

    # Show keyboard shortcuts at the bottom
    help_text = "Q: Quit | S: Save | T: Toggle Effect"
    h = frame.shape[0]
    cv2.putText(
        frame,
        help_text,
        (10, h - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (200, 200, 200),
        1,
        cv2.LINE_AA,
    )

    return frame


def display_side_by_side(original, processed, window_name="Face Blur System"):
    """
    Concatenate original and processed frames horizontally and show them.

    Parameters
    ----------
    original : numpy.ndarray
        The unmodified frame.
    processed : numpy.ndarray
        The frame with privacy effects applied.
    window_name : str
        Title for the OpenCV window.
    """
    # Make sure both frames have the same height before concatenation
    h1, w1 = original.shape[:2]
    h2, w2 = processed.shape[:2]

    if h1 != h2:
        # Resize processed to match original height
        processed = cv2.resize(processed, (int(w2 * h1 / h2), h1))

    combined = np.hstack([original, processed])
    cv2.imshow(window_name, combined)


def save_image(frame, output_dir="output"):
    """
    Save the processed frame to the output directory with a timestamp name.

    Parameters
    ----------
    frame : numpy.ndarray
        The frame to save.
    output_dir : str
        Directory where the image will be saved.

    Returns
    -------
    str
        The file path of the saved image.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"blurred_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    cv2.imwrite(filepath, frame)
    print(f"[INFO] Image saved to: {filepath}")

    return filepath
