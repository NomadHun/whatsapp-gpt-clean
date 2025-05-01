from fastapi import FastAPI, Request
from fastapi.responses import Response
from gpt_engine import get_gpt_response
import json

app = FastAPI()

# Загружаем каталог плитки
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Поиск image_url по названию плитки
def find_image_url(reply_text: str) -> str | None:
    for product in products:
        if product["Название"].lower() in reply_text.lower():
            return product.get("image_url")
    return None

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    message = form.get("Body")
    phone = form.get("From")

    reply, send_image = get_gpt_response(message)
    image_url = find_image_url(reply)

    if send_image and image_url:
        return Response(content=f"""
<Response>
  <Message>
    <Body>{reply}</Body>
    <Media>{image_url}</Media>
  </Message>
</Response>
""", media_type="application/xml")

    return Response(content=f"""
<Response>
  <Message>
    <Body>{reply}</Body>
  </Message>
</Response>
""", media_type="application/xml")