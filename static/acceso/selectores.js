const selectoresDataElement = document.getElementById('selectores-data');
const selectoresJSON = JSON.parse(selectoresDataElement.dataset.selectores);

// obtenemos componentes de selectores
const selectorSucursal = document.getElementById('selectorSucursal');
const selectorCaja = document.getElementById('selectorCaja');


function llenarSelectorSucursal(){
  /*
    Actualiza los valores del selector de sucursal
  */

  selectorSucursal.innerHTML = '';
  // iteramos los elementos del JSON

  for(const tienda in selectoresJSON){
    if(selectoresJSON.hasOwnProperty(tienda)){

      const option = document.createElement('option');
      option.value = selectoresJSON[tienda].index_sucursal; 
      option.textContent = tienda; // Mostramos la clave como texto
      selectorSucursal.appendChild(option);

    }// fin if selectoresJSON
  }// fin for json

  // Seleccionar la primera clave por defecto y actualizar el segundo selector
  if (Object.keys(selectoresJSON).length > 0) {
    const primeraTienda = Object.keys(selectoresJSON)[0];
    actualizarSelectorCaja(primeraTienda);
  }
}


function actualizarSelectorCaja(tiendaSeleccionada) {
  /* 
    Se actualizan los valores del selector caja
  */
    selectorCaja.innerHTML = '';

    if (selectoresJSON.hasOwnProperty(tiendaSeleccionada) && selectoresJSON[tiendaSeleccionada].opciones) {
      selectoresJSON[tiendaSeleccionada].opciones.forEach(opcion => {
        // Adaptamos esto según la estructura de tus objetos en 'opciones'
        console.log(opcion)
        const option = document.createElement('option');
        option.value = opcion.index_caja; // Puedes usar el objeto completo como valor o una propiedad específica
        option.textContent = opcion.caja ; // Mostrar 'caja' o 'producto' si existen, sino el objeto completo
        selectorCaja.appendChild(option);
      });
    }
}


selectorSucursal.addEventListener('change', function() {
  const tiendaSeleccionada = this.value;
  actualizarSelectorCaja(tiendaSeleccionada);
});

// Llenar el primer selector al cargar la página
llenarSelectorSucursal();
