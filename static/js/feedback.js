(function () {
  var root = document.getElementById("bs-feedback");
  if (!root) return;

  var openBtn = document.getElementById("bs-fb-open");
  var closeBtn = document.getElementById("bs-fb-close");
  var cancelBtn = document.getElementById("bs-fb-cancel");
  var backdrop = document.getElementById("bs-fb-backdrop");
  var panel = document.getElementById("bs-fb-panel");
  var form = document.getElementById("bs-fb-form");
  var thanks = document.getElementById("bs-fb-thanks");
  var messageEl = document.getElementById("bs-fb-message");
  var errorEl = document.getElementById("bs-fb-error");
  var sendBtn = document.getElementById("bs-fb-send");
  var pills = root.querySelectorAll(".bs-fb__pill");
  var submitUrl = root.getAttribute("data-submit-url") || "/feedback/";
  var selectedType = "suggestion";
  var closeTimer = null;
  var sending = false;

  function csrfToken() {
    var input = form && form.querySelector("[name=csrfmiddlewaretoken]");
    if (input && input.value) return input.value;
    var match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function setType(type) {
    selectedType = type;
    pills.forEach(function (pill) {
      var on = pill.getAttribute("data-type") === type;
      pill.classList.toggle("is-active", on);
      pill.setAttribute("aria-checked", on ? "true" : "false");
    });
  }

  function showError(text) {
    if (!errorEl) return;
    if (text) {
      errorEl.textContent = text;
      errorEl.hidden = false;
    } else {
      errorEl.textContent = "";
      errorEl.hidden = true;
    }
  }

  function openPanel() {
    if (closeTimer) {
      clearTimeout(closeTimer);
      closeTimer = null;
    }
    panel.hidden = false;
    if (backdrop) backdrop.hidden = false;
    openBtn.setAttribute("aria-expanded", "true");
    form.hidden = false;
    thanks.hidden = true;
    showError("");
    setTimeout(function () {
      if (messageEl) messageEl.focus();
    }, 30);
  }

  function closePanel() {
    panel.hidden = true;
    if (backdrop) backdrop.hidden = true;
    openBtn.setAttribute("aria-expanded", "false");
    form.hidden = false;
    thanks.hidden = true;
    showError("");
    sending = false;
    if (sendBtn) {
      sendBtn.disabled = false;
      sendBtn.textContent = "Send feedback";
    }
  }

  function showThanksThenClose() {
    form.hidden = true;
    thanks.hidden = false;
    closeTimer = setTimeout(closePanel, 2000);
  }

  function resetSendButton() {
    sending = false;
    if (sendBtn) {
      sendBtn.disabled = false;
      sendBtn.textContent = "Send feedback";
    }
  }

  pills.forEach(function (pill) {
    pill.addEventListener("click", function () {
      setType(pill.getAttribute("data-type") || "suggestion");
    });
  });

  openBtn.addEventListener("click", function () {
    if (panel.hidden) openPanel();
    else closePanel();
  });
  if (closeBtn) closeBtn.addEventListener("click", closePanel);
  if (cancelBtn) cancelBtn.addEventListener("click", closePanel);
  if (backdrop) backdrop.addEventListener("click", closePanel);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && panel && !panel.hidden) closePanel();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (sending) return;
    var message = (messageEl.value || "").trim();
    if (!message) {
      showError("Please write a short message.");
      messageEl.focus();
      return;
    }
    showError("");
    sending = true;
    sendBtn.disabled = true;
    sendBtn.textContent = "Sending…";

    var token = csrfToken();
    var body = new FormData();
    body.append("csrfmiddlewaretoken", token);
    body.append("type", selectedType);
    body.append("message", message);
    body.append("page_url", window.location.href);
    body.append("user_agent", navigator.userAgent || "");

    fetch(submitUrl, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": token,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: body,
    })
      .then(function (res) {
        var ct = (res.headers.get("content-type") || "").toLowerCase();
        if (ct.indexOf("application/json") !== -1) {
          return res.json().then(function (data) {
            return { ok: res.ok, status: res.status, data: data || {} };
          });
        }
        return res.text().then(function () {
          var err =
            res.status === 403
              ? "Session expired — refresh the page and try again."
              : "Couldn't send just now. Please try again.";
          return { ok: false, status: res.status, data: { error: err } };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          showError(
            (result.data && result.data.error) ||
              "Couldn't send just now. Please try again."
          );
          resetSendButton();
          return;
        }
        messageEl.value = "";
        setType("suggestion");
        showThanksThenClose();
      })
      .catch(function () {
        showError("Couldn't send just now. Please try again.");
        resetSendButton();
      });
  });
})();
