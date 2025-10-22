from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai
import os, json

# Cargar clave API 
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "key.env"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def index(request):
    return render(request, "index.html")

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            message = body.get("message", "")

            if not message:
                return JsonResponse({"response": "No recibí ningún mensaje "})

            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(
                f"Eres un asistente virtual de soporte técnico para la empresa Implementos. "
                f"Responde de forma amable, clara y profesional. Pregunta del usuario: {message}"
            )

            response_text = response.text if hasattr(response, "text") else "No entendí tu mensaje 🤖"
            return JsonResponse({"response": response_text})

        except Exception as e:
            print("Error en webhook:", e)
            return JsonResponse({"response": "Ocurrió un error al procesar tu mensaje."})
    else:
        return JsonResponse({"response": "Método no permitido."}, status=405)