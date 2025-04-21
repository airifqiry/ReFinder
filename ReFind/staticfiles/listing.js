// listing.js

// Функция за броене на думи в описанието
function countWords(textarea) {
  const text = textarea.value.trim();
  const words = text ? text.split(/\s+/) : [];
  const wordCount = words.length;
  document.getElementById('wordCount').textContent = `${wordCount}/50 думи`;
  if (wordCount > 50) {
      textarea.value = words.slice(0, 50).join(' ');
      document.getElementById('wordCount').textContent = `50/50 думи`;
  }
}

// Функция за автоматично местоположение
function fillLocation() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
          var lat = position.coords.latitude;
          var lng = position.coords.longitude;

          // Центрирай картата към текущото местоположение
          map.setView([lat, lng], 13);

          // Премахни предишния маркер, ако има такъв
          if (marker) {
              map.removeLayer(marker);
          }

          // Добави маркер на текущото местоположение
          marker = L.marker([lat, lng]).addTo(map);

          // Попълни полетата за ширина и дължина
          document.getElementById('id_latitude').value = lat;
          document.getElementById('id_longitude').value = lng;

          // Опитай да вземеш адреса чрез Nominatim API
          fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
              .then(response => response.json())
              .then(data => {
                  if (data && data.display_name) {
                      document.getElementById('locationField').value = data.display_name;
                  }
              })
              .catch(error => {
                  console.error('Грешка при обръщане на геокодиране:', error);
              });
      }, function(error) {
          alert("Не можахме да вземем вашето местоположение. Моля, изберете място на картата.");
      });
  } else {
      alert("Геолокацията не се поддържа от този браузър. Моля, изберете място на картата.");
  }
}

// Инициализация на картата, когато DOM е готов
document.addEventListener('DOMContentLoaded', function() {
  console.log("DOM е готов, инициализираме картата...");

  // Проверка дали елементът съществува
  const mapElement = document.getElementById('map');
  if (!mapElement) {
      console.error("Елемент с ID 'map' не е намерен!");
      return;
  }

  // Инициализация на картата
  window.map = L.map('map').setView([42.6977, 23.3219], 13); // Център в София по подразбиране
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
  }).addTo(map);

  console.log("Картата е инициализирана успешно!");

  // Променлива за маркера
  window.marker = null;

  // При клик върху картата
  map.on('click', function(e) {
      // Премахни предишния маркер, ако има такъв
      if (marker) {
          map.removeLayer(marker);
      }

      // Добави нов маркер на кликнатото място
      marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(map);

      // Попълни полетата за ширина и дължина
      document.getElementById('id_latitude').value = e.latlng.lat;
      document.getElementById('id_longitude').value = e.latlng.lng;

      // Опитай да вземеш адреса чрез Nominatim API
      fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${e.latlng.lat}&lon=${e.latlng.lng}`)
          .then(response => response.json())
          .then(data => {
              if (data && data.display_name) {
                  document.getElementById('locationField').value = data.display_name;
              }
          })
          .catch(error => {
              console.error('Грешка при обръщане на геокодиране:', error);
          });
  });

  // Валидация преди изпращане на формата
  document.getElementById('adForm').addEventListener('submit', function(e) {
      const lat = document.getElementById('id_latitude').value;
      const lng = document.getElementById('id_longitude').value;
      if (!lat || !lng) {
          e.preventDefault();
          alert('Моля, изберете място на картата или използвайте автоматично местоположение.');
      }
  });
});