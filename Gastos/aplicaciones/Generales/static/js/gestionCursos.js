(function(){
    const btnEliminacion = document.querySelectorAll('.btnEliminacion');
btnEliminacion.forEach(btn => {
    btn.addEventListener('click', function(e) {
     const confirmacion = confirm("¿Está seguro de eliminar este curso?");
     if(!confirmacion){
         e.preventDefault();
     }
    });
});
})();