from django.db import models




from django.db import models

class Ticket(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    correo = models.EmailField()
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="pendiente")

    def __str__(self):
        return f"{self.asunto} - {self.estado}"



