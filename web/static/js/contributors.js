document.addEventListener("DOMContentLoaded", function () {
    var contributorsRequest = new XMLHttpRequest();

    contributorsRequest.open(
        "GET",
        "https://api.github.com/repos/codethesaurus/codethesaur.us/contributors?accept=application/vd.github.v3+json&per_page=1&anon=1"
    );

    contributorsRequest.send();

    contributorsRequest.onload = function () {
        if (contributorsRequest.status != 200) {
            document.querySelector("#contributors").innerHTML = "multiple";
            return;
        }

        try {
            let header = contributorsRequest.getResponseHeader("link");
            let contributors = header.match(/page=(\d+)>; rel=\"last\"/)[1]
            document.querySelector("#contributors").innerHTML = contributors;
        } catch {
            document.querySelector("#contributors").innerHTML = "multiple";
        }
    };

    contributorsRequest.onerror = function () {
        document.querySelector("#contributors").innerHTML = "multiple";
    };

    var repoRequest = new XMLHttpRequest();
    repoRequest.open(
        "GET",
        "https://api.github.com/repos/codethesaurus/codethesaur.us"
    );
    repoRequest.send();

    repoRequest.onload = function () {
        if (repoRequest.status === 200) {
            let repoData = JSON.parse(repoRequest.responseText);
            let lastUpdate = new Date(repoData.pushed_at);
            let options = { year: 'numeric', month: 'long', day: 'numeric' };
            document.querySelector("#last-update").innerHTML = lastUpdate.toLocaleDateString(undefined, options);
        }
    };
});
