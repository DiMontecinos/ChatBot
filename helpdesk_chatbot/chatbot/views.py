from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from openai import OpenAI   # ✅ Import correcto para la nueva versión
import os, json

# se supone que carga key
load_dotenv("key.env")

# crea cliente 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def index(request):
    return render(request, "index.html")

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            message = body.get("message", "")

            if not message:
                return JsonResponse({"response": "No recibí ningún mensaje 😅"})

            # envia mensaje
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente virtual de soporte técnico para la empresa Implementos."},
                    {"role": "user", "content": message}
                ]
            )

            response_text = completion.choices[0].message.content.strip()
            return JsonResponse({"response": response_text})

        except Exception as e:
            print("Error en webhook:", e)
            return JsonResponse({"response": "Ocurrió un error al procesar tu mensaje."})
    else:
        return JsonResponse({"response": "Método no permitido."}, status=405)
