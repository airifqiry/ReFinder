AOS.init();

document.addEventListener("DOMContentLoaded", function () {
  console.log("📦 DOM напълно зареден");




  // КАРТАТА
  const map = L.map('map').setView([42.6977, 23.3219], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // ТЕСТОВИ ОБЯВИ
  const items = [
    { name: "🎒 Изгубена раница", coords: [42.698, 23.322] },
    { name: "🔑 Ключове с червен ключодържател", coords: [42.694, 23.319] }
  ];

  items.forEach(item => {
    L.marker(item.coords).addTo(map)
      .bindPopup(`<b>${item.name}</b>`);
  });

  // ГЕОЛОКАЦИЯ
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        map.setView([lat, lng], 15);

        L.marker([lat, lng]).addTo(map)
          .bindPopup("📍 Тук се намираш в момента!")
          .openPopup();

        L.circle([lat, lng], {
          color: 'blue',
          fillColor: '#30f',
          fillOpacity: 0.15,
          radius: position.coords.accuracy
        }).addTo(map);
      },
      function(error) {
        console.error("❌ Грешка при определяне на локацията:", error);
      }
    );
  } else {
    alert("❗ Браузърът не поддържа геолокация.");
  }
});


  fetch('/ads-json/')
    .then(response => response.json())
    .then(data => {
      data.forEach(ad => {
        const marker = L.marker([ad.latitude, ad.longitude]).addTo(map);
        marker.bindPopup(`
          <b>${ad.title}</b><br>
          ${ad.description}<br>
          ${ad.image ? `<img src="${ad.image}" width="100">` : ''}
        `);
      });
    });

