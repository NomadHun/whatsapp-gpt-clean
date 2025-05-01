import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Загружаем каталог плитки
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Генерируем краткий каталог для промпта
def build_product_summary():
    return "\n".join([
        f"{p['Название']} ({p['Размер']}, {p['Поверхность']}, {p['Цена']} тг)"
        for p in products
    ])

# Основная функция запроса к GPT
def get_gpt_response(message: str, product_name: str | None = None) -> tuple[str, bool]:
    product_summary = build_product_summary()

    system_prompt = (
        "Ты ассистент по продажам плитки QUASUN. "
        "Отвечай кратко, помогай с выбором и доводи клиента до покупки. "
        "Если клиент интересуется внешним видом плитки, добавь [SEND_IMAGE] в конец ответа.\n\n"
        f"Каталог:\n{product_summary}"
    )

    if product_name:
        system_prompt += f"\n\nКлиент упомянул товар: {product_name}. У него есть фото."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    text = response.choices[0].message.content.strip()
    send_image = "[SEND_IMAGE]" in text
    clean_text = text.replace("[SEND_IMAGE]", "").strip()

    return clean_text, send_image