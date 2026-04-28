from html import escape
import math


def _svg_wrap(inner: str, width: int = 900, height: int = 420) -> str:
    return (
        f'<svg class="wt1-svg" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Task 1 chart">{inner}</svg>'
    )


def _legend(items, x=90, y=378):
    out = []
    cx = x
    for label, color in items:
        out.append(f'<rect x="{cx}" y="{y}" width="18" height="18" rx="4" fill="{color}" />')
        out.append(
            f'<text x="{cx + 24}" y="{y + 13}" font-size="12" fill="#334155" font-weight="600">{escape(str(label))}</text>'
        )
        cx += 120
    return "".join(out)


def render_bar_chart(chart):
    groups = chart["groups"]
    series = chart["series"]
    title = escape(chart["title"])
    w = 900
    h = 420
    left, right, top, bottom = 80, 30, 58, 92
    pw, ph = w - left - right, h - top - bottom
    max_v = max(max(s["values"]) for s in series)
    y_max = int(math.ceil(max_v / 20.0) * 20)
    y_max = max(20, y_max)
    grid = []
    for v in range(0, y_max + 1, 20):
        y = top + ph - (v / y_max) * ph
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+pw}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        grid.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="#94a3b8">{v}</text>')
    group_w = pw / max(1, len(groups))
    bar_w = min(32, (group_w * 0.72) / max(1, len(series)))
    bars = []
    for gi, g in enumerate(groups):
        gx = left + gi * group_w
        for si, s in enumerate(series):
            val = s["values"][gi]
            bh = (val / y_max) * ph
            x = gx + (group_w - (bar_w * len(series))) / 2 + si * bar_w
            y = top + ph - bh
            bars.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w-3:.1f}" height="{bh:.1f}" rx="5" fill="{s["color"]}" />'
            )
            bars.append(
                f'<text x="{x + (bar_w-3)/2:.1f}" y="{y-7:.1f}" text-anchor="middle" font-size="11" fill="{s["color"]}" font-weight="700">{val}</text>'
            )
        bars.append(
            f'<text x="{gx + group_w/2:.1f}" y="{top + ph + 22:.1f}" text-anchor="middle" font-size="12" fill="#475569">{escape(g)}</text>'
        )
    inner = (
        f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{title}</text>'
        + "".join(grid)
        + "".join(bars)
        + _legend([(s["name"], s["color"]) for s in series], x=left, y=h - 34)
    )
    return _svg_wrap(inner, w, h)


def render_line_chart(chart):
    x_labels = chart["x"]
    series = chart["series"]
    title = escape(chart["title"])
    w, h = 900, 420
    left, right, top, bottom = 80, 30, 58, 92
    pw, ph = w - left - right, h - top - bottom
    max_v = max(max(s["values"]) for s in series)
    y_max = int(math.ceil(max_v / 25.0) * 25)
    y_max = max(25, y_max)
    grid = []
    for v in range(0, y_max + 1, 25):
        y = top + ph - (v / y_max) * ph
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+pw}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        grid.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="#94a3b8">{v}</text>')
    step_x = pw / max(1, len(x_labels) - 1)
    x_axis = []
    for i, lbl in enumerate(x_labels):
        x = left + i * step_x
        x_axis.append(f'<text x="{x:.1f}" y="{top+ph+22}" text-anchor="middle" font-size="12" fill="#475569">{escape(lbl)}</text>')
    lines = []
    for s in series:
        pts = []
        for i, v in enumerate(s["values"]):
            x = left + i * step_x
            y = top + ph - (v / y_max) * ph
            pts.append((x, y, v))
        d = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
        lines.append(f'<polyline fill="none" stroke="{s["color"]}" stroke-width="3" points="{d}" />')
        for x, y, v in pts:
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{s["color"]}" />')
            lines.append(f'<text x="{x:.1f}" y="{y-8:.1f}" text-anchor="middle" font-size="10" fill="{s["color"]}">{v}</text>')
    inner = (
        f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{title}</text>'
        + "".join(grid)
        + "".join(lines)
        + "".join(x_axis)
        + _legend([(s["name"], s["color"]) for s in series], x=left, y=h - 34)
    )
    return _svg_wrap(inner, w, h)


