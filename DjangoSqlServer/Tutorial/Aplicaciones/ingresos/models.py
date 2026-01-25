from django.db import models
from django.core.validators import EmailValidator

class Cliente(models.Model):
    documento_identidad = models.CharField(max_length=20, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(validators=[EmailValidator()])
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    TIPO_CHOICES = [
        ('MUJER', 'Mujer'),
        ('HOMBRE', 'Hombre'),
        ('NIÑO', 'Niño'),
    ]
    
    CATEGORIA_CHOICES = [
        ('JJ', 'Joyería'),
        ('PP', 'Perfumería'),
        ('AA', 'Accesorios'),
    ]
    
    codigo_producto = models.CharField(max_length=20, unique=True, editable=False)
    nombre_producto = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=2, choices=CATEGORIA_CHOICES)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def save(self, *args, **kwargs):
        if not self.codigo_producto:
            ultimo = Producto.objects.filter(categoria=self.categoria).order_by('-id').first()
            if ultimo and ultimo.codigo_producto:
                ultimo_num = int(ultimo.codigo_producto.replace(self.categoria, ''))
                nuevo_num = ultimo_num + 1
            else:
                nuevo_num = 1
            self.codigo_producto = f"{self.categoria}{nuevo_num:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.codigo_producto} - {self.nombre_producto}"

class DisponibilidadEntrega(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='tiempo_entrega')
    dias_entrega = models.IntegerField(help_text="Días estimados de entrega")
    fecha_disponibilidad = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        db_table = 'disponibilidad_entrega'
        verbose_name = 'Disponibilidad de Entrega'
        verbose_name_plural = 'Disponibilidades de Entrega'
    
    def __str__(self):
        return f"{self.producto.codigo_producto} - {self.dias_entrega} días"

