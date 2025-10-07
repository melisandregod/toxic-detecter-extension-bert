# 🧠 BERT Toxic API + Chrome Extension (Windows Setup Guide)

A simple step-by-step guide for installing and running both the **FastAPI backend** and the **Realtime Chrome Extension** on Windows. 🚀

---

## 🧠 BERT Toxic API (FastAPI)

### 📦 Installation
1. Open **Command Prompt** or **PowerShell**
2. Go to your project folder:
   ```bash
   cd bert-toxic-api
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install required libraries:
   ```bash
   pip install fastapi uvicorn transformers torch
   pip install google-generativeai fastapi uvicorn transformers torch
<<<<<<< HEAD
=======

>>>>>>> 1d09d4d (Update README and content.js to enhance installation instructions and improve toxicity bubble display)
   ```

---

### ▶️ Run the API
1. Start the server:
   ```bash
   uvicorn app:app --reload
   ```
2. Wait until you see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```
3. Open your browser and visit:
   👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

4. Or test via command line:
   ```bash
   curl -X POST "http://127.0.0.1:8000/predict" ^
   -H "Content-Type: application/json" ^
   -d "{\"text\": \"you are stupid\"}"
   ```

✅ Example Output:
```json
{
  "text": "you are stupid",
  "label": "toxic",
  "confidence": 0.97
}
```

---

## 🧩 Chrome Extension (Realtime Toxicity Checker)

### ⚙️ Installation
1. Open **Google Chrome**
2. Go to:
   ```
   chrome://extensions/
   ```
3. Turn on **Developer Mode** (top-right corner)
4. Click **Load unpacked**
5. Select the folder:
   ```
   chrome-toxic-extension
   ```

---

### ▶️ Usage
1. Open any webpage that has a typing field (Google, YouTube, Reddit, etc.)
2. Start typing any text — for example:
   ```
   you are stupid
   ```
3. Wait **5 seconds** after finishing typing  
   → The extension will analyze the text via your local API

Bubble will appear below your input box:
- 🟢 **Clean (xx%)** = Safe message  
- 🔴 **Toxic (xx%)** = Contains toxic words

> ⚠️ **Note:** You must have the API running (`uvicorn app:app --reload`) before using the extension.

---

## 🧩 Quick Start Summary

```bash
# Run API
cd bert-toxic-api
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn transformers torch
uvicorn app:app --reload
```

Then:
1️⃣ Open Chrome → `chrome://extensions/`  
2️⃣ Click **Load unpacked** → Choose `chrome-toxic-extension/`  
3️⃣ Type in any text field → Wait 5 seconds → See result ✅

---

Enjoy your local BERT Toxicity Detector 🔥
