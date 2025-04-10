
    AOS.init();

    document.getElementById('search').addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        window.location.href = 'search.html?query=' + encodeURIComponent(this.value);
      }
    });

    const map = L.map('map').setView([42.6977, 23.3219], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const items = [
      { name: "🎒 Изгубена раница", coords: [42.698, 23.322] },
      { name: "🔑 Ключове с червен ключодържател", coords: [42.694, 23.319] }
    ];

    items.forEach(item => {
      L.marker(item.coords).addTo(map)
        .bindPopup(`<b>${item.name}</b>`);
    });
