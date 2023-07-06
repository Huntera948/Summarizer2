var axios = require("axios").default;

const your_key_1 = "your_key_1";

var options = {
  method: "GET",
  url: "https://api.newscatcherapi.com/v2/search",
  params: { q: "Bitcoin", lang: "en", sort_by: "relevancy", page: "1" },
  headers: {
    "x-api-key": "your_key_1",
  },
};

axios
  .request(options)
  .then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.error(error);
  });
