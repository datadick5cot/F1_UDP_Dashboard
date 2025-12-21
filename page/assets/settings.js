

async function fetchsettings() {
  try {
    const res = await fetch("http://localhost:8000/config");
    const data = await res.json();

    document.getElementById("IPAddress").textContent = data.IPaddress ?? "--";
    } catch (err) {

    console.error("Failed to fetch settings:", err);
}
}
fetchsettings();

const gameMap = {'F1 2024' : 2024,
                  'F1 2025' : 2025}

// settings drop down 
const selector = document.getElementById("selector");
if (selector) {
  selector.addEventListener("change", function () {
    const selectedValue = this.value;
    document.getElementById("udpFormat").textContent = gameMap[selectedValue];
  });
}