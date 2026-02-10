const API = window.API_BASE || "/api/hotels";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("hotelForm");
  if (!form) return;

  form.addEventListener("submit", onSubmit);

  const isEdit = window.MODE === "edit" && window.HOTEL_ID;
  if (isEdit) loadHotel(window.HOTEL_ID);
});

async function loadHotel(id) {
  const res = await fetch(`${API}/${id}`);
  const data = await safeJson(res);

  if (!res.ok) return showError(data?.message || "Error cargando hotel");

  document.getElementById("name").value = data.name ?? "";
  document.getElementById("city").value = data.city ?? "";
  document.getElementById("stars").value = data.stars ?? "";
  document.getElementById("image_url").value = data.image_url ?? "";


  // ✅ NUEVO: precio por persona/noche
  const priceEl = document.getElementById("price_per_person_night");
  if (priceEl) priceEl.value = data.price_per_person_night ?? "";
}

async function onSubmit(e) {
  e.preventDefault();
  clearError();

  const priceRaw = document.getElementById("price_per_person_night")?.value;

  const payload = {
    name: document.getElementById("name").value.trim(),
    city: document.getElementById("city").value.trim(),
    stars: Number(document.getElementById("stars").value),
    price_per_person_night: Number(priceRaw),
    image_url: document.getElementById("image_url").value.trim(),
  };

  // Validación rápida en frontend (evita mandar NaN)
  if (!payload.name) return showError("name es requerido");
  if (!payload.city) return showError("city es requerido");
  if (!Number.isFinite(payload.stars)) return showError("stars debe ser un número");
  if (payload.stars < 1 || payload.stars > 5) return showError("stars debe estar entre 1 y 5");

  if (!Number.isFinite(payload.price_per_person_night))
    return showError("price_per_person_night debe ser un número");
  if (payload.price_per_person_night <= 0)
    return showError("price_per_person_night debe ser mayor a 0");

  const isEdit = window.MODE === "edit" && window.HOTEL_ID;

  const res = await fetch(isEdit ? `${API}/${window.HOTEL_ID}` : API, {
    method: isEdit ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await safeJson(res);
  if (!res.ok) return showError(data?.message || "Error guardando");

  window.location.href = "/admin";
}

async function safeJson(res) {
  try {
    return await res.json();
  } catch {
    return null;
  }
}

function showError(text) {
  const el = document.getElementById("error");
  if (el) el.textContent = text || "";
}
function clearError() {
  showError("");
}
