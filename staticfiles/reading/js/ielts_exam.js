(function () {
  const dataNode = document.getElementById("ielts-exam-json");
  if (!dataNode) return;

  const EXAM_DATA = JSON.parse(dataNode.textContent || "{}");
  const TOTAL_QUESTIONS = 40;
  const left = document.getElementById("ielts-left-panel");
  const right = document.getElementById("ielts-questions");
  const nav = document.getElementById("ielts-nav");
  const warning = document.getElementById("ielts-warning");

  let actualTotal = 0;
  (EXAM_DATA.parts || []).forEach((part) => {
    (part.questionGroups || []).forEach((group) => {
      actualTotal += (group.questions || []).length;
    });
  });

  if (actualTotal < TOTAL_QUESTIONS && warning) {
    warning.hidden = false;
    warning.textContent =
      `This test was generated with ${actualTotal} of 40 questions. ` +
      "Please ask your administrator to regenerate this test.";
  }

  function renderLeft() {
    left.innerHTML = (EXAM_DATA.parts || [])
      .map((part) => {
        const paragraphs = (part.paragraphs || [])
          .map((p) => `<p><strong>${p.label}.</strong> ${p.text}</p>`)
          .join("");
        return `<article class="ielts-part"><h2>Passage ${part.partNumber}: ${part.title}</h2>${paragraphs}</article>`;
      })
      .join("");
  }

  function renderQuestions() {
    const chunks = [];
    (EXAM_DATA.parts || []).forEach((part) => {
      chunks.push(`<section class="ielts-q-part"><h3>Questions for Passage ${part.partNumber}</h3>`);
      (part.questionGroups || []).forEach((group) => {
        (group.questions || []).forEach((q) => {
          let body = "";
          if (group.type === "mc") {
            body = Object.entries(q.options || {})
              .map(([k, v]) => `<label><input type="radio" name="q-${q.number}" value="${k}"> ${k}. ${v}</label>`)
              .join("");
          } else if (group.type === "tfng") {
            body = ["True", "False", "Not Given"]
              .map((v) => `<label><input type="radio" name="q-${q.number}" value="${v}"> ${v}</label>`)
              .join("");
          } else if (group.type === "ynng") {
            body = ["Yes", "No", "Not Given"]
              .map((v) => `<label><input type="radio" name="q-${q.number}" value="${v}"> ${v}</label>`)
              .join("");
          } else {
            body = `<input type="text" name="q-${q.number}" placeholder="Type answer">`;
          }
          chunks.push(
            `<div class="ielts-q" id="q-${q.number}"><div class="ielts-qn">${q.number}.</div><div><p>${q.stem}</p>${body}</div></div>`
          );
        });
      });
      chunks.push("</section>");
    });
    right.innerHTML = chunks.join("");
  }

  function renderNav() {
    const allQuestions = [];
    (EXAM_DATA.parts || []).forEach((part, pi) => {
      (part.questionGroups || []).forEach((group) => {
        (group.questions || []).forEach((q) => {
          allQuestions.push({ num: q.number, partIndex: pi });
        });
      });
    });
    allQuestions.sort((a, b) => a.num - b.num);
    nav.innerHTML = allQuestions
      .map((q) => `<button type="button" data-q="${q.num}">${q.num}</button>`)
      .join("");

    nav.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        const el = document.getElementById(`q-${btn.dataset.q}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });
  }

  renderLeft();
  renderQuestions();
  renderNav();
})();
