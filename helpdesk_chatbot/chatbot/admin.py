from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_usuario", "correo", "asunto", "estado", "fecha_creacion")
    list_filter = ("estado", "fecha_creacion")
    search_fields = ("nombre_usuario", "correo", "asunto", "descripcion")
    ordering = ("-fecha_creacion",)
