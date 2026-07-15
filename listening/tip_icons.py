"""SVG icon slugs for listening tips (by question type, tip order)."""

TYPE_TIP_ICONS: dict[str, list[str]] = {
    "multiple-choice": ["eye", "brain", "lightbulb", "check"],
    "gap-fill": ["clipboard", "list", "pen", "map"],
    "sentence": ["letters", "book-open", "clock"],
    "matching": ["list", "users", "puzzle"],
    "map": ["pin", "compass", "map"],
    "short-answer": ["list", "lightbulb", "pen"],
}

TYPE_SET_ICONS: dict[str, list[str]] = {
    "multiple-choice": ["building", "book", "briefcase", "heartbeat", "compass"],
    "gap-fill": ["clipboard", "building", "car", "tree", "music"],
    "sentence": ["book-open", "water", "moon", "layers", "bird"],
    "matching": ["users", "image", "presentation", "heart", "briefcase"],
    "map": ["map", "building", "image", "tree", "heartbeat"],
    "short-answer": ["lightbulb", "water", "briefcase", "book", "heartbeat"],
}
