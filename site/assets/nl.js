// Påmelding til Skadedyrbrevet (dobbel bekreftelse via e-post). Brukes av alle skjema med data-nl.
(() => {
  const api = document.documentElement.dataset.ai || "https://skadedyrguiden-ai.stian-andreassen-835.workers.dev";
  document.querySelectorAll("form[data-nl]").forEach((f) => f.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = f.querySelector("[data-nlmsg]"), btn = f.querySelector("button");
    btn.disabled = true; msg.textContent = "Sender …";
    try {
      const r = await fetch(api + "/subscribe", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: f.querySelector("input[type=email]").value, website: f.querySelector("[name=website]")?.value || "" }) });
      const d = await r.json().catch(() => ({}));
      msg.textContent = r.ok ? (d.message || "Sjekk innboksen din og bekreft adressen.") : (d.error || "Noe gikk galt. Prøv igjen.");
      if (r.ok) f.querySelector("input[type=email]").value = "";
    } catch { msg.textContent = "Fikk ikke kontakt. Prøv igjen om litt."; }
    btn.disabled = false;
  }));
})();
