document.addEventListener("DOMContentLoaded", function () {
  var contributorsRequest = new XMLHttpRequest();

  contributorsRequest.open(
    "GET",
    "https://api.github.com/repos/codethesaurus/codethesaur.us/contributors?accept=application/vd.github.v3+json&per_page=200&anon=1"
  );

  contributorsRequest.send();

  contributorsRequest.onload = function () {
    if (contributorsRequest.status != 200) {
      document.querySelector("#contributors").innerHTML = "multiple";
      return;
    }

    try {
      var response = JSON.parse(contributorsRequest.response);

      document.querySelector("#contributors").innerHTML = response.length;
    } catch {
      document.querySelector("#contributors").innerHTML = "multiple";
    }
  };

  contributorsRequest.onerror = function () {
    document.querySelector("#contributors").innerHTML = "multiple";
  };
});
