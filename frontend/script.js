const API_BASE = "http://127.0.0.1:8000";
const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) }
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`);
  return body;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function renderIncidents(incidents) {
  const rows = $("incidentRows");
  const select = $("incidentSelect");
  if (!incidents.length) {
    rows.innerHTML = '<tr><td colspan="5" class="empty">No incidents found.</td></tr>';
    select.innerHTML = '<option value="">No incidents available</option>';
    return;
  }
  rows.innerHTML = incidents.map((item) => `
    <tr>
      <td>${escapeHtml(item.id)}</td>
      <td>${escapeHtml(item.title)}</td>
      <td><span class="severity ${escapeHtml(item.severity)}">${escapeHtml(item.severity.toUpperCase())}</span></td>
      <td><span class="state">${escapeHtml(item.status)}</span></td>
      <td>${item.status === "open" ? "Needs review" : "Recorded"}</td>
    </tr>`).join("");
  select.innerHTML = incidents.filter(x => x.status === "open")
    .map(x => `<option value="${escapeHtml(x.id)}">${escapeHtml(x.id)} — ${escapeHtml(x.title)}</option>`).join("");
  if (!select.options.length) select.innerHTML = '<option value="">No open incidents</option>';
}

async function loadDashboard() {
  $("refreshBtn").disabled = true;
  try {
    const [health, summary, incidents] = await Promise.all([
      api("/health"), api("/api/summary"), api("/api/incidents")
    ]);
    $("apiStatus").textContent = "Backend connected";
    $("apiMessage").textContent = `${health.service} · ${health.environment} · API healthy`;
    $("totalIncidents").textContent = summary.total_incidents;
    $("openIncidents").textContent = summary.open_incidents;
    $("recoveries").textContent = summary.successful_recoveries;
    renderIncidents(incidents);
  } catch (error) {
    $("apiStatus").textContent = "Backend unavailable";
    $("apiMessage").textContent = "Start the FastAPI backend, then press Refresh status.";
    $("incidentRows").innerHTML = `<tr><td colspan="5" class="empty">${escapeHtml(error.message)}</td></tr>`;
    $("totalIncidents").textContent = "—";
    $("openIncidents").textContent = "—";
    $("recoveries").textContent = "—";
  } finally {
    $("refreshBtn").disabled = false;
  }
}

async function requestRecovery() {
  const incidentId = $("incidentSelect").value;
  const action = $("actionSelect").value;
  const message = $("recoveryMessage");
  const button = $("recoverBtn");
  if (!incidentId) {
    message.textContent = "Select an open incident first.";
    return;
  }
  button.disabled = true;
  message.textContent = "Validating the action against backend policy...";
  try {
    const result = await api("/api/recover", {
      method: "POST",
      body: JSON.stringify({ incident_id: incidentId, action })
    });
    message.textContent = `${result.status}: ${result.message}`;
    await loadDashboard();
  } catch (error) {
    message.textContent = `Recovery not completed: ${error.message}`;
  } finally {
    button.disabled = false;
  }
}

$("refreshBtn").addEventListener("click", loadDashboard);
$("loadIncidentsBtn").addEventListener("click", loadDashboard);
$("recoverBtn").addEventListener("click", requestRecovery);
loadDashboard();
