$(document).ready(function(){
  jQuery.get('https://api.github.com/repos/codethesaurus/codethesaur.us/contributors?accept=application/vnd.github.v3+json&per_page=100&anon=1', function(data, status){
    $("#contributors").text(data.length)
  })
})