fetch('/signals')
  .then(res => res.json())
  .then(data => {
    document.getElementById("signals").innerText = JSON.stringify(data, null, 2);
  });
