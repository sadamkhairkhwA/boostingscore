"""Central SVG icon registry — soft rounded-square tiles, #3B6D11 accent.

Templates: {% load bs_icons %}{% bs_icon "leaf" "green" %}
Python:     icon_html("leaf", "green")
JS:         BSIcons.tile("leaf", "green")  (see static/js/bs-icons.js)

Legacy emoji values in the DB are mapped to icon slugs automatically.
"""

from __future__ import annotations

import html
import re

# slug -> (svg inner HTML, default variant)
ICONS: dict[str, dict] = {
    "leaf": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 18 2c1 2 2 4.5 2 8a9 9 0 1 1-9 10z"/>',
    },
    "heartbeat": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M19 14c1.5-1.3 3-3.2 3-5.5A5.5 5.5 0 0 0 12 5.5 5.5 5.5 0 0 0 5 8.5C5 10.8 6.5 12.7 8 14l4 4 4-4z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 5.5V3"/>',
    },
    "laptop": {
        "variant": "blue",
        "svg": '<rect x="3" y="5" width="18" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M2 19h20"/>',
    },
    "graduation-cap": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M22 9 12 5 2 9l10 4 10-4z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/>',
    },
    "users": {
        "variant": "navy",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M22 21v-2a4 4 0 0 0-3-3.87"/><path fill="none" stroke="currentColor" stroke-width="2" d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    },
    "building": {
        "variant": "navy",
        "svg": '<rect x="4" y="3" width="16" height="18" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M9 7h.01M9 11h.01M9 15h.01M15 7h.01M15 11h.01M15 15h.01"/>',
    },
    "plane": {
        "variant": "blue",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M2 12h5l3-9 4 18 3-9h5"/>',
    },
    "flask": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M9 3h6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M10 3v6.5L5.5 19a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2L14 9.5V3"/>',
    },
    "briefcase": {
        "variant": "orange",
        "svg": '<rect x="3" y="7" width="18" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    },
    "book": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    },
    "book-open": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M3 19V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v13a1 1 0 0 1-1 1H6a3 3 0 0 1-3-3zM6 17h13"/>',
    },
    "star": {
        "variant": "amber",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 2l2.6 6.3L21 9l-5 4.4L17.5 20 12 16.8 6.5 20 8 13.4 3 9l6.4-.7z"/>',
    },
    "flashcards": {
        "variant": "green",
        "svg": '<rect x="3" y="5" width="12" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="8" y="3" width="12" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "list": {
        "variant": "navy",
        "svg": '<line x1="8" y1="6" x2="21" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="18" x2="15" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="4" cy="6" r="1" fill="currentColor"/><circle cx="4" cy="12" r="1" fill="currentColor"/><circle cx="4" cy="18" r="1" fill="currentColor"/>',
    },
    "quiz": {
        "variant": "purple",
        "svg": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M9.5 9.5a2.5 2.5 0 1 1 4.2 1.8c-.6.6-1.2 1-1.2 2.2V14"/><line x1="12" y1="17" x2="12" y2="17.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    },
    "keyboard": {
        "variant": "navy",
        "svg": '<rect x="2" y="6" width="20" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="6" cy="10" r=".5" fill="currentColor"/><circle cx="10" cy="10" r=".5" fill="currentColor"/><circle cx="14" cy="10" r=".5" fill="currentColor"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6 14h8"/>',
    },
    "folder": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.5L10 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2z"/>',
    },
    "guide": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2"/><line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" stroke-width="2"/>',
    },
    "clock": {
        "variant": "green",
        "svg": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 7v5l3 3"/>',
    },
    "flame": {
        "variant": "amber",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 2c1 3 4 4 4 8a4 4 0 1 1-8 0c0-2 1-3 2-4-1 3 1 4 2 4 1 0 2-1 2-2.5C14 5 13 4 12 2z"/>',
    },
    "check": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M5 12l4 4L19 7"/>',
    },
    "x": {
        "variant": "red",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/>',
    },
    "warning": {
        "variant": "amber",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 3L2 20h20L12 3z"/><line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="17" r=".5" fill="currentColor"/>',
    },
    "settings": {
        "variant": "navy",
        "svg": '<circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
    },
    "chart": {
        "variant": "blue",
        "svg": '<line x1="18" y1="20" x2="18" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="12" y1="20" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="6" y1="20" x2="6" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    },
    "map": {
        "variant": "green",
        "svg": '<polygon fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" points="1 6 9 2 15 6 23 2 23 18 15 22 9 18 1 22 1 6"/><circle cx="9" cy="10" r="2" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "pen": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 20h4l10-10-4-4L4 16v4zM14 6l4 4"/>',
    },
    "write": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M14 3v6h6M8 13h8M8 17h5"/>',
    },
    "structure": {
        "variant": "green",
        "svg": '<rect x="3" y="3" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="14" y="3" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="14" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/><rect x="14" y="14" width="7" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "eye": {
        "variant": "blue",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "compass": {
        "variant": "orange",
        "svg": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><polygon fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" points="16 8 14 14 8 16 10 10"/>',
    },
    "newspaper": {
        "variant": "orange",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19h16a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14"/><path fill="none" stroke="currentColor" stroke-width="2" d="M8 7h12M8 11h8M8 15h5"/>',
    },
    "headphones": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 14v-2a8 8 0 0 1 16 0v2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M4 14a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-2a2 2 0 0 1 2-2zM20 14a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2 2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2z"/>',
    },
    "lightbulb": {
        "variant": "amber",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M9 18h6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M10 22h4"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 2a7 7 0 0 0-4 12.7V18h8v-3.3A7 7 0 0 0 12 2z"/>',
    },
    "target": {
        "variant": "green",
        "svg": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="1" fill="currentColor"/>',
    },
    "key": {
        "variant": "navy",
        "svg": '<circle cx="8" cy="15" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 15h9M18 12v6"/>',
    },
    "brain": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M9 4a3 3 0 0 0-3 3v1a2 2 0 0 0 0 4v1a3 3 0 0 0 3 3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M15 4a3 3 0 0 1 3 3v1a2 2 0 0 1 0 4v1a3 3 0 0 1-3 3"/><line x1="12" y1="4" x2="12" y2="20" stroke="currentColor" stroke-width="2"/>',
    },
    "puzzle": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M10 4h4v2a2 2 0 0 0 2 2h2v4h-2a2 2 0 0 0-2 2v2H10v-2a2 2 0 0 0-2-2H6v-4h2a2 2 0 0 0 2-2V4z"/>',
    },
    "level-easy": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    },
    "level-medium": {
        "variant": "blue",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2"/>',
    },
    "level-hard": {
        "variant": "orange",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path fill="none" stroke="currentColor" stroke-width="2" d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7" stroke="currentColor" stroke-width="2"/><line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" stroke-width="2"/>',
    },
    "cards": {
        "variant": "green",
        "svg": '<rect x="3" y="5" width="12" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="8" y="3" width="12" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "clipboard": {
        "variant": "navy",
        "svg": '<rect x="5" y="4" width="14" height="17" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M9 4h6a2 2 0 0 1 2 2v1H7V6a2 2 0 0 1 2-2z"/>',
    },
    "process": {
        "variant": "blue",
        "svg": '<circle cx="6" cy="6" r="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="18" cy="6" r="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="18" r="2" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" d="M8 6h8M7 8l3 8M17 8l-3 8"/>',
    },
    "pie": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 2v10l8.66 5"/><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "scale": {
        "variant": "navy",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 3v18"/><path fill="none" stroke="currentColor" stroke-width="2" d="M5 7h14"/><path fill="none" stroke="currentColor" stroke-width="2" d="M5 7l-3 6h6L5 7zM19 7l-3 6h6l-3-6z"/>',
    },
    "chat": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"/>',
    },
    "city": {
        "variant": "navy",
        "svg": '<rect x="3" y="10" width="6" height="11" fill="none" stroke="currentColor" stroke-width="2"/><rect x="11" y="6" width="5" height="15" fill="none" stroke="currentColor" stroke-width="2"/><rect x="18" y="3" width="3" height="18" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "thumbs-up": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M7 11v8a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-6h5a2 2 0 0 0 2-2l1-6a2 2 0 0 0-2-2h-6l1-4a2 2 0 0 0-2-2 2 2 0 0 0-2 2v4"/>',
    },
    "pin": {
        "variant": "green",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M12 21s6-5.2 6-10a6 6 0 1 0-12 0c0 4.8 6 10 6 10z"/><circle cx="12" cy="11" r="2" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "volume": {
        "variant": "blue",
        "svg": '<polygon fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path fill="none" stroke="currentColor" stroke-width="2" d="M15 9a4 4 0 0 1 0 6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M17 7a7 7 0 0 1 0 10"/>',
    },
    "shuffle": {
        "variant": "navy",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M16 3h5v5"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 20L21 3"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M21 16v5h-5"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M15 15l6 6"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 4l5 5"/>',
    },
    "fullscreen": {
        "variant": "navy",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M8 3H5a2 2 0 0 0-2 2v3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M21 8V5a2 2 0 0 0-2-2h-3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M3 16v3a2 2 0 0 0 2 2h3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M16 21h3a2 2 0 0 0 2-2v-3"/>',
    },
    "trophy": {
        "variant": "amber",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M8 21h8"/><path fill="none" stroke="currentColor" stroke-width="2" d="M12 17v4"/><path fill="none" stroke="currentColor" stroke-width="2" d="M7 4h10v5a5 5 0 0 1-10 0V4z"/><path fill="none" stroke="currentColor" stroke-width="2" d="M7 6H4a2 2 0 0 0 2 3"/><path fill="none" stroke="currentColor" stroke-width="2" d="M17 6h3a2 2 0 0 1-2 3"/>',
    },
    "inbox": {
        "variant": "navy",
        "svg": '<polyline fill="none" stroke="currentColor" stroke-width="2" points="22 12 16 12 14 15 10 15 8 12 2 12"/><path fill="none" stroke="currentColor" stroke-width="2" d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    },
    "star-outline": {
        "variant": "amber",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 2l2.6 6.3L21 9l-5 4.4L17.5 20 12 16.8 6.5 20 8 13.4 3 9l6.4-.7z"/>',
    },
    "link": {
        "variant": "blue",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path fill="none" stroke="currentColor" stroke-width="2" d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    },
    "letters": {
        "variant": "purple",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M4 7V4h16v3"/><line x1="9" y1="20" x2="15" y2="20" stroke="currentColor" stroke-width="2"/><line x1="12" y1="4" x2="12" y2="20" stroke="currentColor" stroke-width="2"/>',
    },
    "refresh": {
        "variant": "navy",
        "svg": '<path fill="none" stroke="currentColor" stroke-width="2" d="M3 2v6h6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M21 12A9 9 0 0 0 6 5.3L3 8"/><path fill="none" stroke="currentColor" stroke-width="2" d="M21 22v-6h-6"/><path fill="none" stroke="currentColor" stroke-width="2" d="M3 12a9 9 0 0 0 15 6.7l3-2.7"/>',
    },
    "trend-up": {
        "variant": "green",
        "svg": '<polyline fill="none" stroke="currentColor" stroke-width="2" points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline fill="none" stroke="currentColor" stroke-width="2" points="17 6 23 6 23 12"/>',
    },
    "trend-down": {
        "variant": "red",
        "svg": '<polyline fill="none" stroke="currentColor" stroke-width="2" points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline fill="none" stroke="currentColor" stroke-width="2" points="17 18 23 18 23 12"/>',
    },
}

