console.log("✅ Realtime Toxicity Checker Loaded");

const API_URL = "http://127.0.0.1:8000/predict";
const THRESHOLD = 0.7; // ความมั่นใจที่ถือว่า toxic
const DELAY = 2000; // เวลา
let typingTimers = new WeakMap(); // เก็บ timer ของแต่ละช่อง

// ฟังก์ชันหลัก: ตรวจข้อความในช่อง input/textarea
async function checkToxicity(el) {
  const text = el.value.trim();
  if (!text) return;

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    const label = data.label;
    const confidence = data.confidence;
    showBubble(el, label, confidence);
  } catch (err) {
    console.error("❌ API Error:", err);
  }
}

// แสดง bubble แจ้งผล
function showBubble(inputEl, label, confidence) {
  const old = document.getElementById("toxic-bubble");
  if (old) old.remove();

  const bubble = document.createElement("div");
  bubble.id = "toxic-bubble";

  if (label === "toxic" && confidence > THRESHOLD) {
    bubble.textContent = `⚠️ Toxic (${(confidence * 100).toFixed(1)}%)`;
    bubble.style.background = "rgba(255, 0, 0, 0.85)";
  } else {
    bubble.textContent = `✅ Clean (${(confidence * 100).toFixed(1)}%)`;
    bubble.style.background = "rgba(0, 128, 0, 0.85)";
  }

  Object.assign(bubble.style, {
    position: "absolute",
    color: "white",
    padding: "4px 8px",
    borderRadius: "6px",
    fontSize: "12px",
    fontFamily: "Arial, sans-serif",
    zIndex: "99999",
    pointerEvents: "none",
    opacity: "0",
    transition: "opacity 0.3s ease"
  });

  document.body.appendChild(bubble);

  const rect = inputEl.getBoundingClientRect();
  bubble.style.left = `${rect.left + window.scrollX}px`;
  bubble.style.top = `${rect.bottom + window.scrollY + 6}px`;
  bubble.style.opacity = "1";

  setTimeout(() => bubble.remove(), 4000);
}

// ดักการพิมพ์ในทุก input และ textarea
function attachListeners() {
  const inputs = document.querySelectorAll("input[type=text], textarea");
  inputs.forEach((el) => {
    el.addEventListener("input", () => {
      clearTimeout(typingTimers.get(el));
      const timer = setTimeout(() => checkToxicity(el), DELAY);
      typingTimers.set(el, timer);
    });
  });
}

// ติดตั้ง listener ทันที
attachListeners();

// ถ้าในเว็บมี element ถูกเพิ่มใหม่ เช่นช่องแชต dynamic
// ใช้ MutationObserver ดักและติด listener ให้ช่องใหม่ด้วย
const observer = new MutationObserver(() => attachListeners());
observer.observe(document.body, { childList: true, subtree: true });
