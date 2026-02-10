document.addEventListener("DOMContentLoaded", loadMine);

async function loadMine() {
  const API_MY = window.API_MY_RES || "/api/my-reservations";
  const API_HOTELS = window.API_HOTELS || "/api/hotels";

  const msg = document.getElementById("msg");
  const box = document.getElementById("myRes");

  if (!msg || !box) return;

  msg.textContent = "Cargando...";

  // 1) Traer mis reservas
  const resMine = await fetch(API_MY);
  const mine = await safeJson(resMine);

  if (!resMine.ok) {
    msg.textContent = mine?.message || "No autorizado";
    box.innerHTML = "";
    return;
  }

  // 2) Traer hoteles (para mapear id -> nombre)
  const resHotels = await fetch(API_HOTELS);
  const hotels = await safeJson(resHotels);

  const hotelMap = new Map();
  if (resHotels.ok && Array.isArray(hotels)) {
    hotels.forEach(h => {
      if (h?.id) hotelMap.set(String(h.id), String(h.name || "Hotel"));
    });
  }

  msg.textContent = `Total: ${mine.length}`;

  // 3) Pintar tabla
  box.innerHTML = `
    <div class="tableWrap">
      <table class="table">
        <thead>
          <tr>
            <th>Hotel</th>
            <th>Check-in</th>
            <th>Check-out</th>
            <th>Noches</th>
            <th>Huéspedes</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          ${mine.map(r => {
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
                <td><span class="badge badge--info">📅 ${escapeHtml(r.check_in)}</span></td>
                <td><span class="badge badge--info">📅 ${escapeHtml(r.check_out)}</span></td>
                <td><span class="badge badge--info">🌙 ${escapeHtml(String(r.nights ?? "—"))}</span></td>
                <td><span class="badge badge--ok">👥 ${escapeHtml(String(r.guests))}</span></td>
                <td><span class="badge badge--ok">💵 ${money(r.total_paid)}</span></td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
    </div>
  `;
}

/* ---------------- Helpers ---------------- */

function shortId(id){
  if (!id) return "";
  const s = String(id);
  return s.length > 12 ? `${s.slice(0, 8)}...${s.slice(-4)}` : s;
}

function money(v){
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  return n.toLocaleString("es-EC", { style: "currency", currency: "USD" });
}

async function safeJson(res){
  try { return await res.json(); } catch { return null; }
}

function escapeHtml(s){
  return String(s)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}
