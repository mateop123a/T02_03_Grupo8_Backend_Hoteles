document.addEventListener("DOMContentLoaded", async () => {
  await loadHotelsAdmin();
  await loadReservations();
});

/* ================= HOTELS (ADMIN) ================= */

async function loadHotelsAdmin() {
  const API = window.API_HOTELS || "/api/hotels";
  const msg = document.getElementById("adminMsg");
  const cards = document.getElementById("adminCards");

  msg.textContent = "Cargando hoteles...";
  const res = await fetch(API);
  const data = await res.json();

  if (!res.ok) {
    msg.textContent = data.message || "Error";
    return;
  }

  cards.innerHTML = "";
  data.forEach(h => {
    const el = document.createElement("article");
    el.className = "hotel";
    el.innerHTML = `
      <div class="hotel__img" style="background-image:url('${escapeHtml(getImg(h))}')"></div>
      <div class="hotel__info">
        <div class="hotel__name">${escapeHtml(h.name)}</div>

        <div class="hotel__meta">
          <span>📍 ${escapeHtml(h.city)}</span>
          <span class="stars">${starsText(h.stars)}</span>
          <span class="price">💵 ${money(h.price_per_person_night)} / persona·noche</span>
        </div>

        <div class="hotel__actions">
          <a class="btn btn--ghost" href="/admin/hotels/${h.id}/edit">✏️ Editar</a>
          <button class="btn btn--danger" data-id="${h.id}">🗑️ Eliminar</button>
        </div>
      </div>
    `;
    cards.appendChild(el);
  });

  // Eliminar hotel
  cards.querySelectorAll("button[data-id]").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-id");
      if (!confirm("¿Eliminar hotel?")) return;

      const del = await fetch(`${API}/${id}`, { method: "DELETE" });
      const out = await safeJson(del);

      if (!del.ok) {
        msg.textContent = out?.message || "Error";
        return;
      }
      loadHotelsAdmin();
    });
  });

  msg.textContent = `Total hoteles: ${data.length}`;
}

/* ================= RESERVATIONS ================= */

async function loadReservations() {
  const API_RES = window.API_RESERVATIONS || "/api/reservations";
  const API_HOTELS = window.API_HOTELS || "/api/hotels";

  const msg = document.getElementById("resMsg");
  const box = document.getElementById("reservations");

  msg.textContent = "Cargando reservas...";

  // 1) Traer reservas (solo admin)
  const res = await fetch(API_RES);
  const data = await safeJson(res);

  if (!res.ok) {
    msg.textContent = data?.message || "No autorizado";
    box.innerHTML = "";
    return;
  }

  // 2) Traer hoteles para mapear id -> nombre
  const resHotels = await fetch(API_HOTELS);
  const hotels = await safeJson(resHotels);

  const hotelMap = new Map();
  if (resHotels.ok && Array.isArray(hotels)) {
    hotels.forEach(h => {
      if (h?.id) hotelMap.set(String(h.id), String(h.name || "Hotel"));
    });
  }

  // 3) Pintar tabla con nombre del hotel
  box.innerHTML = `
    <div class="tableWrap">
      <table class="table">
        <thead>
          <tr>
            <th>Hotel</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Check-in</th>
            <th>Check-out</th>
            <th>Huéspedes</th>
            <th>Total pagado</th>
          </tr>
        </thead>
        <tbody>
          ${data.map(r => {
            const hid = String(r.hotel_id || "");
            const hotelName = hotelMap.get(hid) || `Hotel (${shortId(hid)})`;

            return `
              <tr>
                <td>
                  <div style="display:flex; flex-direction:column; gap:4px;">
                    <strong>${escapeHtml(hotelName)}</strong>
                    <span class="mono" style="opacity:.7;">${escapeHtml(shortId(hid))}</span>
                  </div>
                </td>
                <td>${escapeHtml(r.full_name)}</td>
                <td class="mono">${escapeHtml(r.email)}</td>
                <td><span class="badge badge--info">📅 ${escapeHtml(r.check_in)}</span></td>
                <td><span class="badge badge--info">📅 ${escapeHtml(r.check_out)}</span></td>
                <td><span class="badge badge--ok">👥 ${escapeHtml(String(r.guests))}</span></td>
                <td><span class="badge badge--ok">💵 ${money(r.total_paid)}</span></td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
    </div>
  `;

  msg.textContent = `Total reservas: ${data.length}`;
}


/* ================= HELPERS ================= */

function shortId(id) {
  if (!id) return "";
  const s = String(id);
  return s.length > 12 ? `${s.slice(0, 8)}...${s.slice(-4)}` : s;
}

function starsText(n) {
  n = Math.max(0, Math.min(5, Number(n) || 0));
  return "★".repeat(n) + "☆".repeat(5 - n);
}

function money(v) {
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  return n.toLocaleString("es-EC", { style: "currency", currency: "USD" });
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

function getImg(h){
  return (h && h.image_url) ? String(h.image_url) : hotelImage(h);
}


function hotelImage(h) {
  const city = (h.city || "").toLowerCase();
  let keyword = "hotel,lobby";
  if (city.includes("quito")) keyword = "quito,ecuador,hotel";
  else if (city.includes("guayaquil")) keyword = "guayaquil,ecuador,hotel";
  else if (city.includes("cuenca")) keyword = "cuenca,ecuador,hotel";
  return `https://source.unsplash.com/800x600/?${encodeURIComponent(keyword)}&sig=${Math.abs(hash((h.id || "") + keyword))}`;
}

function hash(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h << 5) - h + s.charCodeAt(i);
  return h;
}

async function safeJson(res) {
  try { return await res.json(); } catch { return null; }
}

function money(v){
  const n = Number(v);
  if (!Number.isFinite(n) || n <= 0) return "—";
  return n.toLocaleString("es-EC", { style: "currency", currency: "USD" });
}
