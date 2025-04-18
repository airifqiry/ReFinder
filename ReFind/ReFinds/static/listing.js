function countWords(textarea) {
    const words = textarea.value.trim().split(/\s+/);
    const wordCount = words[0] === "" ? 0 : words.length;
    const counter = document.getElementById("wordCount");
    counter.textContent = `${wordCount}/50 думи`;
    if (wordCount > 50) {
      textarea.value = words.slice(0, 50).join(" ");
      counter.textContent = "50/50 думи";
    }
  }
  
  function fillLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(pos => {
        const coords = `${pos.coords.latitude},${pos.coords.longitude}`;
        document.getElementById("locationField").value = coords;
      });
    }
  }
  function fillLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(pos => {
        const coords = `${pos.coords.latitude},${pos.coords.longitude}`;
        document.getElementById("locationField").value = coords;
        document.getElementById("id_latitude").value = pos.coords.latitude;
        document.getElementById("id_longitude").value = pos.coords.longitude;
      });
    }
  }
  