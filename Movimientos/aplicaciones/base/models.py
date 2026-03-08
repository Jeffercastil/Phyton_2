from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    documento_identidad = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'base_cliente'  # ← Especifica el nombre exacto de la tabla

    def __str__(self):
        return f"{self.nombre} ({self.documento_identidad})"


class Transaccion(models.Model):
    TIPO_CHOICES = (
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100, default="General")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'base_transaccion'  # ← Especifica el nombre exacto de la tabla

    def __str__(self):
        signo = "+" if self.tipo == 'INGRESO' else "-"
        return f"[{self.usuario.username}] {self.tipo}: {signo}{self.monto} ({self.categoria})"