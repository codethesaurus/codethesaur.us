$(document).ready(function () {
  let i = 1;
  let length = 0;
  const timer = async () => {
    jQuery
      .get(
        `https://api.github.com/repos/codethesaurus/codethesaur.us/contributors?accept=application/vnd.github.v3+json&per_page=100&page=${i}&anon=1`
      )
      .then((data) => {
        length += data.length;
        i++;
        if (data.length === 0) {
          $("#contributors").text(length);
        } else {
          setTimeout(timer, 500);
        }
      });
  };
  timer();
});
