from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai
import os, json
from .models import Ticket

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
                return JsonResponse({"response": "No recibí ningún mensaje 😅"})

            # Procesar respuesta con Gemini
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(
                f"Eres un asistente de soporte técnico. Un usuario escribió: {message}. "
                "Genera una breve respuesta amable y profesional."
            )

            respuesta_chatbot = response.text.strip()

            # aqui guarda el ticket
            Ticket.objects.create(
                nombre_usuario="Usuario anónimo",
                correo="sin_correo@implementos.cl",
                asunto="Consulta general desde chatbot",
                descripcion=message,
                estado="Pendiente"
            )

            return JsonResponse({"response": respuesta_chatbot})

        except Exception as e:
            print("Error en webhook:", e)
            return JsonResponse({"response": "Ocurrió un error al procesar tu mensaje."})
    else:
        return JsonResponse({"response": "Método no permitido."}, status=405)