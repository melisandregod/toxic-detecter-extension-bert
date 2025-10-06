from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from fastapi.middleware.cors import CORSMiddleware

# ---------- CONFIG ----------
MODEL_PATH = "./model"  # ชี้ไปยังโฟลเดอร์โมเดลของคุณ
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------- โหลดโมเดล ----------
print("🔹 Loading model from:", MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    trust_remote_code=False
)
model.to(DEVICE)
model.eval()
print("✅ Model loaded successfully!")

# ---------- FastAPI ----------
app = FastAPI(title="Custom BERT Toxic Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือเฉพาะ origin ของ extension ก็ได้ เช่น "chrome-extension://<EXT_ID>"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TextInput(BaseModel):
    text: str

@app.post("/predict")
async def predict(input: TextInput):
    inputs = tokenizer(input.text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)

    confidence, pred = torch.max(probs, dim=1)
    label = "toxic" if pred.item() == 1 else "non-toxic"

    return {
        "text": input.text,
        "label": label,
        "confidence": float(confidence.item())
    }

@app.get("/")
async def root():
    return {"message": "Your custom BERT Toxic Detector API is running!"}
