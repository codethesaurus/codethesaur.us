document.addEventListener("DOMContentLoaded", function () {
  var currentPage = 1;
  var numberOfContributors = 0;

  function getContributors() {
    var contributorsRequest = new XMLHttpRequest();

    contributorsRequest.open(
      "GET",
      "https://api.github.com/repos/codethesaurus/codethesaur.us/contributors?accept=application/vd.github.v3+json&per_page=100&page=" +
        currentPage +
        "&anon=1"
    );

    contributorsRequest.send();

    contributorsRequest.onload = function () {
      if (contributorsRequest.status != 200) {
        document.querySelector("#contributors").innerHTML = "multiple";
        return;
      }

      try {
        var response = JSON.parse(contributorsRequest.response);

        numberOfContributors += response.length;

        if (response.length < 100) {
          document.querySelector("#contributors").innerHTML =
            numberOfContributors;
        } else {
          currentPage++;
          getContributors();
        }
      } catch {
        document.querySelector("#contributors").innerHTML = "multiple";
      }
    };

    contributorsRequest.onerror = function () {
      document.querySelector("#contributors").innerHTML = "multiple";
    };
  }

  getContributors();
});
