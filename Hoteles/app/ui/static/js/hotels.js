document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("cards")) loadHotels();
  if (document.getElementById("reserveForm")) initReserve();
});

/* ---------------- LISTA HOTELES ---------------- */

async function loadHotels() {
  const API = window.API_HOTELS || "/api/hotels";
  const msg = document.getElementById("msg");
  const cards = document.getElementById("cards");

  if (!msg || !cards) return;

  msg.textContent = "Cargando...";

  const res = await fetch(API);
  const data = await safeJson(res);

  if (!res.ok || !Array.isArray(data)) {
    msg.textContent = data?.message || "Error cargando hoteles";
    return;
  }

  cards.innerHTML = "";
  data.forEach((h) => {
    const el = document.createElement("article");
    el.className = "hotel";
    el.innerHTML = `
      <div class="hotel__img" style="background-image:url('${escapeAttr(h.image_url || "")}')"></div>
      <div class="hotel__body">
        <div class="hotel__name">${escapeHtml(h.name)}</div>

        <div class="hotel__meta">
          <span>📍 ${escapeHtml(h.city)}</span>
          <span class="stars">${starsText(h.stars)}</span>
          <span>💵 ${money(h.price_per_person_night)} / persona·noche</span>
        </div>

        <div class="hotel__actions">
          <a class="btn btn--primary" href="/reserve/${h.id}">🧾 Reservar</a>
        </div>
      </div>
    `;
    cards.appendChild(el);
  });

  msg.textContent = `Total: ${data.length}`;
}

/* ---------------- RESERVA + TOTAL ESTIMADO + HEADER HOTEL ---------------- */

function initReserve() {
  const form = document.getElementById("reserveForm");
  const err = document.getElementById("error");
  const ok = document.getElementById("ok");
  if (!form) return;

  const API_RES = window.API_RESERVATIONS || "/api/reservations";
  const API_HOTELS = window.API_HOTELS || "/api/hotels";
  const hotelId = document.getElementById("hotel_id")?.value || "";

  ensureEstimateBox();

  const state = { price: 0, nights: 0, guests: 1, total: 0 };

  // header + precio
  if (hotelId) {
    loadHotelDetails(API_HOTELS, hotelId, state).then(() => {
      state.guests = Number(document.getElementById("guests")?.value || 1);
      state.nights = calcNights(
        document.getElementById("check_in")?.value,
        document.getElementById("check_out")?.value
      );
      state.total = calcTotal(state.price, state.nights, state.guests);
      updateEstimateUI(state);
    });
  } else {
    updateEstimateUI(state);
  }

  // recalcular
  const checkInEl = document.getElementById("check_in");
  const checkOutEl = document.getElementById("check_out");
  const guestsEl = document.getElementById("guests");
  const payEl = document.getElementById("payment_method");

  [checkInEl, checkOutEl, guestsEl].forEach((el) => {
    if (!el) return;
    el.addEventListener("input", () => {
      state.guests = Number(guestsEl?.value || 1);
      state.nights = calcNights(checkInEl?.value, checkOutEl?.value);
      state.total = calcTotal(state.price, state.nights, state.guests);
      updateEstimateUI(state);
    });
  });

  if (payEl) {
    payEl.addEventListener("change", () => {
      togglePaymentBoxes(payEl.value);
    });
    togglePaymentBoxes(payEl.value);
  }



  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (err) err.textContent = "";
    if (ok) ok.textContent = "";

    const payment_method = String(document.getElementById("payment_method")?.value || "").trim();
    if (!payment_method) {
      if (err) err.textContent = "Selecciona un método de pago.";
      return;
    }

    // ✅ si es tarjeta, validar campos (frontend demo)
    if (payment_method === "card") {
      const v = validateCardFields();
      if (!v.ok) {
        if (err) err.textContent = v.message;
        return;
      }
    }

    const payload = {
      hotel_id: hotelId,
      full_name: (document.getElementById("full_name")?.value || "").trim(),
      email: (document.getElementById("email")?.value || "").trim(),
      check_in: document.getElementById("check_in")?.value || "",
      check_out: document.getElementById("check_out")?.value || "",
      guests: Number(document.getElementById("guests")?.value || 1),
      payment_method, // ✅ se guarda en DB
      // ❌ no mandes total_paid; backend lo calcula
    };

    const res = await fetch(API_RES, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await safeJson(res);

    if (res.status === 401) {
      window.location.href = `/login?next=/reserve/${hotelId}`;
      return;
    }

    if (!res.ok) {
      if (err) err.textContent = data?.message || "Error";
      return;
    }

    if (ok) ok.textContent = "✅ Reserva creada. Abriendo comprobante...";
    setTimeout(() => {
      window.location.href = `/reservation/${data.id}`;
    }, 300);
  });
}

/* ---------- Tarjeta UI + validación demo ---------- */

