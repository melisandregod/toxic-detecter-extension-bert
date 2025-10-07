from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import os

# ------------------------
# 🔹 CONFIG
# ------------------------
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # ✅ อนุญาตทุก origin (ง่ายสุดสำหรับ dev)
        # หรือถ้าอยากจำกัดเฉพาะ extension ของคุณ
        # "chrome-extension://<YOUR_EXTENSION_ID>"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "./model"  # path โมเดล BERT ที่คุณเทรนเอง

# โหลดโมเดล
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# ------------------------
# 🔹 Gemini API Key
# ------------------------
# (1) ไปที่ https://aistudio.google.com/app/apikey
# (2) สร้าง API key แล้ววางลงใน .env หรือใส่ตรงนี้ (ชั่วคราว)
genai.configure(api_key="AIzaSyBKGJg-dODWqcAtSfDXVbZc8TIs_ACrk8w")

# ------------------------
# 🔹 Input Model
# ------------------------
class TextInput(BaseModel):
    text: str

# ------------------------
# 🔹 ฟังก์ชันตรวจข้อความ Toxic
# ------------------------
def predict_toxic(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)

    confidence, pred = torch.max(probs, dim=1)
    label = "toxic" if pred.item() == 1 else "non-toxic"
    return label, confidence.item()

# ------------------------
# 🔹 ฟังก์ชันใช้ Gemini แนะนำข้อความ
# ------------------------
def suggest_alternative(text):
    try:
        prompt = f"Rewrite politely in one short sentence: {text}"
        response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Unable to suggest alternative."

# ------------------------
# 🔹 API Endpoint
# ------------------------
@app.post("/predict")
def predict_text(input: TextInput):
    label, confidence = predict_toxic(input.text)
    suggestion = None

    if label == "toxic" and confidence > 0.6:
        suggestion = suggest_alternative(input.text)

    return {
        "text": input.text,
        "label": label,
        "confidence": round(confidence, 3),
        "suggestion": suggestion
    }

@app.get("/test_gemini")
def test_gemini():
    """
    🔍 Route สำหรับทดสอบ Gemini API ว่าเรียกได้ไหม
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Say hello politely.")
        return {
            "status": "✅ Gemini API connected successfully!",
            "response": response.text.strip()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "❌ Gemini API error",
            "error": str(e)
        }
    
@app.get("/list_models")
def list_gemini_models():
    """
    🔍 Route สำหรับดูรายการโมเดลที่ Gemini API รองรับ
    """
    try:
        models = genai.list_models()
        model_list = [m.name for m in models]
        return {"available_models": model_list}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