def _pie_paths(values, cx, cy, r, colors):
    total = sum(values) or 1
    out = []
    angle = -90.0
    for i, v in enumerate(values):
        frac = v / total
        delta = frac * 360
        end = angle + delta
        x1 = cx + r * math.cos(math.radians(angle))
        y1 = cy + r * math.sin(math.radians(angle))
        x2 = cx + r * math.cos(math.radians(end))
        y2 = cy + r * math.sin(math.radians(end))
        large = 1 if delta > 180 else 0
        d = f"M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f} Z"
        out.append(f'<path d="{d}" fill="{colors[i % len(colors)]}" stroke="#fff" stroke-width="1"/>')
        mid = angle + delta / 2
        tx = cx + r * 0.62 * math.cos(math.radians(mid))
        ty = cy + r * 0.62 * math.sin(math.radians(mid))
        out.append(
            f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700">{int(v)}%</text>'
        )
        angle = end
    return "".join(out)


def render_pie_chart(chart):
    colors = ["#1e3a5f", "#4b9cf0", "#2d6a0a", "#b45309", "#7c3aed", "#db2777"]
    w, h = 900, 430
    title = escape(chart["title"])
    inner = [f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{title}</text>']
    inner.append(f'<text x="275" y="64" text-anchor="middle" font-size="14" fill="#334155" font-weight="700">{escape(chart["left_year"])}</text>')
    inner.append(f'<text x="625" y="64" text-anchor="middle" font-size="14" fill="#334155" font-weight="700">{escape(chart["right_year"])}</text>')
    inner.append(_pie_paths(chart["left"], 275, 190, 105, colors))
    inner.append(_pie_paths(chart["right"], 625, 190, 105, colors))
    inner.append(_legend(list(zip(chart["labels"], colors)), x=95, y=365))
    return _svg_wrap("".join(inner), w, h)


def render_process_chart(chart):
    steps = chart["steps"]
    w = 900
    box_w = 650
    box_h = 44
    gap = 16
    h = 90 + len(steps) * (box_h + gap) + 20
    x = (w - box_w) / 2
    y = 52
    inner = [f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{escape(chart["title"])}</text>']
    for i, step in enumerate(steps, start=1):
        fy = y + (i - 1) * (box_h + gap)
        fill = "#1e3a5f" if i % 2 else "#2f5f91"
        inner.append(f'<rect x="{x}" y="{fy}" width="{box_w}" height="{box_h}" rx="10" fill="{fill}" />')
        inner.append(f'<circle cx="{x-28}" cy="{fy + box_h/2}" r="15" fill="#0f172a" />')
        inner.append(f'<text x="{x-28}" y="{fy + box_h/2 + 4}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700">{i}</text>')
        inner.append(
            f'<text x="{x+14}" y="{fy + 27}" font-size="14" fill="#fff">{escape(step)}</text>'
        )
        if i < len(steps):
            ay = fy + box_h + 10
            inner.append(f'<line x1="{w/2}" y1="{ay}" x2="{w/2}" y2="{ay+8}" stroke="#64748b" stroke-width="2"/>')
            inner.append(f'<polygon points="{w/2-5},{ay+8} {w/2+5},{ay+8} {w/2},{ay+14}" fill="#64748b"/>')
    return _svg_wrap("".join(inner), w, h)


def render_table_chart(chart):
    headers = chart["headers"]
    rows = chart["rows"]
    w, h = 900, 410
    left, top = 34, 56
    col_w = [180, 140, 140, 140, 220]
    row_h = 44
    inner = [f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{escape(chart["title"])}</text>']
    x = left
    for i, head in enumerate(headers):
        inner.append(f'<rect x="{x}" y="{top}" width="{col_w[i]}" height="{row_h}" fill="#1e3a5f" />')
        inner.append(f'<text x="{x+8}" y="{top+27}" font-size="13" fill="#fff" font-weight="700">{escape(head)}</text>')
        x += col_w[i]
    for ri, row in enumerate(rows):
        y = top + row_h + ri * row_h
        bg = "#fff" if ri % 2 == 0 else "#f8fafc"
        x = left
        for ci, val in enumerate(row):
            inner.append(f'<rect x="{x}" y="{y}" width="{col_w[ci]}" height="{row_h}" fill="{bg}" stroke="#e2e8f0"/>')
            color = "#334155"
            if ci == len(row) - 1 and "↑" in val:
                color = "#166534"
            elif ci == len(row) - 1 and "↓" in val:
                color = "#b91c1c"
            inner.append(f'<text x="{x+8}" y="{y+27}" font-size="12" fill="{color}">{escape(val)}</text>')
            x += col_w[ci]
    return _svg_wrap("".join(inner), w, h)


def render_map_chart(chart):
    w, h = 900, 420
    left_x, right_x, top = 70, 500, 70
    panel_w, panel_h = 320, 260
    inner = [f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{escape(chart["title"])}</text>']
    inner.append(f'<rect x="{left_x}" y="{top}" width="{panel_w}" height="{panel_h}" rx="12" fill="#f8fafc" stroke="#cbd5e1"/>')
    inner.append(f'<rect x="{right_x}" y="{top}" width="{panel_w}" height="{panel_h}" rx="12" fill="#f8fafc" stroke="#cbd5e1"/>')
    inner.append(f'<text x="{left_x+panel_w/2}" y="{top+24}" text-anchor="middle" font-size="14" fill="#334155" font-weight="700">{escape(chart["left_label"])}</text>')
    inner.append(f'<text x="{right_x+panel_w/2}" y="{top+24}" text-anchor="middle" font-size="14" fill="#334155" font-weight="700">{escape(chart["right_label"])}</text>')
    inner.append(f'<text x="{450}" y="{200}" text-anchor="middle" font-size="28" fill="#64748b">→</text>')
    def block(base_x, items, color):
        out = []
        for i, name in enumerate(items):
            x = base_x + 18 + (i % 2) * 154
            y = top + 42 + (i // 2) * 54
            out.append(f'<rect x="{x}" y="{y}" width="140" height="40" rx="8" fill="{color}" />')
            out.append(f'<text x="{x+70}" y="{y+24}" text-anchor="middle" font-size="11" fill="#fff">{escape(name)}</text>')
        return "".join(out)
    inner.append(block(left_x, chart["left"], "#94a3b8"))
    inner.append(block(right_x, chart["right"], "#ef4444"))
    inner.append('<rect x="230" y="362" width="14" height="14" fill="#ef4444"/><text x="250" y="373" font-size="12" fill="#334155">New</text>')
    inner.append('<rect x="310" y="362" width="14" height="14" fill="#22c55e"/><text x="330" y="373" font-size="12" fill="#334155">Expanded</text>')
    inner.append('<rect x="422" y="362" width="14" height="14" fill="#94a3b8"/><text x="442" y="373" font-size="12" fill="#334155">Removed</text>')
    return _svg_wrap("".join(inner), w, h)


def render_mixed_chart(chart):
    x_labels = chart["x"]
    bars = chart["bars"]
    line = chart["line"]
    w, h = 900, 460
    left, right, top = 80, 30, 56
    usable_h = h - top - 72
    split = top + usable_h * 0.55
    pw = w - left - right
    step_x = pw / max(1, len(x_labels) - 1)
    inner = [f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="#334155">{escape(chart["title"])}</text>']
    inner.append(f'<line x1="{left}" y1="{split}" x2="{left+pw}" y2="{split}" stroke="#cbd5e1" stroke-width="2"/>')
    max_bar = max(bars)
    bar_h = split - top - 30
    for i, v in enumerate(bars):
        x = left + i * step_x - 16
        hh = (v / max_bar) * bar_h
        y = split - hh - 6
        inner.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="30" height="{hh:.1f}" rx="5" fill="#1e3a5f"/>')
        inner.append(f'<text x="{x+15:.1f}" y="{y-6:.1f}" text-anchor="middle" font-size="10" fill="#1e3a5f">{v}</text>')
    max_line = max(line)
    min_line = min(line)
    line_h = h - split - 40
    pts = []
    for i, v in enumerate(line):
        x = left + i * step_x
        y = split + 22 + line_h - ((v - min_line) / (max_line - min_line or 1)) * line_h
        pts.append((x, y, v))
    inner.append('<polyline fill="none" stroke="#4b9cf0" stroke-width="3" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts) + '"/>')
    for x, y, v in pts:
        inner.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#4b9cf0"/>')
        inner.append(f'<text x="{x:.1f}" y="{y-8:.1f}" text-anchor="middle" font-size="10" fill="#4b9cf0">{v}</text>')
    for i, lbl in enumerate(x_labels):
        x = left + i * step_x
        inner.append(f'<text x="{x:.1f}" y="{h-20}" text-anchor="middle" font-size="11" fill="#475569">{escape(lbl)}</text>')
    inner.append(_legend([("Population (millions)", "#1e3a5f"), ("GDP per capita ($k)", "#4b9cf0")], x=left, y=h - 44))
    return _svg_wrap("".join(inner), w, h)


def render_question_chart(question):
    chart = question["chart"]
    kind = chart["kind"]
    if kind == "bar":
        return render_bar_chart(chart)
    if kind == "line":
        return render_line_chart(chart)
    if kind == "pie":
        return render_pie_chart(chart)
    if kind == "process":
        return render_process_chart(chart)
    if kind == "table":
        return render_table_chart(chart)
    if kind == "map":
        return render_map_chart(chart)
    if kind == "mixed":
        return render_mixed_chart(chart)
    return _svg_wrap('<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle">No chart</text>')
