
var search_text = ""
$("#search-button").click(function(){
    var value = $("#search-box").val();
    var form = new FormData();
    form.append("query", value);
    var settings = {
    "url": "/api/get_searched_list",
    "method": "POST",
    "timeout": 0,
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
  };
    $.ajax(settings).done(function (response) {
        window.location.href = response;
    });
});
