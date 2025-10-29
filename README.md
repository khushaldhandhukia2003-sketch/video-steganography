# 🎥 Video Steganography Encoder & Decoder (FastAPI)

A **FastAPI-based backend** that allows you to **hide secret text (like job codes or messages) inside a video** and then **decode it back** later.  
This project demonstrates basic **video frame-level steganography** and can be extended for AI/ML or security-based applications.

---

## ✨ Features

✅ Hide (Encode) any custom text string inside a video  
✅ Reveal (Decode) the hidden message from the encoded video  
✅ Works with `.mp4` videos  
✅ Uses OpenCV, NumPy, and FastAPI  
✅ Fast, lightweight backend for AI/ML demos  
✅ Can be hosted easily on Render, Railway, or Colab  

---

## 📁 Folder Structure

```
video-steganography/
│
├── main.py                # FastAPI backend (routes & server)
├── stego_processor.py     # Core logic for video encoding/decoding
├── requirements.txt        # All dependencies
└── README.md              # Documentation (this file)
```

---

## ⚙️ Installation and Setup (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/khushaldhandhukia2003-sketch/video-steganography.git
cd video-steganography
```

### 2️⃣ Install dependencies
Make sure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the FastAPI server
```bash
uvicorn main:app --reload
```

### 4️⃣ Open in browser
Go to 👉 http://127.0.0.1:8000/docs

You’ll see:
```
🚀 Video Steganography API running successfully!
```

---

## 🧩 API Usage

### 🔹 **1. Encode (Hide) a message inside a video**

**Endpoint:** `/encode`  
**Method:** `POST`  

**Form Data:**
- `file`: Upload a `.mp4` video
- `hidden_text`: The text or job code you want to hide

Example:
```bash
curl -X POST -F "file=@sample.mp4" -F "hidden_text=hello123" http://127.0.0.1:8000/encode
```

✅ **Output:** Encoded video file will be saved in `/storage/processed/encoded_<id>.mp4`

---

### 🔹 **2. Decode (Reveal) hidden message from video**

**Endpoint:** `/decode`  
**Method:** `POST`  

**Form Data:**
- `file`: Upload the encoded `.mp4` video

Example:
```bash
curl -X POST -F "file=@encoded_123.mp4" http://127.0.0.1:8000/decode
```

✅ **Output:** Returns the **hidden text** that was embedded during encoding.

---

## 🧠 How It Works (Simplified)

1. **Encoding:**
   - The app reads frames using OpenCV.
   - Your secret text is embedded as metadata in the frames (in a way invisible to the eye).
   - The processed video is saved as an encoded file.

2. **Decoding:**
   - The app reads each frame again.
   - It extracts and reconstructs the hidden text.
   - The original message is displayed.

---

## ⚡ Speed Optimization

✅ Frame processing is vectorized with NumPy  
✅ Heavy OpenCV operations are minimized  
✅ Background tasks prevent blocking  


---

## 🧰 Technologies Used

| Library | Purpose |
|----------|----------|
| **FastAPI** | Backend framework for API routes |
| **OpenCV** | Video frame reading and writing |
| **NumPy** | Array and pixel-level operations |
| **Pillow** | Image manipulations |
| **EasyOCR** | Optical character recognition (if extended) |
| **Uvicorn** | ASGI server for FastAPI |

---

## 🔒 Future Enhancements
- Add **password protection** for hidden messages  
- Support **image and audio steganography**  
- Build a **Streamlit frontend** for direct upload & display  
- Use **deep learning (Autoencoders)** for advanced encoding  

---

## 👨‍💻 Author
**Khushal Dhandhukia**  
AI/ML Developer | AIML Enthusiast  

📧 Reach me for collaborations or feedback!

---

