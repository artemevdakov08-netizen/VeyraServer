from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Модель GPT (например Qwen-7B-Chat или любая легкая GPTQ версия)
model_name = "Qwen/Qwen-7B-Chat-GPTQ"  # можно заменить на GPTQ для легкости
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16  # экономим RAM
)
model.eval()

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Преобразуем в токены
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")  # или "cuda" если есть GPU
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,  # ограничение, чтобы не застрял
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
