
async function sendSignal() {
  const apiKey = document.getElementById("apiKey").value;
  const symbol = document.getElementById("symbol").value;
  const signal = document.getElementById("signal").value;
  const confidence = parseFloat(document.getElementById("confidence").value);

  const responseBox = document.getElementById("responseBox");

  const payload = {
    symbol,
    signal,
    confidence,
    strategy: "quantumx"
  };

  try {
    const res = await fetch("https://quantumx-production.up.railway.app/webhook/quantumx", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + apiKey
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    responseBox.innerText = JSON.stringify(data, null, 2);
  } catch (err) {
    responseBox.innerText = "Error: " + err.message;
  }
}
