/* BoostingScore SVG icons — mirrors vocabulary/icon_registry.py for dynamic UI */
(function (global) {
  "use strict";

  var ICONS = {
    leaf: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 18 2c1 2 2 4.5 2 8a9 9 0 1 1-9 10z"/>' },
    heartbeat: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M19 14c1.5-1.3 3-3.2 3-5.5A5.5 5.5 0 0 0 12 5.5 5.5 5.5 0 0 0 5 8.5C5 10.8 6.5 12.7 8 14l4 4 4-4z"/>' },
    laptop: { v: "blue", s: '<rect x="3" y="5" width="18" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M2 19h20"/>' },
    "graduation-cap": { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M22 9 12 5 2 9l10 4 10-4z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/>' },
    building: { v: "navy", s: '<rect x="4" y="3" width="16" height="18" rx="1" fill="none" stroke="currentColor" stroke-width="2"/>' },
    city: { v: "navy", s: '<rect x="3" y="10" width="6" height="11" fill="none" stroke="currentColor" stroke-width="2"/><rect x="11" y="6" width="5" height="15" fill="none" stroke="currentColor" stroke-width="2"/><rect x="18" y="3" width="3" height="18" fill="none" stroke="currentColor" stroke-width="2"/>' },
    plane: { v: "blue", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M2 12h5l3-9 4 18 3-9h5"/>' },
    flask: { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M10 3v6.5L5.5 19a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2L14 9.5V3"/>' },
    briefcase: { v: "orange", s: '<rect x="3" y="7" width="18" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>' },
    book: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>' },
    star: { v: "amber", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 2l2.6 6.3L21 9l-5 4.4L17.5 20 12 16.8 6.5 20 8 13.4 3 9l6.4-.7z"/>' },
    cards: { v: "green", s: '<rect x="3" y="5" width="12" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="8" y="3" width="12" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>' },
    target: { v: "green", s: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="1" fill="currentColor"/>' },
    lightbulb: { v: "amber", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M9 18h6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 2a7 7 0 0 0-4 12.7V18h8v-3.3A7 7 0 0 0 12 2z"/>' },
    pen: { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 20h4l10-10-4-4L4 16v4zM14 6l4 4"/>' },
    key: { v: "navy", s: '<circle cx="8" cy="15" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 15h9"/>' },
    brain: { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M9 4a3 3 0 0 0-3 3v1a2 2 0 0 0 0 4v1a3 3 0 0 0 3 3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M15 4a3 3 0 0 1 3 3v1a2 2 0 0 1 0 4v1a3 3 0 0 1-3 3"/><line x1="12" y1="4" x2="12" y2="20" stroke="currentColor" stroke-width="2"/>' },
    flame: { v: "amber", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 2c1 3 4 4 4 8a4 4 0 1 1-8 0c0-2 1-3 2-4-1 3 1 4 2 4 1 0 2-1 2-2.5C14 5 13 4 12 2z"/>' },
    "level-easy": { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>' },
    "level-medium": { v: "blue", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2"/>' },
    "level-hard": { v: "orange", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2"/><line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" stroke-width="2"/>' },
    check: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" d="M5 12l4 4L19 7"/>' },
    x: { v: "red", s: '<path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/>' },
    warning: { v: "amber", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 3L2 20h20L12 3z"/><line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="2"/>' },
    settings: { v: "navy", s: '<circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2"/>' },
    chart: { v: "blue", s: '<line x1="6" y1="20" x2="6" y2="14" stroke="currentColor" stroke-width="2"/><line x1="12" y1="20" x2="12" y2="4" stroke="currentColor" stroke-width="2"/><line x1="18" y1="20" x2="18" y2="10" stroke="currentColor" stroke-width="2"/>' },
    compass: { v: "orange", s: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><polygon fill="none" stroke="currentColor" stroke-width="2" points="16 8 14 14 8 16 10 10"/>' },
    newspaper: { v: "orange", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19h16a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14"/>' },
    headphones: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 14v-2a8 8 0 0 1 16 0v2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M4 14a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-2a2 2 0 0 1 2-2zM20 14a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2 2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2z"/>' },
    "thumbs-up": { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M7 11v8a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-6h5a2 2 0 0 0 2-2l1-6a2 2 0 0 0-2-2h-6l1-4a2 2 0 0 0-2-2 2 2 0 0 0-2 2v4"/>' },
    pin: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 21s6-5.2 6-10a6 6 0 1 0-12 0c0 4.8 6 10 6 10z"/><circle cx="12" cy="11" r="2" fill="none" stroke="currentColor" stroke-width="2"/>' },
    puzzle: { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M10 4h4v2a2 2 0 0 0 2 2h2v4h-2a2 2 0 0 0-2 2v2H10v-2a2 2 0 0 0-2-2H6v-4h2a2 2 0 0 0 2-2V4z"/>' },
    users: { v: "navy", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4" fill="none" stroke="currentColor" stroke-width="2"/>' },
    folder: { v: "green", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.5L10 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2z"/>' },
    clock: { v: "green", s: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 7v5l3 3"/>' },
    quiz: { v: "purple", s: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M9.5 9.5a2.5 2.5 0 1 1 4.2 1.8c-.6.6-1.2 1-1.2 2.2V14"/><line x1="12" y1="17" x2="12" y2="17.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' },
    clipboard: { v: "navy", s: '<rect x="5" y="4" width="14" height="17" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M9 4h6a2 2 0 0 1 2 2v1H7V6a2 2 0 0 1 2-2z"/>' },
    keyboard: { v: "navy", s: '<rect x="2" y="6" width="20" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="6" cy="10" r=".5" fill="currentColor"/><circle cx="10" cy="10" r=".5" fill="currentColor"/><circle cx="14" cy="10" r=".5" fill="currentColor"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6 14h8"/>' },
    scale: { v: "navy", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 3v18"/><path fill="none" stroke="currentColor" stroke-width="2" d="M5 7h14"/><path fill="none" stroke="currentColor" stroke-width="2" d="M5 7l-3 6h6L5 7zM19 7l-3 6h6l-3-6z"/>' },
    link: { v: "blue", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path fill="none" stroke="currentColor" stroke-width="2" d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>' },
    letters: { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 7V4h16v3"/><line x1="9" y1="20" x2="15" y2="20" stroke="currentColor" stroke-width="2"/><line x1="12" y1="4" x2="12" y2="20" stroke="currentColor" stroke-width="2"/>' },
    volume: { v: "blue", s: '<polygon fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path fill="none" stroke="currentColor" stroke-width="2" d="M15 9a4 4 0 0 1 0 6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M17 7a7 7 0 0 1 0 10"/>' },
    shuffle: { v: "navy", s: '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M16 3h5v5"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 20L21 3"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M21 16v5h-5"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M15 15l6 6"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 4l5 5"/>' },
    fullscreen: { v: "navy", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M8 3H5a2 2 0 0 0-2 2v3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M21 8V5a2 2 0 0 0-2-2h-3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M3 16v3a2 2 0 0 0 2 2h3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M16 21h3a2 2 0 0 0 2-2v-3"/>' },
    trophy: { v: "amber", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M8 21h8"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 17v4"/><path fill="none" stroke="currentColor" stroke-width="2" d="M7 4h10v5a5 5 0 0 1-10 0V4z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M7 6H4a2 2 0 0 0 2 3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M17 6h3a2 2 0 0 1-2 3"/>' },
    inbox: { v: "navy", s: '<polyline fill="none" stroke="currentColor" stroke-width="2" points="22 12 16 12 14 15 10 15 8 12 2 12"/><path fill="none" stroke="currentColor" stroke-width="2" d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>' },
    "star-outline": { v: "amber", s: '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 2l2.6 6.3L21 9l-5 4.4L17.5 20 12 16.8 6.5 20 8 13.4 3 9l6.4-.7z"/>' },
    refresh: { v: "navy", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M3 2v6h6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M21 12A9 9 0 0 0 6 5.3L3 8"/><path fill="none" stroke="currentColor" stroke-width="2" d="M21 22v-6h-6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M3 12a9 9 0 0 0 15 6.7l3-2.7"/>' },
    "trend-up": { v: "green", s: '<polyline fill="none" stroke="currentColor" stroke-width="2" points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline fill="none" stroke="currentColor" stroke-width="2" points="17 6 23 6 23 12"/>' },
    "trend-down": { v: "red", s: '<polyline fill="none" stroke="currentColor" stroke-width="2" points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline fill="none" stroke="currentColor" stroke-width="2" points="17 18 23 18 23 12"/>' },
    structure: { v: "green", s: '<rect x="3" y="3" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="14" y="3" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="14" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="14" y="14" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/>' },
    eye: { v: "blue", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/>' },
    write: { v: "purple", s: '<path fill="none" stroke="currentColor" stroke-width="2" d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M14 3v6h6M8 13h8M8 17h5"/>' }
  };

  var TOPIC = {
    environment: "leaf", health: "heartbeat", technology: "laptop",
    education: "graduation-cap", society: "building", travel: "plane",
    science: "flask", business: "briefcase", other: "star"
  };

  var EMOJI = {
    "\uD83C\uDF3F": "leaf", "\uD83E\uDE7A": "heartbeat", "\uD83C\uDFE5": "heartbeat",
    "\uD83D\uDCBB": "laptop", "\uD83C\uDF93": "graduation-cap", "\uD83D\uDCDA": "book",
    "\uD83C\uDFD9\uFE0F": "city", "\uD83C\uDFDB\uFE0F": "building", "\u2708\uFE0F": "plane",
    "\uD83D\uDD2C": "flask", "\uD83D\uDCBC": "briefcase", "\uD83D\uDCC7": "cards",
    "\u2B50": "star", "\uD83D\uDCD6": "book", "\uD83C\uDFAF": "target",
    "\uD83D\uDCA1": "lightbulb", "\u270F\uFE0F": "pen", "\uD83D\uDD11": "key",
    "\uD83E\uDDE0": "brain", "\uD83D\uDD25": "flame",
    "\uD83D\uDCD7": "level-easy", "\uD83D\uDCD8": "level-medium", "\uD83D\uDCD9": "level-hard",
    "\uD83D\uDC65": "users", "\uD83E\uDDE9": "puzzle", "\uD83D\uDCCA": "chart",
    "\u2705": "check", "\uD83C\uDF1F": "star", "\uD83D\uDC4D": "thumbs-up",
    "\u26A0": "warning", "\u2699": "settings", "\uD83D\uDCCD": "pin",
    "\u2606": "star-outline", "\u2605": "star", "\u2713": "check",
    "\uD83D\uDD00": "shuffle", "\uD83D\uDCE5": "inbox", "\uD83C\uDFC6": "trophy",
    "\uD83D\uDD0A": "volume", "\uD83D\uDCCB": "clipboard", "\u23F1\uFE0F": "clock",
    "\uD83D\uDCC1": "folder", "\u2328\uFE0F": "keyboard", "\uD83D\uDD17": "link",
    "\uD83D\uDCC8": "trend-up", "\uD83D\uDCC9": "trend-down", "\uD83C\uDFD7\uFE0F": "structure",
    "\uD83D\uDC41\uFE0F": "eye", "\uD83D\uDD04": "refresh", "\u270D\uFE0F": "pen",
    "\uD83C\uDF89": "trophy", "\u23F1": "clock", "\u26A0\uFE0F": "warning",
    "\uD83D\uDCDD": "write", "\uD83D\uDCC4": "clipboard", "\uD83D\uDCF0": "newspaper",
    "\uD83E\uDDED": "compass", "\u26D4": "x"
  };

  var PICKER = ["book", "target", "lightbulb", "pen", "key", "brain", "star", "flame"];

  function resolve(name) {
    if (!name) return "book";
    if (ICONS[name]) return name;
    if (TOPIC[name]) return TOPIC[name];
    if (EMOJI[name]) return EMOJI[name];
    return "book";
  }

  function tile(name, variant, size) {
    var slug = resolve(name);
    var meta = ICONS[slug] || ICONS.book;
    var v = variant || meta.v || "green";
    var sz = size || "md";
    return (
      '<span class="bs-icon-tile bs-icon-tile--' + v + " bs-icon-tile--" + sz + '" aria-hidden="true">' +
      '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">' +
      meta.s + "</svg></span>"
    );
  }

  function inline(name, kind) {
    var slug = resolve(name);
    var meta = ICONS[slug] || ICONS.check;
    var cls = "bs-icon-inline bs-icon-inline--" + (kind || "ok");
    return (
      '<span class="' + cls + '" aria-hidden="true">' +
      '<svg viewBox="0 0 24 24" width="16" height="16" fill="none">' + meta.s + "</svg></span>"
    );
  }

  function setTile(el, name, variant, size) {
    if (!el) return;
    el.innerHTML = tile(name, variant, size);
  }

  global.BSIcons = {
    ICONS: ICONS,
    TOPIC: TOPIC,
    PICKER: PICKER,
    resolve: resolve,
    tile: tile,
    inline: inline,
    setTile: setTile,
    check: function () { return inline("check", "ok"); },
    cross: function () { return inline("x", "bad"); },
    warn: function () { return inline("warning", "warn"); }
  };
})(typeof window !== "undefined" ? window : this);
