document.addEventListener("DOMContentLoaded", loadReservation);

async function loadReservation() {
  const id = window.RES_ID;
  const box = document.getElementById("rBox");
  if (!id || !box) return;

  const res = await fetch(`/api/reservations/${id}`);
  const data = await safeJson(res);

  if (!res.ok) {
    box.innerHTML = `<p class="error">${escapeHtml(data?.message || "Reserva no encontrada")}</p>`;
    return;
  }

  box.innerHTML = `
    <div class="hotel__meta" style="margin-top:0;">
      <span class="badge badge--info">🆔 ${escapeHtml(shortId(data.id))}</span>
      <span class="badge badge--info">👤 ${escapeHtml(data.full_name)}</span>
      <span class="badge badge--info">📧 ${escapeHtml(data.email)}</span>
    </div>

    <div style="margin-top:12px;">
      <p class="muted" style="margin:0 0 8px;">Detalles</p>
      <div class="hotel__meta">
        <span class="badge badge--info">🏨 Hotel ID: ${escapeHtml(shortId(data.hotel_id))}</span>
        <span class="badge badge--info">📅 ${escapeHtml(data.check_in)} → ${escapeHtml(data.check_out)}</span>
        <span class="badge badge--ok">👥 ${escapeHtml(String(data.guests))} huéspedes</span>
        <span class="badge badge--info">🌙 ${escapeHtml(String(data.nights ?? "—"))} noches</span>
        <span class="badge badge--ok">💵 Total: ${money(data.total_paid)}</span>
      </div>
    </div>
  `;
}

function shortId(id){ if(!id) return ""; const s=String(id); return s.length>10? `${s.slice(0,8)}...` : s; }
function money(v){ const n=Number(v); if(!Number.isFinite(n)) return "—"; return n.toLocaleString("es-EC",{style:"currency",currency:"USD"}); }
async function safeJson(res){ try { return await res.json(); } catch { return null; } }
function escapeHtml(s){ return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;"); }
