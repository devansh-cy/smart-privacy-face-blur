"""
effects.py
==========
Privacy effects module – Gaussian Blur and Pixelation.

Each function takes a frame and a list of face bounding boxes, applies
the chosen effect to every face region, and returns the modified frame.
"""

import cv2
import numpy as np


def apply_blur(frame, faces, ksize=99):
    """
    Apply Gaussian Blur to each detected face region.

    Parameters
    ----------
    frame : numpy.ndarray
        The original BGR image.
    faces : list of tuple
        List of (x, y, w, h) bounding boxes from the face detector.
    ksize : int
        Kernel size for GaussianBlur (must be odd). Larger = more blur.

    Returns
    -------
    numpy.ndarray
        A copy of the frame with all face regions blurred.
    """
    # Work on a copy so the original frame stays untouched
    output = frame.copy()

    # Make sure kernel size is odd (OpenCV requirement)
    if ksize % 2 == 0:
        ksize += 1

    for (x, y, w, h) in faces:
        # Extract the Region of Interest (ROI) – the face area
        roi = output[y : y + h, x : x + w]

        # Apply Gaussian Blur to the ROI
        blurred_roi = cv2.GaussianBlur(roi, (ksize, ksize), 30)

        # Replace the original face region with the blurred version
        output[y : y + h, x : x + w] = blurred_roi

    return output


def apply_pixelation(frame, faces, pixel_size=10):
    """
    Apply a pixelation (mosaic) censor effect to each detected face.

    How it works:
      1. Shrink the face ROI to a very small size.
      2. Scale it back up using nearest-neighbour interpolation.
      This creates the classic "pixelated" / "mosaic" look.

    Parameters
    ----------
    frame : numpy.ndarray
        The original BGR image.
    faces : list of tuple
        List of (x, y, w, h) bounding boxes.
    pixel_size : int
        Controls the block size. Smaller = more pixelated.

    Returns
    -------
    numpy.ndarray
        A copy of the frame with all face regions pixelated.
    """
    output = frame.copy()

    for (x, y, w, h) in faces:
        # Extract the face ROI
        roi = output[y : y + h, x : x + w]

        # Step 1 – Shrink the ROI to a tiny size
        small = cv2.resize(
            roi,
            (pixel_size, pixel_size),
            interpolation=cv2.INTER_LINEAR,
        )

        # Step 2 – Scale it back to the original size (nearest-neighbour
        # keeps the blocky look)
        pixelated_roi = cv2.resize(
            small,
            (w, h),
            interpolation=cv2.INTER_NEAREST,
        )

        # Replace the face region with the pixelated version
        output[y : y + h, x : x + w] = pixelated_roi

    return output
