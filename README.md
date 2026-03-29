#  Smart Privacy Face Blur System

A Digital Image Processing project built with **Python** and **OpenCV** that automatically detects human faces in images and live webcam video and applies **Gaussian Blur** or **Pixelation** to protect privacy.

---

## 📁 Folder Structure

```
smart-privacy-face-blur/
├── main.py               # Entry point (CLI)
├── face_detector.py      # Haar Cascade face detection
├── effects.py            # Blur & pixelation effects
├── utils.py              # Display, save, and overlay helpers
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── project_report.md     # College submission document
├── output/               # Saved processed images
└── sample_images/        # Place your test images here
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher

### Steps

```bash
# 1. Navigate to the project folder
cd smart-privacy-face-blur

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Image Mode
```bash
python main.py --mode image --input sample_images/photo.jpg
```

### Webcam Mode
```bash
python main.py --mode webcam
```

### Keyboard Controls
| Key | Action |
|-----|--------|
| **Q** | Quit the program |
| **S** | Save the processed image to `output/` |
| **T** | Toggle between Blur and Pixelation |

---

## 🧠 Step-by-Step Explanation

### 1. Loading Input
- **Image mode**: `cv2.imread()` loads the image from disk.
- **Webcam mode**: `cv2.VideoCapture(0)` opens the default camera and reads frames in a loop.

### 2. Face Detection (face_detector.py)
- The frame is converted to **grayscale** using `cv2.cvtColor()` because Haar Cascade works on single-channel images.
- `cv2.CascadeClassifier` loads the pre-trained `haarcascade_frontalface_default.xml` model (bundled with OpenCV).
- `detectMultiScale()` scans the image at multiple scales and returns bounding boxes `(x, y, w, h)` for every detected face.

### 3. Applying Effects (effects.py)

#### Gaussian Blur
- The face **Region of Interest (ROI)** is extracted: `frame[y:y+h, x:x+w]`.
- `cv2.GaussianBlur()` is applied with a large kernel (99×99) to heavily blur the region.
- The blurred ROI replaces the original face area.

#### Pixelation
- The face ROI is **shrunk** to a tiny size (e.g., 10×10 pixels).
- It is then **scaled back up** using nearest-neighbour interpolation, creating a blocky/mosaic look.

### 4. Display & Controls (utils.py, main.py)
- The original and processed frames are shown **side by side** using `np.hstack()`.
- The face count and current effect name are drawn on the frame with `cv2.putText()`.
- The keyboard loop listens for **Q**, **S**, and **T** key presses.

---

## 💡 Suggestions to Improve Further

1. **DNN-based detector** – Replace Haar Cascade with OpenCV's DNN face detector (`res10_300x300_ssd_iter_140000.caffemodel`) for better accuracy.
3. **Video file input** – Add a third mode to process pre-recorded video files (MP4, AVI).
4. **Selective blurring** – Let the user click on specific faces to blur only those (ignore others).
5. **Face tracking** – Use OpenCV trackers (KCF, CSRT) to maintain identity across frames and improve speed.
6. **GUI** – Build a graphical interface with Tkinter or PyQt so non-technical users can use the tool easily.
7. **Batch processing** – Process all images in a folder automatically and save results.
8. **Eye / body detection** – Extend to blur license plates, body regions, or other sensitive content.

---

## 📝 License

This project is for **educational purposes** (Digital Image Processing coursework).
