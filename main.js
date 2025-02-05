const form = document.getElementById("form");
const floatingInput = document.getElementById("floatingInput");
const floatingTextarea = document.getElementById("floatingTextarea");

let ws = new WebSocket("ws://localhost:5000");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (ws.readyState === WebSocket.OPEN) {
    const data = {
      date: new Date(),
      username: floatingInput.value,
      message: floatingTextarea.value,
    };
    ws.send(JSON.stringify(data));
    floatingInput.value = null;
    floatingTextarea.value = null;
  } else {
    console.error("WebSocket is not open. Ready state: " + ws.readyState);
  }
});

ws.onopen = (e) => {
  console.log("Hello WebSocket!");
};

ws.onmessage = (e) => {
  console.log(e.data);
  text = e.data;
};

ws.onclose = (e) => {
  console.log("WebSocket is closed now.");
};

ws.onerror = (e) => {
  console.error("WebSocket error observed:", e);
};