function togglePaymentBoxes(method) {
  const card = document.getElementById("cardBox");
  const transfer = document.getElementById("transferBox");
  const cash = document.getElementById("cashBox");

  if (card) card.style.display = method === "card" ? "block" : "none";
  if (transfer) transfer.style.display = method === "transfer" ? "block" : "none";
  if (cash) cash.style.display = method === "cash" ? "block" : "none";
}



function validateCardFields() {
  const name = (document.getElementById("card_name")?.value || "").trim();
  const numberRaw = (document.getElementById("card_number")?.value || "").replace(/\s+/g, "");
  const exp = (document.getElementById("card_exp")?.value || "").trim();
  const cvv = (document.getElementById("card_cvv")?.value || "").trim();

  if (!name) return { ok: false, message: "Ingresa el nombre de la tarjeta." };

  // número 13-19 dígitos
  if (!/^\d{13,19}$/.test(numberRaw)) {
    return { ok: false, message: "Número de tarjeta inválido." };
  }

  // exp MM/AA
  if (!/^\d{2}\/\d{2}$/.test(exp)) {
    return { ok: false, message: "Fecha de vencimiento inválida (MM/AA)." };
  }
  const [mmStr, yyStr] = exp.split("/");
  const mm = Number(mmStr), yy = Number(yyStr);
  if (mm < 1 || mm > 12) return { ok: false, message: "Mes de vencimiento inválido." };

  // cvv 3-4
  if (!/^\d{3,4}$/.test(cvv)) {
    return { ok: false, message: "CVV inválido." };
  }

  return { ok: true };
}


async function loadHotelDetails(API_HOTELS, hotelId, state) {
  try {
    const res = await fetch(`${API_HOTELS}/${hotelId}`);
    const data = await safeJson(res);
    if (!res.ok || !data) return;

    state.price = Number(data.price_per_person_night) || 0;

    const title = document.getElementById("hotelTitle");
    const meta = document.getElementById("hotelMeta");
    const price = document.getElementById("hotelPrice");

    if (title) title.textContent = data.name ? data.name : "Hotel";
    if (meta) {
      const city = data.city ? `📍 ${data.city}` : "";
      const stars = data.stars != null ? ` • ${starsText(data.stars)}` : "";
      meta.textContent = `${city}${stars}`.trim();
    }
    if (price) price.textContent = `💵 ${money(state.price)} / persona·noche`;
  } catch {
    // silencio
  }
}

/* ---------------- ESTIMACIÓN UI ---------------- */

function ensureEstimateBox() {
  const form = document.getElementById("reserveForm");
  if (!form) return;
  if (document.getElementById("estimateBox")) return;

  const box = document.createElement("div");
  box.id = "estimateBox";
  box.style.marginTop = "12px";
  box.style.padding = "12px";
  box.style.border = "1px solid rgba(255,255,255,0.12)";
  box.style.borderRadius = "14px";
  box.style.background = "rgba(255,255,255,0.05)";

  box.innerHTML = `
    <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
      <span class="badge badge--info" id="estPrice">💵 Precio: —</span>
      <span class="badge badge--info" id="estNights">🌙 Noches: —</span>
      <span class="badge badge--ok" id="estTotal">🧾 Total estimado: —</span>
    </div>
  `;
  form.appendChild(box);
}

function updateEstimateUI(state) {
  const estPrice = document.getElementById("estPrice");
  const estNights = document.getElementById("estNights");
  const estTotal = document.getElementById("estTotal");

  if (estPrice) estPrice.textContent = `💵 Precio: ${state.price ? money(state.price) : "—"} / persona·noche`;
  if (estNights) estNights.textContent = `🌙 Noches: ${state.nights || "—"}`;
  if (estTotal) estTotal.textContent = `🧾 Total estimado: ${state.total ? money(state.total) : "—"}`;
}

/* ---------------- CÁLCULOS ---------------- */

function calcNights(checkInStr, checkOutStr) {
  if (!checkInStr || !checkOutStr) return 0;
  const inDate = new Date(checkInStr + "T00:00:00");
  const outDate = new Date(checkOutStr + "T00:00:00");
  if (Number.isNaN(inDate.getTime()) || Number.isNaN(outDate.getTime())) return 0;

  const diffMs = outDate - inDate;
  const nights = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  return nights > 0 ? nights : 0;
}

function calcTotal(price, nights, guests) {
  const p = Number(price) || 0;
  const n = Number(nights) || 0;
  const g = Number(guests) || 0;
  if (p <= 0 || n <= 0 || g <= 0) return 0;
  return p * n * g;
}

/* ---------------- HELPERS ---------------- */

async function safeJson(res) {
  try { return await res.json(); } catch { return null; }
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

// para url dentro de style=""
function escapeAttr(s) {
  return String(s).replaceAll('"', "%22").replaceAll("'", "%27");
}
