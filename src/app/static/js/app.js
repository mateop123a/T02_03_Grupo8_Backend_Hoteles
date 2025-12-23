const API_BASE = ""; 

function getToken() {
  return localStorage.getItem("token");
}

function setToken(t) {
  localStorage.setItem("token", t);
}

function clearToken() {
  localStorage.removeItem("token");
}

function requireAuth() {
  const t = getToken();
  if (!t) window.location.href = "/ui/login";
}

function logout() {
  clearToken();
  window.location.href = "/ui/login";
}

async function apiFetch(path, { method = "GET", body = null, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });

  // Si el token expiró o no hay token
  if (res.status === 401) {
    clearToken();
    window.location.href = "/ui/login";
    return;
  }

  // Respuesta puede ser JSON o HTML de error
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; }
  catch { data = { raw: text }; }

  if (!res.ok) {
    const msg = data?.error || data?.message || "Error";
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }

  return data;
}

function showMsg(elId, message, type = "success") {
  const el = document.getElementById(elId);
  if (!el) return;
  el.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;
}

function valRequired(v, name) {
  if (!v || String(v).trim() === "") throw new Error(`${name} es requerido.`);
}

function valDateISO(v, name) {
  // YYYY-MM-DD
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) throw new Error(`${name} debe ser YYYY-MM-DD.`);
}

function valPositiveNumber(v, name) {
  const n = Number(v);
  if (!Number.isFinite(n) || n <= 0) throw new Error(`${name} debe ser > 0.`);
  return n;
}
