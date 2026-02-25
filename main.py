import os
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# ===============================
# Настройки
# ===============================

MODEL_NAME = "Qwen/Qwen-7B-Chat-GPTQ"
HF_TOKEN = os.getenv("HF_TOKEN")  # берём токен из Environment Variables
DEVICE = "cpu"  # если будет GPU, можно поменять на "cuda"
MAX_TOKENS = 128

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN не найден! Добавь его в Environment Variables.")

print("Загрузка модели...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    token=HF_TOKEN
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    token=HF_TOKEN
)

model.to(DEVICE)
model.eval()

print("Модель успешно загружена ✅")

# ===============================
# API
# ===============================

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data["prompt"]

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_TOKENS,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"response": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# Запуск сервера
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


