$(document).ready(function(){
  jQuery.get('https://api.github.com/repos/codethesaurus/codethesaur.us/contributors', function(data, status){
    $("#contributors").text(data.length)
  })
})