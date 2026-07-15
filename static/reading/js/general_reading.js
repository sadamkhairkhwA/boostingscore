(function () {
  "use strict";

  const K_STREAK = "gr_streak";
  const K_COMPLETED = "gr_completed_today";
  const K_LAST_SUMMARY = "gr_last_summary";
  const K_HISTORY = "gr_history";
  const K_BOOKMARKS = "gr_bookmarks";
  const K_SPEED = "gr_speed_sessions";
  const K_DECK = "gr_vocab_deck";
  const K_CURRENT = "gr_current_article";

  const TOPICS = ["all", "environment", "health", "technology", "society", "science", "business", "education"];
  const LEVELS = ["all", "beginner", "intermediate", "advanced"];
  const TOPIC_ICON = { environment: "leaf", health: "heartbeat", technology: "laptop", society: "city", science: "flask", business: "chart", education: "graduation-cap" };
  const TOPIC_LABEL = { environment: "Environment", health: "Health", technology: "Technology", society: "Society", science: "Science", business: "Business", education: "Education" };

  function topicIcon(topic, size) {
    var slug = TOPIC_ICON[topic] || "book";
    return typeof BSIcons !== "undefined" ? BSIcons.tile(slug, null, size || "sm") : "";
  }
  function clockIcon() {
    return typeof BSIcons !== "undefined" ? BSIcons.inline("clock", "ok") : "";
  }
  function flameIcon() {
    return typeof BSIcons !== "undefined" ? BSIcons.inline("flame", "warn") : "";
  }
  function checkIcon() {
    return typeof BSIcons !== "undefined" ? BSIcons.check() : "";
  }

  const ARTICLES = [
    {
      id: "a1",
      topic: "environment",
      level: "intermediate",
      minutes: 5,
      words: 320,
      questions: 5,
      title: "How cities are redesigning streets for cleaner air",
      desc: "Urban planners are replacing car lanes with green corridors — the results are measurable.",
      paragraphs: [
        "Urban planners worldwide are reallocating street space from private cars to cycle lanes, shade trees, and wider pavements. Their argument is simple: streets are public assets and should support clean mobility, not congestion alone.",
        "In several pilot zones, emissions around schools dropped within months once through-traffic was reduced and bus reliability improved. Residents initially worried about access, but data later showed faster short trips by bike and on foot.",
        "Critics note that redesign can fail when alternatives are weak. Without predictable public transport and clear freight windows, traffic pressure shifts to nearby streets and public trust declines.",
        "For IELTS readers, this article is useful because it links cause, evidence, and limitation — exactly the structure many Reading and Writing items reward.",
      ],
      vocab: [
        { word: "reallocating", pron: "/ˌriːˈæləkeɪtɪŋ/", def: "distributing resources in a different way" },
        { word: "corridors", pron: "/ˈkɒrɪdɔːz/", def: "routes or channels used for movement" },
        { word: "congestion", pron: "/kənˈdʒestʃən/", def: "too much traffic causing delay" },
        { word: "emissions", pron: "/ɪˈmɪʃənz/", def: "polluting gases released into the air" },
        { word: "predictable", pron: "/prɪˈdɪktəbəl/", def: "happening in a consistent way" },
        { word: "limitation", pron: "/ˌlɪmɪˈteɪʃən/", def: "a restriction or weakness" },
      ],
      questionsData: [
        { q: "What was reallocated in pilot zones?", options: ["School budgets", "Street space", "Hospital beds", "River water"], answer: 1, exp: "Paragraph 1 states street space was reallocated." },
        { q: "Which outcome happened near schools?", options: ["More traffic fines", "Lower emissions", "Higher parking demand", "Fewer buses"], answer: 1, exp: "Paragraph 2 reports emissions dropped near schools." },
        { q: "What can reduce trust in redesign plans?", options: ["Fast buses", "Clear freight windows", "Weak alternatives", "More cycle lanes"], answer: 2, exp: "Paragraph 3 warns failure happens when alternatives are weak." },
        { q: "What writing structure does the text highlight?", options: ["Narrative only", "Cause-evidence-limitation", "Dialogue format", "Chronological biography"], answer: 1, exp: "Paragraph 4 explicitly names cause, evidence, and limitation." },
        { q: "The main topic is best described as:", options: ["Airport expansion", "Street redesign for cleaner mobility", "University admissions", "Hospital staffing"], answer: 1, exp: "All paragraphs center on urban street redesign and outcomes." },
      ],
    },
    {
      id: "a2",
      topic: "health",
      level: "beginner",
      minutes: 4,
      words: 240,
      questions: 5,
      title: "Why sleep deprivation affects memory",
      desc: "Short sleep cycles reduce memory consolidation.",
      paragraphs: [
        "Sleep helps your brain organise information.",
        "When sleep is cut, recall becomes less reliable.",
        "Students who sleep enough perform better in comprehension tests.",
        "Consistent sleep beats last-minute cramming.",
      ],
      vocab: [
        { word: "deprivation", pron: "/ˌdeprɪˈveɪʃən/", def: "not having enough of something essential" },
        { word: "consolidation", pron: "/kənˌsɒlɪˈdeɪʃən/", def: "strengthening memory over time" },
        { word: "recall", pron: "/rɪˈkɔːl/", def: "to remember information" },
        { word: "reliable", pron: "/rɪˈlaɪəbəl/", def: "consistently dependable" },
        { word: "comprehension", pron: "/ˌkɒmprɪˈhenʃən/", def: "understanding of text" },
        { word: "consistent", pron: "/kənˈsɪstənt/", def: "regular and steady" },
      ],
      questionsData: [
        { q: "Sleep mainly helps the brain to:", options: ["Grow muscles", "Organise information", "Boost appetite", "Reduce vocabulary"], answer: 1, exp: "Paragraph 1 says sleep helps organise information." },
        { q: "When sleep is reduced, recall becomes:", options: ["More reliable", "Less reliable", "Unchanged", "Instant"], answer: 1, exp: "Paragraph 2 says recall becomes less reliable." },
        { q: "Who performed better?", options: ["People with enough sleep", "People with no sleep", "Only teachers", "None"], answer: 0, exp: "Paragraph 3 says students with enough sleep did better." },
        { q: "What beats cramming?", options: ["Coffee", "Consistent sleep", "Longer classes", "No breaks"], answer: 1, exp: "Paragraph 4 gives consistent sleep as better than cramming." },
        { q: "Main message:", options: ["Skip sleep to study", "Sleep quality supports memory", "Memory is random", "Only diet matters"], answer: 1, exp: "All paragraphs connect sleep with memory outcomes." },
      ],
    },
  ];

  function makeArticle(id, topic, level, title, desc, minutes, words) {
    return {
      id,
      topic,
      level,
      minutes,
      words,
      questions: 5,
      title,
      desc,
      paragraphs: [
        `${title} is increasingly discussed in ${topicLabel(topic)} policy contexts.`,
        `The article compares evidence, constraints, and practical decisions for learners.`,
        `Examples show why precision and paraphrase awareness matter in IELTS reading.`,
        `A final section connects the topic to writing-ready collocations and claims.`,
      ],
      vocab: [
        { word: "evidence", pron: "/ˈevɪdəns/", def: "facts used to support a claim" },
        { word: "constraint", pron: "/kənˈstreɪnt/", def: "a limitation that restricts action" },
        { word: "precision", pron: "/prɪˈsɪʒən/", def: "exactness and accuracy" },
        { word: "paraphrase", pron: "/ˈpærəfreɪz/", def: "restating meaning in different words" },
        { word: "context", pron: "/ˈkɒntekst/", def: "the situation in which something appears" },
        { word: "collocation", pron: "/ˌkɒləˈkeɪʃən/", def: "a natural word combination" },
      ],
      questionsData: [
        { q: "What does the article mainly compare?", options: ["Evidence and constraints", "Airline prices", "Museum maps", "Medical scans"], answer: 0, exp: "Paragraphs focus on evidence and constraints." },
        { q: "Which skill is highlighted for IELTS?", options: ["Paraphrase awareness", "Typing speed only", "Handwriting style", "Memorising dates"], answer: 0, exp: "The text links paraphrase awareness to reading accuracy." },
        { q: "What appears in the final section?", options: ["Collocations for writing", "Recipe methods", "Sport scores", "Train tables"], answer: 0, exp: "Final paragraph mentions writing-ready collocations." },
        { q: "A constraint is best defined as:", options: ["A limitation", "A synonym list", "A scorecard", "A colour code"], answer: 0, exp: "Constraint means limitation." },
        { q: "Best summary:", options: ["Topic analysis for IELTS transfer", "A tourist brochure", "A weather bulletin", "A fictional dialogue"], answer: 0, exp: "Overall focus is IELTS-transferable topic analysis." },
      ],
    };
  }

  ARTICLES.push(
    makeArticle("a3", "technology", "advanced", "The hidden cost of artificial intelligence", "Data-center growth changes energy demand.", 7, 480),
    makeArticle("a4", "society", "intermediate", "How remote work changed city centres", "Commuting patterns and retail footfall shifted rapidly.", 5, 300),
    makeArticle("a5", "science", "intermediate", "Microplastics found in human bloodstream", "Researchers debate what concentrations mean for long-term health.", 5, 310),
    makeArticle("a6", "business", "advanced", "When companies delay climate targets", "Investors react to credibility gaps in reporting.", 6, 390),
    makeArticle("a7", "education", "beginner", "Why spaced repetition beats cramming", "Smaller sessions over time improve long-term recall.", 4, 220),
    makeArticle("a8", "environment", "advanced", "Coral reef restoration using electricity", "Biorock methods show promise with scaling constraints.", 8, 520)
  );

  const BOOT = window.GR_BOOTSTRAP || {};
  if (Array.isArray(BOOT.articles) && BOOT.articles.length) {
    ARTICLES.length = 0;
    BOOT.articles.forEach((a) => ARTICLES.push(a));
  }

  function featuredArticleId() {
    const f = ARTICLES.find((a) => a.isFeatured);
    return f ? f.id : (ARTICLES[0] ? ARTICLES[0].id : "a1");
  }

  let activeTopic = "all";
  let activeLevel = "all";
  let currentArticleId = getStore(K_CURRENT, featuredArticleId());
  if (!ARTICLES.some((a) => a.id === currentArticleId)) {
    currentArticleId = featuredArticleId();
  }
  let readingTimer = null;
  let readingStart = null;
  let readingElapsed = 0;
  let qState = null;
  let vocabState = null;
  let challengeTimer = null;
  let challengeStart = null;

  function getStore(k, d) { try { const r = sessionStorage.getItem(k); return r ? JSON.parse(r) : d; } catch { return d; } }
  function setStore(k, v) { sessionStorage.setItem(k, JSON.stringify(v)); }
  function safeArr(v) { return Array.isArray(v) ? v : []; }
  function todayKey() { return new Date().toISOString().slice(0, 10); }
  function topicLabel(t) { return TOPIC_LABEL[t] || t; }
  function levelLabel(l) { return l.charAt(0).toUpperCase() + l.slice(1); }
  function levelClass(l) { return `gr-level-${l}`; }
  function fmtTime(sec) { const m = Math.floor(sec / 60); const s = sec % 60; return `${m}:${String(s).padStart(2, "0")}`; }
  function currentArticle() { return ARTICLES.find((a) => a.id === currentArticleId) || ARTICLES[0]; }
  function wordCount(t) { return (t || "").trim().split(/\s+/).filter(Boolean).length; }
  function getCookie(name) { const p = (`; ${document.cookie}`).split(`; ${name}=`); return p.length === 2 ? p.pop().split(";").shift() : ""; }

  function setTab(tab) {
    document.querySelectorAll(".gr-tab").forEach((b) => {
      const on = b.dataset.tab === tab;
      b.classList.toggle("active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    document.querySelectorAll(".gr-panel").forEach((p) => p.classList.toggle("active", p.dataset.panel === tab));
    if (tab === "reading") startReadingTimer();
    else stopReadingTimer();
  }

  function streakSet() { return new Set(safeArr((getStore(K_STREAK, { dates: [] })).dates)); }
  function addStreakDay(day) { const s = streakSet(); s.add(day); setStore(K_STREAK, { dates: Array.from(s).sort() }); }
  function streakCount() { const s = streakSet(); let d = new Date(`${todayKey()}T00:00:00`); let n = 0; while (s.has(d.toISOString().slice(0, 10))) { n += 1; d.setDate(d.getDate() - 1); } return n; }

  function renderStreak() {
    document.getElementById("gr-streak-title").innerHTML = `${streakCount()}-day reading streak ${flameIcon()}`;
    const labels = ["M", "T", "W", "T", "F", "S", "S"];
    const today = new Date(`${todayKey()}T00:00:00`);
    const monday = new Date(today);
    monday.setDate(today.getDate() - (today.getDay() === 0 ? 6 : today.getDay() - 1));
    const s = streakSet();
    document.getElementById("gr-streak-dots").innerHTML = labels.map((l, i) => {
      const d = new Date(monday);
      d.setDate(monday.getDate() + i);
      const key = d.toISOString().slice(0, 10);
      const cls = d > today ? "future" : (key === todayKey() && !s.has(key)) ? "today" : (s.has(key) ? "done" : "none");
      return `<span class="gr-dot ${cls}">${l}</span>`;
    }).join("");
  }

  function renderFeatured() {
    const a = currentArticle();
    document.getElementById("gr-featured-kicker").textContent = `Today's article · ${a.minutes} min`;
    document.getElementById("gr-featured-title").textContent = a.title;
    document.getElementById("gr-featured-desc").textContent = a.desc;
    document.getElementById("gr-featured-tags").innerHTML =
      `<span class="gr-tag">${topicIcon(a.topic)} ${topicLabel(a.topic)}</span>` +
      `<span class="gr-pill ${levelClass(a.level)}">${levelLabel(a.level)}</span>` +
      `<span class="gr-tag">${a.words} words</span>` +
      `<span class="gr-tag">${a.questions} questions</span>`;
  }

  function completedToday() { return safeArr(getStore(K_COMPLETED, [])).filter((r) => r.date === todayKey()); }
  function addCompleted(row) { const arr = safeArr(getStore(K_COMPLETED, [])); arr.unshift(row); setStore(K_COMPLETED, arr.slice(0, 100)); }

  function renderCompleted() {
    const rows = completedToday();
    const el = document.getElementById("gr-completed-today");
    if (!rows.length) { el.innerHTML = '<p class="gr-muted">No completed articles yet today.</p>'; return; }
    el.innerHTML = rows.map((r) =>
      `<div class="gr-completed-row"><div class="left"><span class="gr-check">${checkIcon()}</span><div><p class="gr-done-title">${r.title}</p><p class="gr-muted small">${topicLabel(r.topic)} · ${r.score}/${r.total} · ${r.wpm} wpm</p></div></div><span class="gr-pill">Done ${checkIcon()}</span></div>`
    ).join("");
  }

  function renderSummary() {
    const s = getStore(K_LAST_SUMMARY, { date: "", text: "" });
    const input = document.getElementById("gr-summary-input");
    if (s.date === todayKey()) input.value = s.text || "";
    document.getElementById("gr-summary-count").textContent = `${wordCount(input.value)} words`;
  }

  function drawFeedback(f) {
    const score = Math.max(0, Math.min(5, Number(f.score || 0)));
    const label = (f.accuracy_label || "amber").toLowerCase();
    const acc = document.getElementById("gr-fb-accuracy");
    acc.className = `gr-pill ${label === "green" ? "gr-level-beginner" : label === "red" ? "gr-level-advanced" : "gr-level-intermediate"}`;
    acc.textContent = `Accuracy: ${label.toUpperCase()}`;
    document.getElementById("gr-fb-score").textContent = `${score}/5`;
    document.getElementById("gr-fb-stars").innerHTML = Array.from({ length: 5 }, (_, i) =>
      `<span class="gr-star" aria-hidden="true">${i < score ? (typeof BSIcons !== "undefined" ? BSIcons.inline("star", "warn") : "") : (typeof BSIcons !== "undefined" ? BSIcons.inline("star-outline", "warn") : "")}</span>`
    ).join("");
    document.getElementById("gr-fb-progress").style.width = `${score * 20}%`;
    document.getElementById("gr-fb-right").textContent = `What you got right: ${f.got_right || "Good coverage of key ideas."}`;
    const missed = document.getElementById("gr-fb-missed");
    missed.className = `gr-fb-box ${score >= 4 ? "gr-fb-green" : "gr-fb-amber"}`;
    missed.textContent = `What you missed: ${f.missed || "No major gaps."}`;
    document.getElementById("gr-fb-model").textContent = f.model_summary || "Model summary unavailable.";
    document.getElementById("gr-fb-tip").textContent = f.tip || "Actionable tip: add one precise detail next time.";
    document.getElementById("gr-summary-feedback").hidden = false;
  }

  async function analyseSummary() {
    const input = document.getElementById("gr-summary-input");
    const summary = input.value.trim();
    const status = document.getElementById("gr-summary-status");
    if (!summary) { status.className = "gr-status warn"; status.textContent = "Write a summary first."; return; }
    setStore(K_LAST_SUMMARY, { date: todayKey(), text: summary, articleId: currentArticle().id });
    status.className = "gr-status on";
    status.textContent = "Analysing your summary...";
    document.getElementById("gr-summary-feedback").hidden = true;
    try {
      const a = currentArticle();
      const r = await fetch("/reading/general/summary-feedback/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({
          article_slug: a.slug || a.id,
          article_title: a.title,
          article_text: a.paragraphs.join("\n\n"),
          summary,
        }),
      });
      const data = await r.json();
      if (!r.ok || !data.ok) throw new Error("analysis failed");
      drawFeedback(data.feedback);
      status.className = "gr-status on";
      status.innerHTML = `${checkIcon()} Summary saved and analysed.`;
    } catch (_e) {
      status.className = "gr-status warn";
      status.textContent = "Could not analyse right now — summary saved anyway.";
    }
  }

  function renderFilters() {
    document.getElementById("gr-topic-filters").innerHTML = TOPICS.map((t) =>
      `<button class="gr-filter ${activeTopic === t ? "active" : ""}" data-topic="${t}">${t === "all" ? "All" : `${topicIcon(t)} ${topicLabel(t)}`}</button>`
    ).join("");
    document.getElementById("gr-level-filters").innerHTML = LEVELS.map((l) =>
      `<button class="gr-filter ${activeLevel === l ? "active" : ""}" data-level="${l}">${l === "all" ? "All" : levelLabel(l)}</button>`
    ).join("");
  }

  function renderBrowse() {
    const rows = ARTICLES.filter((a) => (activeTopic === "all" || a.topic === activeTopic) && (activeLevel === "all" || a.level === activeLevel));
    document.getElementById("gr-article-grid").innerHTML = rows.map((a) =>
      `<article class="gr-article" data-article="${a.id}"><div class="gr-article__icon">${topicIcon(a.topic, "md")}</div><span class="gr-pill ${levelClass(a.level)}">${levelLabel(a.level)}</span><h4>${a.title}</h4><p>${a.minutes} min · ${a.words} words</p><p>${topicLabel(a.topic)}</p></article>`
    ).join("");
  }

  function startReadingTimer() {
    if (readingTimer) return;
    if (!readingStart) readingStart = Date.now() - (readingElapsed * 1000);
    readingTimer = setInterval(() => {
      readingElapsed = Math.floor((Date.now() - readingStart) / 1000);
      document.getElementById("gr-reading-timer").innerHTML = `${clockIcon()} ${fmtTime(readingElapsed)}`;
    }, 1000);
  }
  function stopReadingTimer() { if (readingTimer) { clearInterval(readingTimer); readingTimer = null; } }

  function inDeck(word) { return safeArr(getStore(K_DECK, [])).find((d) => d.word.toLowerCase() === word.toLowerCase()) || null; }
  function addDeck(entry) { const d = safeArr(getStore(K_DECK, [])); if (!d.some((x) => x.word.toLowerCase() === entry.word.toLowerCase())) d.push(entry); setStore(K_DECK, d); }

  function renderReading() {
    const a = currentArticle();
    setStore(K_CURRENT, a.id);
    document.getElementById("gr-reading-title").textContent = a.title;
    document.getElementById("gr-reading-tags").innerHTML =
      `<span class="gr-tag">${topicIcon(a.topic)} ${topicLabel(a.topic)}</span>` +
      `<span class="gr-pill ${levelClass(a.level)}">${levelLabel(a.level)}</span>` +
      `<span class="gr-tag">${a.words} words</span>` +
      `<span class="gr-tag">${a.questions} questions</span>`;
    document.getElementById("gr-reading-body").innerHTML = a.paragraphs.map((p) => `<p>${p}</p>`).join("");
    document.getElementById("gr-reading-vocab-line").innerHTML = a.vocab.map((v) => `<span class="gr-vocab-word ${inDeck(v.word) ? "in-deck" : ""}" data-word="${v.word}">${v.word}</span>`).join(" · ");
    document.getElementById("gr-bookmark-btn").innerHTML = safeArr(getStore(K_BOOKMARKS, [])).includes(a.id)
      ? 'Bookmarked <span class="bs-icon-inline bs-icon-inline--ok" aria-hidden="true">' + (typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "") + "</span>"
      : "Bookmark article";
    document.getElementById("gr-word-popup").hidden = true;
  }

  function showWord(word) {
    const a = currentArticle();
    const v = a.vocab.find((x) => x.word === word);
    if (!v) return;
    document.querySelectorAll(".gr-vocab-word").forEach((el) => el.classList.toggle("active", el.dataset.word === word));
    const d = inDeck(word);
    document.getElementById("gr-word-title").textContent = v.word;
    document.getElementById("gr-word-pron").textContent = v.pron;
    document.getElementById("gr-word-def").textContent = v.def;
    document.getElementById("gr-word-level").textContent = d ? `Level ${d.level} — in deck` : "Not in deck";
    const btn = document.getElementById("gr-word-add");
    btn.dataset.word = word;
    btn.innerHTML = d
      ? 'Added <span class="bs-icon-inline bs-icon-inline--ok" aria-hidden="true">' + (typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "") + "</span>"
      : "Add to deck";
    btn.disabled = !!d;
    document.getElementById("gr-word-popup").hidden = false;
  }

  function beginQuestions() {
    const a = currentArticle();
    qState = {
      idx: 0,
      total: a.questionsData.length,
      correct: 0,
      elapsed: readingElapsed,
      wpm: Math.max(80, Math.round(a.words / Math.max(1, readingElapsed / 60))),
    };
    document.getElementById("gr-q-results").hidden = true;
    renderQuestion();
    setTab("questions");
  }

  function renderQuestion() {
    const q = currentArticle().questionsData[qState.idx];
    document.getElementById("gr-q-counter").textContent = `Question ${qState.idx + 1} of ${qState.total}`;
    document.getElementById("gr-q-correct").textContent = `Correct: ${qState.correct}`;
    document.getElementById("gr-q-progress").style.width = `${(qState.idx / qState.total) * 100}%`;
    document.getElementById("gr-q-text").textContent = q.q;
    document.getElementById("gr-q-options").innerHTML = q.options.map((o, i) => `<button class="gr-option" data-i="${i}">${o}</button>`).join("");
    document.getElementById("gr-q-explain").hidden = true;
    document.getElementById("gr-q-next").hidden = true;
  }

  function answerQuestion(i) {
    const q = currentArticle().questionsData[qState.idx];
    document.querySelectorAll("#gr-q-options .gr-option").forEach((b, idx) => {
      if (idx === q.answer) b.classList.add("correct");
      if (idx === i && idx !== q.answer) b.classList.add("wrong");
      b.disabled = true;
    });
    if (i === q.answer) qState.correct += 1;
    document.getElementById("gr-q-correct").textContent = `Correct: ${qState.correct}`;
    const exp = document.getElementById("gr-q-explain");
    exp.textContent = q.exp;
    exp.hidden = false;
    const n = document.getElementById("gr-q-next");
    n.hidden = false;
    n.textContent = qState.idx === qState.total - 1 ? "See results →" : "Next question →";
  }

  function showResults() {
    const a = currentArticle();
    const score = qState.correct;
    const total = qState.total;
    const msg = score === 5 ? ["Perfect score!", "gr-level-beginner"] : score === 4 ? ["Great — one to review", "gr-level-intermediate"] : ["Re-read to strengthen understanding", "gr-level-advanced"];
    document.getElementById("gr-q-progress").style.width = "100%";
    document.getElementById("gr-q-text").textContent = "Results";
    document.getElementById("gr-q-options").innerHTML = "";
    document.getElementById("gr-q-explain").hidden = true;
    document.getElementById("gr-q-next").hidden = true;
    document.getElementById("gr-r-title").textContent = `${score}/${total}`;
    document.getElementById("gr-r-meta").textContent = `${qState.wpm} wpm · ${fmtTime(qState.elapsed)} time taken`;
    const m = document.getElementById("gr-r-message");
    m.textContent = msg[0];
    m.className = `gr-pill ${msg[1]}`;
    document.getElementById("gr-q-results").hidden = false;

    const row = { id: Date.now(), date: todayKey(), articleId: a.id, title: a.title, topic: a.topic, score, total, wpm: qState.wpm, time: qState.elapsed };
    const hist = safeArr(getStore(K_HISTORY, []));
    hist.unshift(row);
    setStore(K_HISTORY, hist.slice(0, 200));
    addCompleted({ date: todayKey(), title: a.title, topic: a.topic, score, total, wpm: qState.wpm });
    addStreakDay(todayKey());
    const sp = safeArr(getStore(K_SPEED, []));
    sp.unshift({ date: todayKey(), articleId: a.id, wpm: qState.wpm });
    setStore(K_SPEED, sp.slice(0, 200));
    fetch("/reading/general/log-session/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
      body: JSON.stringify({
        article_slug: a.slug || a.id,
        score,
        total_questions: total,
        wpm: qState.wpm,
        time_taken_secs: qState.elapsed,
      }),
    }).catch(() => {});

    renderTodayAll();
    renderSpeed();
    renderProgress();
    renderHistory();
    startVocabSession();
  }

  function startVocabSession() { vocabState = { idx: 0, flipped: false, easy: 0, hard: 0, words: currentArticle().vocab.slice() }; renderFlashcard(); }

  function renderFlashcard() {
    if (!vocabState) return;
    const total = vocabState.words.length;
    document.getElementById("gr-vocab-progress").textContent = `${Math.min(vocabState.idx + 1, total)} / ${total} done`;
    if (vocabState.idx >= total) {
      document.getElementById("gr-flashcard").textContent = `Session complete. Easy: ${vocabState.easy} · Hard: ${vocabState.hard}`;
      document.getElementById("gr-flash-actions").hidden = true;
      document.getElementById("gr-flash-score").textContent = "Great work — save these words to your deck.";
      return;
    }
    const w = vocabState.words[vocabState.idx];
    document.getElementById("gr-flashcard").textContent = vocabState.flipped ? `${w.word}\n\n${w.def}` : w.word;
    document.getElementById("gr-flash-actions").hidden = !vocabState.flipped;
    document.getElementById("gr-flash-score").textContent = "Tap card to flip.";
  }

  function renderSpeed() {
    const s = safeArr(getStore(K_SPEED, [])).slice(0, 7);
    const current = s[0] ? s[0].wpm : 0;
    const prev = s.length > 1 ? Math.round(s.slice(1).reduce((a, b) => a + b.wpm, 0) / (s.length - 1)) : 0;
    document.getElementById("gr-sp-current").textContent = current;
    document.getElementById("gr-sp-vs").textContent = `${current - prev >= 0 ? "+" : ""}${current - prev}`;
    document.getElementById("gr-sp-target").textContent = Math.max(0, 200 - current);
    document.getElementById("gr-sp-progress").style.width = `${Math.min(100, current / 2)}%`;
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"];
    document.getElementById("gr-speed-chart").innerHTML = Array.from({ length: 7 }, (_, i) => {
      const v = s[6 - i] ? s[6 - i].wpm : 0;
      return `<div class="gr-speed-col"><div class="gr-speed-bar ${i === 6 ? "today" : ""}" style="height:${Math.max(10, v / 2)}px"></div><div class="small">${days[i]}</div><div class="small">${v}</div></div>`;
    }).join("");
    const a = currentArticle();
    const best = safeArr(getStore(K_SPEED, [])).filter((x) => x.articleId === a.id).reduce((m, x) => Math.max(m, x.wpm), 0);
    document.getElementById("gr-challenge-best").textContent = best ? `Best for this article: ${best} wpm` : "No challenge yet for this article.";
  }

  function renderProgress() {
    const hist = safeArr(getStore(K_HISTORY, []));
    const avg = hist.length ? hist.reduce((a, b) => a + (b.score / b.total), 0) / hist.length : 0;
    const level = avg >= 0.8 ? "Advanced" : avg >= 0.55 ? "Intermediate" : "Beginner";
    const pct = Math.round(Math.min(100, avg * 100));
    document.getElementById("gr-level-title").textContent = `${level} level`;
    document.getElementById("gr-level-req").textContent = "Requirement: keep average 4/5+ and maintain streak activity.";
    document.getElementById("gr-level-progress").style.width = `${pct}%`;
    const passedMark = typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "";
    document.getElementById("gr-level-cards").innerHTML =
      `<div class="gr-level-card"><h4>Beginner</h4><p class="gr-muted small">Complete 3 sessions</p><p class="gr-pill">Passed ${passedMark}</p></div>` +
      `<div class="gr-level-card"><h4>Intermediate</h4><p class="gr-muted small">Average 3+/5 across 8 sessions</p><p class="gr-pill">${level === "Beginner" ? "Locked" : level === "Intermediate" ? "In progress" : "Passed " + passedMark}</p></div>` +
      `<div class="gr-level-card"><h4>Advanced</h4><p class="gr-muted small">Average 4+/5 across 20 sessions</p><p class="gr-pill">${level === "Advanced" ? "In progress" : "Locked"}</p></div>`;
    const by = {};
    hist.forEach((h) => { by[h.topic] = by[h.topic] || { c: 0, t: 0 }; by[h.topic].c += h.score; by[h.topic].t += h.total; });
    document.getElementById("gr-topic-bars").innerHTML = Object.keys(TOPIC_LABEL).map((t) => {
      const v = by[t];
      const p = v ? Math.round((v.c / v.t) * 100) : 0;
      const col = p >= 75 ? "#16a34a" : p >= 60 ? "#f59e0b" : "#dc2626";
      return `<div class="gr-topic-row"><div class="gr-topic-head"><span>${topicLabel(t)}</span><span>${p}%</span></div><div class="bar"><div class="fill" style="width:${p}%;background:${col}"></div></div></div>`;
    }).join("");
    const comp = safeArr(getStore(K_COMPLETED, []));
    const map = {};
    comp.forEach((c) => { map[c.date] = (map[c.date] || 0) + 1; });
    const now = new Date();
    const end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    const cells = [];
    for (let d = 1; d <= end.getDate(); d += 1) {
      const key = new Date(now.getFullYear(), now.getMonth(), d).toISOString().slice(0, 10);
      let cls = "";
      if (map[key] >= 1) cls = "partial";
      if (map[key] >= 2) cls = "full";
      if (key === todayKey()) cls += " today";
      cells.push(`<span class="gr-cell ${cls.trim()}"></span>`);
    }
    document.getElementById("gr-calendar").innerHTML = cells.join("");
    const streak = streakCount();
    const deck = safeArr(getStore(K_DECK, []));
    document.getElementById("gr-progress-stats").innerHTML =
      `<div class="gr-stat"><p class="num">${hist.filter((h) => h.date.startsWith(todayKey().slice(0, 7))).length}</p><p class="gr-muted small">Sessions this month</p></div>` +
      `<div class="gr-stat"><p class="num">${streak}</p><p class="gr-muted small">Current streak</p></div>` +
      `<div class="gr-stat"><p class="num">${deck.length}</p><p class="gr-muted small">Words reviewed</p></div>` +
      `<div class="gr-stat"><p class="num">${streak}</p><p class="gr-muted small">Best streak</p></div>`;
  }

  function renderHistory() {
    const hist = safeArr(getStore(K_HISTORY, []));
    document.getElementById("gr-history-list").innerHTML = hist.length
      ? hist.slice(0, 30).map((h) =>
          `<div class="gr-history-row"><div><p class="gr-done-title">${topicIcon(h.topic, "sm")} ${h.title}</p><p class="gr-muted small">${topicLabel(h.topic)} · ${h.date} · ${h.wpm} wpm</p></div><span class="gr-pill ${h.score / h.total >= 0.8 ? "gr-level-beginner" : h.score / h.total >= 0.6 ? "gr-level-intermediate" : "gr-level-advanced"}">${h.score}/${h.total}</span></div>`
        ).join("")
      : '<p class="gr-muted">No history yet.</p>';
    const ids = safeArr(getStore(K_BOOKMARKS, []));
    document.getElementById("gr-bookmarks-list").innerHTML = ids.length
      ? ids.map((id) => {
          const a = ARTICLES.find((x) => x.id === id);
          if (!a) return "";
          return `<div class="gr-bookmark-row"><div><p class="gr-done-title">${a.title}</p><p class="gr-muted small">${topicLabel(a.topic)} · ${levelLabel(a.level)}</p></div><div class="gr-row-gap"><span class="gr-pill ${levelClass(a.level)}">${levelLabel(a.level)}</span><button class="gr-btn-light" data-remove-bookmark="${a.id}">Remove</button></div></div>`;
        }).join("")
      : '<p class="gr-muted">No bookmarks yet.</p>';
  }

  function renderTodayAll() { renderStreak(); renderFeatured(); renderCompleted(); renderSummary(); }

  function bind() {
    document.querySelectorAll(".gr-tab").forEach((b) => b.addEventListener("click", () => setTab(b.dataset.tab)));
    document.getElementById("gr-start-reading").addEventListener("click", () => { readingElapsed = 0; readingStart = null; renderReading(); setTab("reading"); });
    document.getElementById("gr-topic-filters").addEventListener("click", (e) => { const b = e.target.closest("[data-topic]"); if (!b) return; activeTopic = b.dataset.topic; renderFilters(); renderBrowse(); });
    document.getElementById("gr-level-filters").addEventListener("click", (e) => { const b = e.target.closest("[data-level]"); if (!b) return; activeLevel = b.dataset.level; renderFilters(); renderBrowse(); });
    document.getElementById("gr-article-grid").addEventListener("click", (e) => { const c = e.target.closest("[data-article]"); if (!c) return; currentArticleId = c.dataset.article; setStore(K_CURRENT, currentArticleId); readingElapsed = 0; readingStart = null; renderReading(); setTab("reading"); });
    document.getElementById("gr-reading-back").addEventListener("click", () => setTab("browse"));
    document.getElementById("gr-reading-vocab-line").addEventListener("click", (e) => { const w = e.target.closest("[data-word]"); if (!w) return; showWord(w.dataset.word); });
    document.getElementById("gr-word-add").addEventListener("click", () => { const w = document.getElementById("gr-word-add").dataset.word; const v = currentArticle().vocab.find((x) => x.word === w); if (!v) return; addDeck({ word: v.word, topic: currentArticle().topic, level: 1, def: v.def }); showWord(w); renderReading(); });
    document.getElementById("gr-bookmark-btn").addEventListener("click", () => {
      fetch("/reading/general/toggle-bookmark/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({ article_slug: currentArticle().slug || currentArticle().id }),
      })
        .then((r) => r.json())
        .then((data) => {
          const ids = safeArr(getStore(K_BOOKMARKS, []));
          if (data.bookmarked && !ids.includes(currentArticleId)) ids.push(currentArticleId);
          if (!data.bookmarked) {
            const next = ids.filter((x) => x !== currentArticleId);
            setStore(K_BOOKMARKS, next);
          } else {
            setStore(K_BOOKMARKS, ids);
          }
          renderReading();
          renderHistory();
        })
        .catch(() => {});
    });
    document.getElementById("gr-reading-done").addEventListener("click", () => { stopReadingTimer(); beginQuestions(); });
    document.getElementById("gr-q-options").addEventListener("click", (e) => { const b = e.target.closest("[data-i]"); if (!b || !document.getElementById("gr-q-next").hidden) return; answerQuestion(Number(b.dataset.i)); });
    document.getElementById("gr-q-next").addEventListener("click", () => { if (qState.idx === qState.total - 1) showResults(); else { qState.idx += 1; renderQuestion(); } });
    document.getElementById("gr-r-vocab").addEventListener("click", () => setTab("vocab"));
    document.getElementById("gr-r-next").addEventListener("click", () => setTab("browse"));
    document.getElementById("gr-flashcard").addEventListener("click", () => { if (!vocabState) return; vocabState.flipped = !vocabState.flipped; renderFlashcard(); });
    document.getElementById("gr-flash-hard").addEventListener("click", () => { vocabState.hard += 1; vocabState.idx += 1; vocabState.flipped = false; renderFlashcard(); });
    document.getElementById("gr-flash-easy").addEventListener("click", () => { vocabState.easy += 1; vocabState.idx += 1; vocabState.flipped = false; renderFlashcard(); });
    document.getElementById("gr-save-vocab").addEventListener("click", () => { const a = currentArticle(); a.vocab.forEach((v) => addDeck({ word: v.word, topic: a.topic, level: 1, def: v.def })); const s = document.getElementById("gr-save-vocab-msg"); s.className = "gr-status on"; s.innerHTML = (typeof BSIcons !== "undefined" ? BSIcons.inline("check", "ok") : "") + ` Added to ${topicLabel(a.topic)} deck — appears in Smart review tomorrow.`; renderReading(); renderProgress(); });
    document.getElementById("gr-summary-input").addEventListener("input", (e) => { document.getElementById("gr-summary-count").textContent = `${wordCount(e.target.value)} words`; });
    document.getElementById("gr-summary-analyse").addEventListener("click", analyseSummary);
    document.getElementById("gr-challenge-start").addEventListener("click", () => {
      challengeStart = Date.now();
      document.getElementById("gr-challenge-done").disabled = false;
      document.getElementById("gr-challenge-result").className = "gr-status";
      if (challengeTimer) clearInterval(challengeTimer);
      challengeTimer = setInterval(() => { document.getElementById("gr-challenge-timer").textContent = fmtTime(Math.floor((Date.now() - challengeStart) / 1000)); }, 1000);
    });
    document.getElementById("gr-challenge-done").addEventListener("click", () => {
      if (!challengeStart) return;
      clearInterval(challengeTimer);
      challengeTimer = null;
      const sec = Math.max(1, Math.floor((Date.now() - challengeStart) / 1000));
      const wpm = Math.round(currentArticle().words / (sec / 60));
      const sessions = safeArr(getStore(K_SPEED, []));
      const best = sessions.filter((s) => s.articleId === currentArticleId).reduce((m, s) => Math.max(m, s.wpm), 0);
      sessions.unshift({ date: todayKey(), articleId: currentArticleId, wpm });
      setStore(K_SPEED, sessions.slice(0, 200));
      const msg = document.getElementById("gr-challenge-result");
      msg.className = "gr-status on";
      msg.textContent = wpm > best ? `New best! ${wpm} wpm` : wpm === best ? `Matched your best (${wpm} wpm)` : `Try again — ${wpm} wpm (best ${best})`;
      document.getElementById("gr-challenge-done").disabled = true;
      renderSpeed();
    });
    document.getElementById("gr-bookmarks-list").addEventListener("click", (e) => {
      const b = e.target.closest("[data-remove-bookmark]");
      if (!b) return;
      const id = b.dataset.removeBookmark;
      fetch("/reading/general/toggle-bookmark/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({ article_slug: id }),
      }).catch(() => {});
      setStore(K_BOOKMARKS, safeArr(getStore(K_BOOKMARKS, [])).filter((x) => x !== id));
      renderHistory();
    });
  }

  function bootstrap() {
    if (!sessionStorage.getItem(K_STREAK)) setStore(K_STREAK, { dates: [] });
    if (!sessionStorage.getItem(K_COMPLETED)) setStore(K_COMPLETED, BOOT.completedToday || []);
    if (!sessionStorage.getItem(K_LAST_SUMMARY)) setStore(K_LAST_SUMMARY, BOOT.lastSummary || { date: "", text: "", articleId: "" });
    if (!sessionStorage.getItem(K_HISTORY)) setStore(K_HISTORY, BOOT.history || []);
    if (!sessionStorage.getItem(K_BOOKMARKS)) setStore(K_BOOKMARKS, BOOT.bookmarks || []);
    if (!sessionStorage.getItem(K_SPEED)) setStore(K_SPEED, BOOT.speedSessions || [{ date: todayKey(), articleId: featuredArticleId(), wpm: 170 }]);
    if (!sessionStorage.getItem(K_DECK)) setStore(K_DECK, []);
    if (!sessionStorage.getItem(K_CURRENT)) setStore(K_CURRENT, featuredArticleId());
  }

  function init() {
    bootstrap();
    var timerIc = document.querySelector(".gr-timer__ic");
    if (timerIc && typeof BSIcons !== "undefined") timerIc.innerHTML = BSIcons.inline("clock", "ok");
    renderTodayAll();
    renderFilters();
    renderBrowse();
    renderReading();
    startVocabSession();
    renderSpeed();
    renderProgress();
    renderHistory();
    bind();
    setTab("today");
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
