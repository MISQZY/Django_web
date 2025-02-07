document.getElementById("fetch-data-btn").addEventListener("click", function() {
    fetch("{% url 'collect_vpn_data' %}", {
      method: "POST",
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.log(error));
  });