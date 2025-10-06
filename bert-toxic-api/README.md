# 🧠 BERT Toxic Comment Detector API (Simple Version)

A simple REST API for detecting toxic language using your **custom fine-tuned BERT model**, powered by **FastAPI** and **PyTorch**.

---

## 🚀 Features
- ✅ Uses your own fine-tuned BERT model
- ⚡ Built with FastAPI (lightweight and fast)
- 🧠 GPU-ready (CUDA supported)
- 🧩 Easy JSON API interface

---

## 🗂️ Project Structure

```
bert-toxic-api/
│
├── venv/                      # Python virtual environment
├── app.py                     # Main FastAPI app
├── requirements.txt            # Dependencies
└── model/                      # Your trained model folder
    ├── config.json
    ├── tokenizer.json
    ├── vocab.txt
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    └── pytorch_model.bin
```

---

## ⚙️ Installation (macOS / Linux)

### 1️⃣ 
```bash
cd bert-toxic-api
```

### 2️⃣ Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install fastapi uvicorn transformers torch
```

### 4️⃣ Place your fine-tuned model
Copy your model into the `model/` folder (from `save_pretrained()`).


## ▶️ Run API
```bash
uvicorn app:app --reload
```

Then open in browser:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Example Test

```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"text": "You are stupid"}'
```

Response:
```json
{
  "text": "You are stupid",
  "label": "toxic",
  "confidence": 0.97
}
```

---

## 📦 Requirements

```
fastapi
uvicorn
transformers
torch
```

---

## 🧑‍💻 Author
Developed by **Your Name**  
Fine-tuned BERT Toxic Detector  
🚀 Powered by [FastAPI](https://fastapi.tiangolo.com/) & [Transformers](https://huggingface.co/transformers/)
