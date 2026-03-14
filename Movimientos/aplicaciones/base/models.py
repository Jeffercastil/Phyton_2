from django.db import models
from django.contrib.auth.models import User


class Deuda(models.Model):  # ← AL MISMO NIVEL QUE Cliente, NO dentro de Transaccion
    TIPO_CHOICES = (
        ('DEUDA', 'Deuda Normal'),
        ('REPORTADO', 'Deuda Reportada'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='DEUDA')
    valor_inicial = models.DecimalField(max_digits=15, decimal_places=2)
    valor_total_a_pagar = models.DecimalField(max_digits=15, decimal_places=2)
    cuota_mensual = models.DecimalField(max_digits=15, decimal_places=2)
    total_meses = models.IntegerField()
    fecha_inicio = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def meses_pagados(self):
        from django.db.models import Sum
        pagos = Transaccion.objects.filter(
            usuario=self.usuario,
            deuda=self,
            tipo='GASTO'
        ).aggregate(total=Sum('monto'))['total'] or 0
        if self.cuota_mensual > 0:
            return int(pagos / self.cuota_mensual)
        return 0

    def total_pagado(self):
        from django.db.models import Sum
        return Transaccion.objects.filter(
            usuario=self.usuario,
            deuda=self,
            tipo='GASTO'
        ).aggregate(total=Sum('monto'))['total'] or 0

    def saldo_pendiente(self):
        return self.valor_total_a_pagar - self.total_pagado()

    def meses_restantes(self):
        return max(0, self.total_meses - self.meses_pagados())

    def interes_total(self):
        return self.valor_total_a_pagar - self.valor_inicial

    def interes_pagado(self):
        if self.valor_total_a_pagar > 0:
            proporcion = float(self.total_pagado()) / float(self.valor_total_a_pagar)
            return float(self.interes_total()) * proporcion
        return 0

    def porcentaje_pagado(self):
        if self.valor_total_a_pagar > 0:
            return round((float(self.total_pagado()) / float(self.valor_total_a_pagar)) * 100, 1)
        return 0

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"


class Transaccion(models.Model):  # ← Transaccion DESPUÉS de Deuda (para que pueda referenciarla)
    TIPO_CHOICES = (
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    deuda = models.ForeignKey(Deuda, on_delete=models.SET_NULL, null=True, blank=True)  # ← referencia directa, sin comillas
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100, default="General")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'base_transaccion'

    def __str__(self):
        signo = "+" if self.tipo == 'INGRESO' else "-"
        return f"[{self.usuario.username}] {self.tipo}: {signo}{self.monto} ({self.categoria})"


class Perfil(models.Model):
    """Modelo para almacenar información adicional del usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True, default='Colombia')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True, verbose_name='Biografía')
    avatar = models.CharField(max_length=10, blank=True, null=True, default='👤')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'base_perfil'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    def get_nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        if self.usuario.first_name or self.usuario.last_name:
            return f"{self.usuario.first_name} {self.usuario.last_name}".strip()
        return self.usuario.username