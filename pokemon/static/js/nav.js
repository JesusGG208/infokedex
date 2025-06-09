// En el diseño responsive hay un botón con id 'navtoggle' cuando se hace clic
document.getElementById('navtoggle').addEventListener('click', function () {
    // Cuando se activa te sale la barra de navegación entera
    document.getElementById('nav-menu').classList.toggle('active');
});
