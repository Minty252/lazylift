// lazylift.cc: mail links and the waitlist form. No cookies, no tracking.
(function () {
  var en = document.documentElement.lang === "en";

  // The address is written backwards and base64-encoded in the HTML, so address
  // collectors that search the page text find nothing.
  var MAIL = "bW9jLnp0aXJvbW5uYW1mb2hAZW0=";
  var address = atob(MAIL).split("").reverse().join("");
  document.querySelectorAll("[data-mail]").forEach(function (a) {
    a.href = "mailto:" + address;
    a.textContent = address;
  });

  // Waitlist: the mail endpoint on fastpal.com (Hofmann GmbH), which allows this origin.
  var TEXT = en
    ? { sending: "Sending …", send: "Join the waitlist", thanks: "Thank you!", done: "You are on the waitlist. I will e-mail you once you can test it.", fail: "Sending does not work right now.", write: "Write to me directly at" }
    : { sending: "Wird gesendet …", send: "Auf die Warteliste", thanks: "Danke!", done: "Du stehst auf der Warteliste. Ich melde mich per Mail, sobald du testen kannst.", fail: "Senden geht gerade nicht.", write: "Schreib mir gern direkt an" };
  document.querySelectorAll("form[data-anfrage]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var button = form.querySelector("button[type=submit]");
      var old = form.querySelector(".cc-form-fehler");
      if (old) old.remove();
      button.disabled = true;
      button.textContent = TEXT.sending;
      var data = Object.fromEntries(new FormData(form));
      data.art = form.getAttribute("data-anfrage");
      data.sprache = en ? "en" : "de";
      // text/plain keeps it a simple request (no preflight); the route reads JSON anyway.
      fetch("https://fastpal.com/api/anfrage", { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(data) })
        .then(function (res) { return res.json().then(function (body) { return { ok: res.ok && body.ok, body: body }; }); })
        .catch(function () { return { ok: false, body: null }; })
        .then(function (r) {
          if (r.ok) {
            var done = document.createElement("div");
            done.className = "cc-form-danke";
            done.setAttribute("role", "status");
            done.innerHTML = '<p class="cc-betrag"></p><p></p>';
            done.children[0].textContent = TEXT.thanks;
            done.children[1].textContent = TEXT.done;
            form.replaceWith(done);
            return;
          }
          button.disabled = false;
          button.textContent = TEXT.send;
          var p = document.createElement("p");
          p.className = "cc-form-fehler";
          p.setAttribute("role", "alert");
          p.textContent = ((r.body && r.body.fehler) || TEXT.fail) + " " + TEXT.write + " ";
          var a = document.createElement("a");
          a.href = "mailto:" + address;
          a.textContent = address;
          p.append(a, ".");
          button.after(p);
        });
    });
  });
})();
