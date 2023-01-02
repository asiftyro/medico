function remoteSearch(text, cb) {
  var remoteSearchUrl = `/medicine/search?q=${text}`;
  fetch(remoteSearchUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((response) => {
      cb(response);
    });
}

var tribute = new Tribute({
  collection: [{
    trigger: '@',
    selectTemplate: function(item) {
      return item.original.value;
    },
    lookup: 'key',
    values: function(text, cb) {
      remoteSearch(text, med => cb(med));
    },
    allowSpaces: true,
    menuItemLimit: 15,
    loadingItemTemplate:'<span>Loading...</span>',
    menuItemTemplate: function (item) {
      return item.original.key + " - " + item.original.value;
    },
  }]
});
