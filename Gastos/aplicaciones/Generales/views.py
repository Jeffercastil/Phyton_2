from django.shortcuts import render, redirect
from .models import Curso #Base de datos
from django.contrib import messages
# Create your views here.
def home(request):
    cursosListados = Curso.objects.all() # mostrara todos los cursos
    messages.success(request, '¡Cursos listados!')
    return render(request, 'gestionCursos.html', {'cursos': cursosListados}) # El nombre de curso no tiene que ser igual 
#Se enlista las plantillas y se muestran los cursos en la pagina

def registrarCurso(request):
    codigo = request.POST.get('txtCodigo')
    nombre = request.POST.get('txtNombre')
    creditos = request.POST.get('NumCreditos')
    curso = Curso.objects.create(codigo = codigo, nombre = nombre, creditos = creditos)
    #Redirecciona a la pagina principal despues de guardar el curso
    messages.success(request, '¡Curso registrado!')
    return redirect('/')

def edicionCurso(request,codigo):
    curso = Curso.objects.get(codigo = codigo)
    return render(request, 'edicionCurso.html', {'curso': curso})

def editarCurso(request):
    if request.method == 'POST':
        codigo = request.POST.get('txtCodigo')  # CORRECCIÓN: usar .get()
        nombre = request.POST.get('txtNombre')  # CORRECCIÓN: usar .get()
        creditos = request.POST.get('NumCreditos')  # CORRECCIÓN: usar .get()
        
        curso = Curso.objects.get(codigo=codigo)
        curso.nombre = nombre
        curso.creditos = creditos
        curso.save()
        messages.success(request, '¡Curso actualizado!')
    return redirect('/')

def eliminarCurso(request,codigo):
    curso = Curso.objects.get(codigo = codigo) 
    curso.delete()
    messages.success(request, '¡Curso eliminado!')
    return redirect('/')

