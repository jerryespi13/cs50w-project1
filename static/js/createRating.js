function createRating(){
    let rating = document.getElementById("average").value
    total = 5
    startIcon = '<img src="/static/images/star-fill.svg" alt="Estrella llena">'
    emptIcon = '<img src="/static/images/star.svg" alt="Estrella vacia">'
    const start = startIcon.repeat(rating)
    const empty = emptIcon.repeat(Math.ceil(total - rating))
    document.getElementById("estrellas").innerHTML= start + empty
}
createRating()

//seleccion de estrella del usuario si ha dejado una reseña pero le restamos 6 porque los inputs tienen los values invertidos
// el 5 es el 1, el 4 es el 2, el 3 es el 3, el 4 es el 2, el 1 es el 5.
const puntuacion_usuario = 6 - document.querySelector("#puntuacion_usuario").value
// con ese dato formamos el id a selecionar
const estrella_selecionar = '#start' + puntuacion_usuario
// agregamos el atributo cheked al input que tiene el value igual al valor puntuado por el usuario
document.querySelector(estrella_selecionar).checked = true