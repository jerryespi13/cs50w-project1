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
