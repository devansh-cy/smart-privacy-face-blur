"""
face_detector.py
================
Face detection module using Haar Cascade Classifier.

This module wraps OpenCV's pre-trained Haar Cascade model to detect
frontal human faces in an image or video frame.
"""

import cv2
import os


CASCADE_PATH = os.path.join(
    cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
)

# Create the classifier object once (reused across all calls)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Safety check – make sure the classifier loaded correctly
if face_cascade.empty():
    raise IOError(
        f"Could not load Haar Cascade from: {CASCADE_PATH}\n"
        "Make sure opencv-python is installed correctly."
    )


def detect_faces(frame):
    """
    Detect all frontal faces in the given BGR frame.

    Parameters
    ----------
    frame : numpy.ndarray
        A BGR image (as returned by cv2.imread or cv2.VideoCapture.read).

    Returns
    -------
    list of tuple
        Each tuple is (x, y, w, h) representing the bounding box of a
        detected face.  Returns an empty list if no faces are found.
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detections = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
    )

    # detectMultiScale returns a numpy array or an empty tuple
    # Convert to a plain Python list of tuples for consistency
    faces = []
    for (x, y, w, h) in detections:
        faces.append((int(x), int(y), int(w), int(h)))

    return faces
