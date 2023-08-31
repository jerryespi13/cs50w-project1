$(function(){
    $.ajax({
        url:'/listalibros',
        success: function(response){
            /*console.log("La api responde bien", response)*/
            $('#search').autocomplete({
                source:response["libros"],
                minLength: 5
            })
        }
    })
})