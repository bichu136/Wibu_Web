var api_link = baseUrl+"api/AnimeScorePredictor"
function DoneClick()
{
    var genre_collection = document.getElementById("genre_collection").children[0]
    var studio_collection = document.getElementById("studio_collection").children[0]
    var source_collection = document.getElementById("source_collection").children[0]
    var x = []
    for (let index = 0; index < source_collection.children.length; index++) {
        if (source_collection.children[index].children[0].checked)
            x.push(1)
        else
        {
            x.push(0)
        }        
    }
    for (let index = 0; index < studio_collection.children.length; index++) {
        if (studio_collection.children[index].children[0].checked)
            x.push(1)
        else
        {
            x.push(0)
        }        
    }
    for (let index = 0; index < genre_collection.children.length; index++) {
        if (genre_collection.children[index].children[0].checked)
            x.push(1)
        else
        {
            x.push(0)
        }        
    }
    fetch(api_link,
        {method:"POST",
         headers:{ 'Content-Type': 'application/json' },
         body: JSON.stringify({ array:x }) }).then(result=>result.json()).then(data =>alert(data))
}