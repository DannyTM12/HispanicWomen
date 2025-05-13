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
  claves = Object.keys(selectoresJSON);

  claves.forEach(clave => {
    
    if(selectoresJSON[clave].length > 0){
      const option = document.createElement('option');
      option.value = selectoresJSON[clave].index_sucursal;
      option.textContent = clave;
      selectorSucursal.appendChild(option);
    }
    
  });

  // Seleccionar la primera clave por defecto y actualizar el segundo selector
  if (claves.length > 0) {
    actualizarSelectorCaja(claves[0]);
  }
}


function actualizarSelectorCaja(claveSeleccionada) {
  /* 
    Se actualizan los valores del selector caja
  */
  selectorCaja.innerHTML = ''; // Limpiar opciones previas
  if (selectoresJSON.hasOwnProperty(claveSeleccionada)) {
    const valores = selectoresJSON[claveSeleccionada];
    
    for(index in valores){
      const option = document.createElement('option');
      option.value = valores[index].index_caja;
      option.textContent = valores[index].nombre;
      selectorCaja.appendChild(option);
    }
  }
}


selectorSucursal.addEventListener('change', function() {
  const claveSeleccionada = this.value;
  actualizarSelectorCaja(claveSeleccionada);
});

llenarSelectorSucursal();
