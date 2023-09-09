// desplazar la pagina para que quede arriba la pagina de busqueda
let InputArriba = document.querySelector(".input-search");
// Desplazar la página hasta el input
InputArriba.scrollIntoView();


//  AUTOCOMPLETADO EN LA BARRA DE BUSQUEDA
const input = document.querySelector('#search');
const datalist = document.querySelector('#datalistOptions');
input.addEventListener('input', () => {
  // Limpiar el datalist
  datalist.innerHTML = '';
  // Obtenemos el valor del input
  const value = input.value;
  // Hacemos la llamada fetch a la ruta autocomplete
  fetch(`autocomplete?q=${value}`)
    .then(response => response.json())
    .then(data => {
      // Agregamos las opciones al datalist
      data.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        datalist.appendChild(option);
      });
    });
});