TOPIC_ICONS = {
    "environment": "leaf",
    "health": "heartbeat",
    "technology": "laptop",
    "education": "graduation-cap",
    "society": "building",
    "travel": "plane",
    "science": "flask",
    "business": "briefcase",
    "other": "star",
}

LEVEL_ICONS = {1: "level-easy", 2: "level-medium", 3: "level-hard"}

DECK_PICKER_ICONS = ["book", "target", "lightbulb", "pen", "key", "brain", "star", "flame"]

_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F900-\U0001F9FF"
    "]+",
    flags=re.UNICODE,
)

# Legacy emoji -> icon slug (DB / old content)
EMOJI_TO_ICON: dict[str, str] = {
    "🌿": "leaf", "🩺": "heartbeat", "🏥": "heartbeat", "💻": "laptop",
    "🎓": "graduation-cap", "📚": "book", "🏙️": "city", "🏛️": "building",
    "✈️": "plane", "🔬": "flask", "💼": "briefcase", "📇": "cards",
    "⭐": "star", "📖": "book", "🎯": "target", "💡": "lightbulb",
    "✏️": "pen", "🔑": "key", "🧠": "brain", "🔥": "flame",
    "📗": "level-easy", "📘": "level-medium", "📙": "level-hard",
    "👥": "users", "🧩": "puzzle", "📊": "chart", "📈": "chart",
    "🥧": "pie", "📋": "clipboard", "⚙️": "process", "🗺️": "map",
    "💬": "chat", "❓": "quiz", "⚖️": "scale", "🏗️": "structure",
    "✍️": "pen", "👁️": "eye", "📝": "write", "🏁": "check",
    "🧭": "compass", "📰": "newspaper", "📘": "level-medium",
    "🌟": "star", "✅": "check", "👍": "thumbs-up", "⚠": "warning",
    "⚠️": "warning", "⚙": "settings", "📍": "pin", "💡": "lightbulb",
    "⌨️": "keyboard", "⌨": "keyboard", "🗂️": "folder", "🗂": "folder",
    "📭": "inbox", "🏆": "trophy", "🔀": "shuffle", "⛶": "fullscreen",
    "🔊": "volume", "🔗": "link", "🔤": "letters", "🎧": "headphones",
    "📈": "trend-up", "📉": "trend-down", "☆": "star-outline", "★": "star",
}


def resolve_icon(value: str | None, default: str = "book") -> str:
    """Map icon slug, topic slug, or legacy emoji to a known icon slug."""
    if not value:
        return default
    v = value.strip()
    if v in ICONS:
        return v
    if v in TOPIC_ICONS:
        return TOPIC_ICONS[v]
    if v in EMOJI_TO_ICON:
        return EMOJI_TO_ICON[v]
    if _EMOJI_RE.search(v):
        return EMOJI_TO_ICON.get(v, default)
    return default


def icon_html(
    name: str,
    variant: str | None = None,
    *,
    size: str = "md",
    extra_class: str = "",
) -> str:
    slug = resolve_icon(name)
    meta = ICONS.get(slug, ICONS["book"])
    var = variant or meta.get("variant", "green")
    cls = f"bs-icon-tile bs-icon-tile--{var} bs-icon-tile--{size}"
    if extra_class:
        cls += f" {extra_class}"
    svg = meta["svg"]
    return (
        f'<span class="{html.escape(cls)}" aria-hidden="true">'
        f'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg">{svg}</svg></span>'
    )


def topic_icon_html(topic: str, size: str = "md") -> str:
    return icon_html(TOPIC_ICONS.get(topic, "book"), size=size)
