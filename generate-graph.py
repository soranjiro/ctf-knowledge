from __future__ import annotations

import html
import json
import os
import pathlib
import re

ROOT_DIR = pathlib.Path(__file__).resolve().parent
OUTPUT_FILE = ROOT_DIR / 'graph.html'
CONTENT_ROOTS = ('insights', 'relations', 'writeup')

KIND_META = {
    'insights': {'label': 'Insights', 'color': '#d97706', 'fill': '#fff7ed', 'border': '#fdba74', 'column': 0},
    'relations': {'label': 'Relations', 'color': '#0f766e', 'fill': '#f0fdfa', 'border': '#5eead4', 'column': 1},
    'writeup': {'label': 'Writeups', 'color': '#2563eb', 'fill': '#eff6ff', 'border': '#93c5fd', 'column': 2},
}


def normalize_path(file_path: pathlib.Path) -> str:
    return file_path.as_posix()


def walk_markdown_files(root: pathlib.Path) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for current_dir, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name != '.git']
        for filename in filenames:
            if filename.endswith('.md'):
                files.append(pathlib.Path(current_dir) / filename)
    return files


def strip_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith('---\n'):
        return '', text

    end_index = text.find('\n---\n', 4)
    if end_index == -1:
        return '', text

    return text[4:end_index], text[end_index + 5 :]


def parse_frontmatter(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    current_list_key = ''

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            current_list_key = ''
            continue

        list_match = re.match(r'^\s*-\s+(.*)$', line)
        if list_match and current_list_key:
            result.setdefault(current_list_key, [])
            assert isinstance(result[current_list_key], list)
            result[current_list_key].append(list_match.group(1).strip())
            continue

        pair_match = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if not pair_match:
            current_list_key = ''
            continue

        key = pair_match.group(1)
        raw_value = pair_match.group(2)
        if not raw_value:
            result[key] = []
            current_list_key = key
            continue

        current_list_key = ''
        result[key] = raw_value

    return result


def get_title(text: str, fallback: str) -> str:
    match = re.search(r'^#\s+(.+)$', text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def classify_node(rel_path: str) -> str:
    for root in CONTENT_ROOTS:
        if rel_path == root or rel_path.startswith(f'{root}/'):
            return root
    return 'other'


def resolve_internal_link(from_path: pathlib.Path, raw_target: str) -> str | None:
    if not raw_target or '://' in raw_target or raw_target.startswith('#'):
        return None

    clean_target = raw_target.split('#', 1)[0].split('?', 1)[0]
    if not clean_target.endswith('.md'):
        return None

    abs_path = (from_path.parent / clean_target).resolve()
    try:
        rel_path = abs_path.relative_to(ROOT_DIR)
    except ValueError:
        return None

    return rel_path.as_posix()


def extract_links(text: str, from_path: pathlib.Path) -> list[str]:
    pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
    links: list[str] = []
    for match in pattern.finditer(text):
        target = resolve_internal_link(from_path, match.group(1).strip())
        if target:
            links.append(target)
    return links


def to_label(value: object) -> str:
    text = str(value)
    text = text.replace('-', ' ').replace('_', ' ')
    return re.sub(r'\b\w', lambda match: match.group(0).upper(), text)


def escape_html(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_meta_chips(node: dict[str, object]) -> str:
    chips: list[str] = []
    kind = node['kind']
    meta = node['meta']

    if kind == 'writeup':
        if isinstance(meta.get('category'), str):
            chips.append(f"category: {to_label(meta['category'])}")
        if isinstance(meta.get('genre'), str):
            chips.append(f"genre: {to_label(meta['genre'])}")
        if isinstance(meta.get('difficulty'), str):
            chips.append(f"difficulty: {to_label(meta['difficulty'])}")
        if isinstance(meta.get('tags'), list):
            chips.extend(f"tag: {to_label(tag)}" for tag in meta['tags'][:3])

    if kind == 'insights':
        category = node['rel_path'].split('/')[1] if '/' in node['rel_path'] else 'general'
        chips.append(f"area: {to_label(category)}")

    if kind == 'relations':
        topic = pathlib.Path(node['rel_path']).stem
        chips.append(f"topic: {to_label(topic)}")

    return ''.join(f'<span class="chip">{escape_html(chip)}</span>' for chip in chips[:4])


def group_by_kind(nodes: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    grouped = {'insights': [], 'relations': [], 'writeup': [], 'other': []}
    for node in nodes:
        grouped.setdefault(node['kind'], grouped['other'])
        grouped[node['kind']].append(node)
    return grouped


def build_html(nodes: list[dict[str, object]], edges: list[dict[str, object]]) -> str:
    # Static full-screen graph layout.
    # Compute degrees.
    deg = {node['id']: 0 for node in nodes}
    for e in edges:
        deg[e['source']] = deg.get(e['source'], 0) + 1
        deg[e['target']] = deg.get(e['target'], 0) + 1

    # Attach degree and a short label.
    for node in nodes:
        node['degree'] = deg.get(node['id'], 0)
        label = ''
        # show compact labels for category/relationship nodes only.
        try:
            if node['kind'] == 'writeup':
                label = ''
            elif node['kind'] == 'insights':
                parts = node['rel_path'].split('/')
                if len(parts) >= 2:
                    label = pathlib.Path(parts[1]).stem
            else:
                label = pathlib.Path(node['rel_path']).stem
        except Exception:
            label = ''
        node['displayLabel'] = label

    dataset = json.dumps({'nodes': nodes, 'edges': edges}, ensure_ascii=False)

    # Return minimalist full-screen HTML with an embedded static layout.
    template = '''<!doctype html>
<html lang="ja">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Knowledge Graph</title>
    <style>
        html,body { height:100%; margin:0; background:#0f172a; color:#e6eef8; font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
        #canvas { width:100%; height:100vh; display:block; }
        .node-label { pointer-events: none; font-weight:700; font-size:11px; fill:#e6eef8; opacity:0.92; }
        .edge { stroke: rgba(255,255,255,0.10); stroke-width:1.2; }
        .tooltip { position:fixed; background:rgba(2,6,23,0.95); color:#cfe8ff; padding:10px 12px; border-radius:8px; font-size:13px; box-shadow:0 8px 30px rgba(2,6,23,0.6); max-width:360px; display:none; z-index:9999; }
        .chip { display:inline-block; background:rgba(255,255,255,0.06); color:#dbeafe; padding:4px 8px; border-radius:999px; margin:2px; font-size:11px; }
        .controls { position:fixed; left:12px; top:12px; z-index:9999; background:rgba(255,255,255,0.05); padding:8px 10px; border-radius:8px; font-size:13px; color:#e6eef8; display:flex; align-items:center; gap:10px; border:1px solid rgba(255,255,255,0.09); }
        .sidebar-toggle { appearance:none; border:1px solid rgba(255,255,255,0.16); background:rgba(255,255,255,0.08); color:#e6eef8; border-radius:6px; font:inherit; padding:4px 8px; cursor:pointer; }
        .sidebar-toggle:hover { background:rgba(255,255,255,0.14); }
        .sidebar { position:fixed; top:0; right:0; width:min(390px, 88vw); height:100vh; z-index:9998; background:rgba(2,6,23,0.96); border-left:1px solid rgba(255,255,255,0.10); box-shadow:-16px 0 40px rgba(0,0,0,0.35); transform:translateX(0); transition:transform 160ms ease; display:flex; flex-direction:column; }
        .sidebar.closed { transform:translateX(100%); }
        .sidebar-header { height:48px; display:flex; align-items:center; justify-content:space-between; gap:8px; padding:0 14px; border-bottom:1px solid rgba(255,255,255,0.08); font-weight:800; }
        .sidebar-close { appearance:none; border:0; background:transparent; color:#cfe8ff; font-size:22px; line-height:1; cursor:pointer; padding:4px 8px; border-radius:6px; }
        .sidebar-close:hover { background:rgba(255,255,255,0.10); }
        .tree { overflow:auto; padding:10px 12px 18px; font-size:13px; }
        .tree details { margin:2px 0; }
        .tree summary { cursor:pointer; color:#dbeafe; padding:4px 6px; border-radius:6px; user-select:none; }
        .tree summary:hover { background:rgba(255,255,255,0.08); }
        .tree-children { margin-left:14px; border-left:1px solid rgba(255,255,255,0.08); padding-left:8px; }
        .tree-file { display:block; color:#bfdbfe; text-decoration:none; padding:4px 6px; border-radius:6px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
        .tree-file:hover { background:rgba(96,165,250,0.16); color:#eff6ff; }
        .reader { position:fixed; top:0; right:0; width:min(720px, 48vw); height:100vh; z-index:9997; background:#f8fafc; color:#111827; border-left:1px solid #cbd5e1; box-shadow:-18px 0 46px rgba(0,0,0,0.34); transform:translateX(100%); transition:transform 180ms ease; display:flex; flex-direction:column; }
        .reader.open { transform:translateX(0); }
        body.reader-open #canvas { width:max(360px, calc(100vw - min(720px, 48vw))); }
        .reader-header { min-height:58px; display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0 18px; border-bottom:1px solid #e2e8f0; background:#ffffff; }
        .reader-title { min-width:0; }
        .reader-title strong { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:15px; }
        .reader-title span { display:block; color:#64748b; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:12px; margin-top:2px; }
        .reader-close { appearance:none; border:0; background:transparent; color:#334155; font-size:26px; line-height:1; cursor:pointer; padding:4px 8px; border-radius:6px; }
        .reader-close:hover { background:#e2e8f0; }
        .reader-body { overflow:auto; padding:28px min(52px, 7vw) 56px; line-height:1.68; font-size:15px; }
        .reader-body h1 { font-size:30px; line-height:1.25; margin:0 0 20px; }
        .reader-body h2 { font-size:22px; margin:30px 0 12px; border-bottom:1px solid #e2e8f0; padding-bottom:6px; }
        .reader-body h3 { font-size:18px; margin:24px 0 8px; }
        .reader-body p { margin:10px 0; }
        .reader-body ul, .reader-body ol { padding-left:24px; margin:10px 0; }
        .reader-body blockquote { margin:14px 0; padding:8px 14px; border-left:4px solid #cbd5e1; color:#475569; background:#f1f5f9; }
        .reader-body code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:0.92em; background:#e2e8f0; border-radius:4px; padding:0.12em 0.32em; }
        .reader-body pre { background:#0f172a; color:#e2e8f0; border-radius:8px; padding:14px 16px; overflow:auto; }
        .reader-body pre code { background:transparent; color:inherit; padding:0; }
        .reader-body a { color:#2563eb; text-decoration:none; }
        .reader-body a:hover { text-decoration:underline; }
        .reader-empty { color:#64748b; }
        .node-circle { stroke: rgba(255,255,255,0.14); stroke-width:1.2; cursor:pointer; }
        .node-circle:active { cursor:grabbing; }
        @media (max-width: 900px) {
            body.reader-open #canvas { width:100%; }
            .reader { width:100vw; }
        }
    </style>
</head>
<body>
    <div class="controls"><button id="sidebar-toggle" class="sidebar-toggle" type="button">Tree</button><span>Nodes: {NODES_COUNT} • Edges: {EDGES_COUNT}</span></div>
    <aside id="sidebar" class="sidebar closed" aria-label="Knowledge files">
        <div class="sidebar-header">
            <span>Files</span>
            <button id="sidebar-close" class="sidebar-close" type="button" aria-label="Close">×</button>
        </div>
        <nav id="tree" class="tree"></nav>
    </aside>
    <aside id="reader" class="reader" aria-label="Markdown preview">
        <div class="reader-header">
            <div class="reader-title">
                <strong id="reader-heading">No file selected</strong>
                <span id="reader-path"></span>
            </div>
            <button id="reader-close" class="reader-close" type="button" aria-label="Close">×</button>
        </div>
        <article id="reader-body" class="reader-body"></article>
    </aside>
    <div id="canvas"></div>
    <div id="tooltip" class="tooltip"></div>
    <script id="graph-data" type="application/json">__DATASET__</script>
    <script>
        const data = JSON.parse(document.getElementById('graph-data').textContent);
        const nodes = data.nodes.map(n => (Object.assign({}, n)));
        const edges = data.edges.map(e => (Object.assign({}, e)));

        const canvas = document.getElementById('canvas');
        const w = Math.max(window.innerWidth, 800);
        const h = Math.max(window.innerHeight, 600);
        const svgNS = 'http://www.w3.org/2000/svg';
        const svg = document.createElementNS(svgNS, 'svg');
        svg.setAttribute('width', '100%');
        svg.setAttribute('height', '100%');
        svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
        canvas.appendChild(svg);
        // top-level group; layout is computed once and then fitted into the viewBox.
        const gAll = document.createElementNS(svgNS, 'g');
        svg.appendChild(gAll);

        const nodeById = new Map(nodes.map(n => [n.id, n]));
        const centerX = w / 2;
        const centerY = h / 2;
        nodes.forEach(n => {
            n.x = centerX;
            n.y = centerY;
            n.vx = 0; n.vy = 0;
            n.r = 6 + Math.sqrt(n.degree || 0) * 3; // size by degree
        });

        const edgeEls = edges.map(e => {
            const line = document.createElementNS(svgNS, 'line');
            line.classList.add('edge');
            gAll.appendChild(line);
            return { el: line, data: e };
        });

        const nodeGroup = nodes.map(n => {
            const g = document.createElementNS(svgNS, 'g');
            const c = document.createElementNS(svgNS, 'circle');
            c.setAttribute('r', String(n.r));
            c.setAttribute('fill', n.kind === 'insights' ? '#f97316' : (n.kind === 'relations' ? '#06b6d4' : '#60a5fa'));
            c.classList.add('node-circle');
            g.appendChild(c);
            const label = document.createElementNS(svgNS, 'text');
            label.setAttribute('y', '0');
            label.setAttribute('text-anchor', 'middle');
            label.setAttribute('dominant-baseline', 'middle');
            label.classList.add('node-label');
            label.textContent = n.displayLabel || '';
            g.appendChild(label);
            gAll.appendChild(g);
            return { g, c, label, node: n };
        });

        const tooltip = document.getElementById('tooltip');

        function showTooltip(n, clientX, clientY) {
            const html = [];
            html.push(`<div style="font-weight:800; font-size:14px; margin-bottom:6px">${escapeHtml(n.title || n.id)}</div>`);
            if (n.rel_path) html.push(`<div style="color:#9fb7d8; font-size:12px; margin-bottom:6px">${escapeHtml(n.rel_path)}</div>`);
            const chips = [];
            if (n.meta && n.meta.category) chips.push(n.meta.category);
            if (n.meta && n.meta.genre) chips.push(n.meta.genre);
            if (n.meta && n.meta.difficulty) chips.push(n.meta.difficulty);
            if (n.meta && Array.isArray(n.meta.tags)) chips.push(...n.meta.tags);
            if (chips.length) html.push('<div>' + chips.slice(0,6).map(c=>`<span class="chip">${escapeHtml(c)}</span>`).join('') + '</div>');
            tooltip.innerHTML = html.join('');
            tooltip.style.display = 'block';
            const x = Math.min(window.innerWidth - 380, clientX + 12);
            const y = Math.min(window.innerHeight - 80, clientY + 12);
            tooltip.style.left = x + 'px';
            tooltip.style.top = y + 'px';
        }

        function hideTooltip() { tooltip.style.display = 'none'; }

        function escapeHtml(s){ return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'); }
        function fileUrl(path) { return encodeURI(path).replaceAll('#', '%23'); }
        function openNodeFile(node) {
            if (!node || !node.rel_path) return;
            openReader(node);
        }
        function splitFrontmatter(text) {
            if (!text.startsWith('---\\n')) return text;
            const end = text.indexOf('\\n---\\n', 4);
            return end === -1 ? text : text.slice(end + 5);
        }
        function renderInline(text, basePath) {
            return escapeHtml(text)
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, (match, label, href) => {
                    const cleanHref = href.split('#', 1)[0];
                    const target = cleanHref.endsWith('.md') ? resolveMarkdownPath(cleanHref, basePath) : '';
                    const attr = target ? ` data-target="${escapeHtml(target)}" href="#"` : ` href="${escapeHtml(href)}" target="_blank" rel="noopener"`;
                    return `<a${attr}>${label}</a>`;
                });
        }
        function resolveMarkdownPath(href, basePath) {
            if (href.includes('://') || href.startsWith('#')) return '';
            const baseParts = (basePath || '').split('/');
            baseParts.pop();
            const path = href.split('#', 1)[0].split('?').shift();
            path.split('/').forEach(part => {
                if (!part || part === '.') return;
                if (part === '..') baseParts.pop();
                else baseParts.push(part);
            });
            return baseParts.join('/');
        }
        function renderMarkdown(markdown, basePath) {
            const lines = splitFrontmatter(markdown || '').replace(/\\r\\n/g, '\\n').split('\\n');
            const out = [];
            let paragraph = [];
            let list = null;
            let inCode = false;
            let codeLines = [];

            function flushParagraph() {
                if (!paragraph.length) return;
                out.push(`<p>${renderInline(paragraph.join(' '), basePath)}</p>`);
                paragraph = [];
            }
            function flushList() {
                if (!list) return;
                out.push(`<${list.tag}>${list.items.map(item => `<li>${renderInline(item, basePath)}</li>`).join('')}</${list.tag}>`);
                list = null;
            }

            lines.forEach(line => {
                if (line.startsWith('```')) {
                    if (inCode) {
                        out.push(`<pre><code>${escapeHtml(codeLines.join('\\n'))}</code></pre>`);
                        inCode = false;
                        codeLines = [];
                    } else {
                        flushParagraph();
                        flushList();
                        inCode = true;
                    }
                    return;
                }
                if (inCode) {
                    codeLines.push(line);
                    return;
                }
                if (!line.trim()) {
                    flushParagraph();
                    flushList();
                    return;
                }
                const heading = line.match(/^(#{1,3})\\s+(.+)$/);
                if (heading) {
                    flushParagraph();
                    flushList();
                    const level = heading[1].length;
                    out.push(`<h${level}>${renderInline(heading[2].trim(), basePath)}</h${level}>`);
                    return;
                }
                const quote = line.match(/^>\\s?(.*)$/);
                if (quote) {
                    flushParagraph();
                    flushList();
                    out.push(`<blockquote>${renderInline(quote[1], basePath)}</blockquote>`);
                    return;
                }
                const ordered = line.match(/^\\s*\\d+\\.\\s+(.+)$/);
                const unordered = line.match(/^\\s*[-*]\\s+(.+)$/);
                if (ordered || unordered) {
                    flushParagraph();
                    const tag = ordered ? 'ol' : 'ul';
                    if (!list || list.tag !== tag) flushList();
                    if (!list) list = { tag, items: [] };
                    list.items.push((ordered || unordered)[1]);
                    return;
                }
                paragraph.push(line.trim());
            });
            if (inCode) out.push(`<pre><code>${escapeHtml(codeLines.join('\\n'))}</code></pre>`);
            flushParagraph();
            flushList();
            return out.join('\\n') || '<p class="reader-empty">No content.</p>';
        }
        function openReader(node) {
            const reader = document.getElementById('reader');
            document.getElementById('reader-heading').textContent = node.title || node.id;
            document.getElementById('reader-path').textContent = node.rel_path || '';
            const body = document.getElementById('reader-body');
            body.innerHTML = renderMarkdown(node.markdown || '', node.rel_path || '');
            body.querySelectorAll('a[data-target]').forEach(link => {
                link.addEventListener('click', event => {
                    event.preventDefault();
                    const target = nodeById.get(link.getAttribute('data-target'));
                    if (target) openReader(target);
                });
            });
            document.body.classList.add('reader-open');
            reader.classList.add('open');
            document.getElementById('sidebar').classList.add('closed');
            fitViewBox();
        }
        function closeReader() {
            document.getElementById('reader').classList.remove('open');
            document.body.classList.remove('reader-open');
            fitViewBox();
        }

        // interaction: drag after the static layout has been calculated.
        let dragging = null;
        let dragStart = null;
        nodeGroup.forEach(({g, c, node}) => {
            c.addEventListener('pointerdown', (e)=>{
                dragging = node;
                dragStart = { x: e.clientX, y: e.clientY };
                c.setPointerCapture(e.pointerId);
            });
            c.addEventListener('pointerup', (e)=>{
                if (dragging===node) {
                    const moved = dragStart ? Math.hypot(e.clientX - dragStart.x, e.clientY - dragStart.y) : 0;
                    dragging = null;
                    dragStart = null;
                    c.releasePointerCapture(e.pointerId);
                    if (moved < 5) openNodeFile(node);
                }
            });
            c.addEventListener('pointerenter', (e)=> showTooltip(node, e.clientX, e.clientY));
            c.addEventListener('pointermove', (e)=> {
                if(dragging===node){
                    const point = svg.createSVGPoint();
                    point.x = e.clientX;
                    point.y = e.clientY;
                    const local = point.matrixTransform(svg.getScreenCTM().inverse());
                    node.x = local.x;
                    node.y = local.y;
                    render();
                }
                showTooltip(node, e.clientX, e.clientY);
            });
            c.addEventListener('pointerleave', hideTooltip);
        });

        function render() {
            edgeEls.forEach(({el, data})=>{
                const s = nodeById.get(data.source);
                const t = nodeById.get(data.target);
                if(!s||!t) return;
                el.setAttribute('x1', s.x); el.setAttribute('y1', s.y);
                el.setAttribute('x2', t.x); el.setAttribute('y2', t.y);
            });

            nodeGroup.forEach(({g, c, label, node})=>{
                g.setAttribute('transform', `translate(${node.x}, ${node.y})`);
                c.setAttribute('r', String(node.r));
                label.textContent = node.displayLabel || '';
            });
        }

        function connectedComponents() {
            const neighbors = new Map(nodes.map(n => [n.id, []]));
            edges.forEach(e => {
                if (!neighbors.has(e.source) || !neighbors.has(e.target)) return;
                neighbors.get(e.source).push(e.target);
                neighbors.get(e.target).push(e.source);
            });

            const seen = new Set();
            const components = [];
            nodes.forEach(start => {
                if (seen.has(start.id)) return;
                const stack = [start.id];
                const component = [];
                seen.add(start.id);
                while (stack.length) {
                    const id = stack.pop();
                    const n = nodeById.get(id);
                    if (n) component.push(n);
                    (neighbors.get(id) || []).forEach(next => {
                        if (!seen.has(next)) {
                            seen.add(next);
                            stack.push(next);
                        }
                    });
                }
                components.push(component);
            });
            return components.sort((a, b) => b.length - a.length);
        }

        function layoutComponent(component) {
            const ids = new Set(component.map(n => n.id));
            const componentEdges = edges.filter(e => ids.has(e.source) && ids.has(e.target));
            const radius = Math.max(80, Math.sqrt(component.length) * 42);
            component.forEach((n, index) => {
                const angle = (Math.PI * 2 * index) / Math.max(1, component.length);
                const degreeBias = n.kind === 'relations' ? 0.35 : (n.kind === 'insights' ? 0.52 : 1);
                n.x = Math.cos(angle) * radius * degreeBias;
                n.y = Math.sin(angle) * radius * degreeBias;
                n.vx = 0;
                n.vy = 0;
            });

            const springLength = Math.max(64, Math.min(130, 260 / Math.sqrt(component.length || 1)));
            for (let step = 0; step < 420; step++) {
                const alpha = 1 - step / 420;
                for (let i = 0; i < component.length; i++) {
                    const a = component[i];
                    for (let j = i + 1; j < component.length; j++) {
                        const b = component[j];
                        let dx = a.x - b.x;
                        let dy = a.y - b.y;
                        let d2 = dx * dx + dy * dy + 16;
                        let d = Math.sqrt(d2);
                        let force = (900 * alpha) / d2;
                        let ux = dx / d;
                        let uy = dy / d;
                        a.vx += ux * force;
                        a.vy += uy * force;
                        b.vx -= ux * force;
                        b.vy -= uy * force;
                    }
                }

                componentEdges.forEach(e => {
                    const s = nodeById.get(e.source);
                    const t = nodeById.get(e.target);
                    if (!s || !t) return;
                    let dx = t.x - s.x;
                    let dy = t.y - s.y;
                    let d = Math.sqrt(dx * dx + dy * dy) || 1;
                    let targetLength = e.sourceKind === 'writeup' || e.targetKind === 'writeup' ? springLength : springLength * 0.75;
                    let force = (d - targetLength) * 0.035 * alpha;
                    let fx = (dx / d) * force;
                    let fy = (dy / d) * force;
                    s.vx += fx;
                    s.vy += fy;
                    t.vx -= fx;
                    t.vy -= fy;
                });

                component.forEach(n => {
                    n.vx += (0 - n.x) * 0.004 * alpha;
                    n.vy += (0 - n.y) * 0.004 * alpha;
                    n.vx *= 0.82;
                    n.vy *= 0.82;
                    n.x += n.vx;
                    n.y += n.vy;
                });
            }
        }

        function boundsFor(component) {
            return component.reduce((box, n) => ({
                minX: Math.min(box.minX, n.x - n.r),
                minY: Math.min(box.minY, n.y - n.r),
                maxX: Math.max(box.maxX, n.x + n.r),
                maxY: Math.max(box.maxY, n.y + n.r),
            }), { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity });
        }

        function packComponents() {
            const components = connectedComponents();
            components.forEach(layoutComponent);

            const boxes = components.map(component => {
                const box = boundsFor(component);
                return {
                    component,
                    width: Math.max(80, box.maxX - box.minX),
                    height: Math.max(80, box.maxY - box.minY),
                    box,
                };
            });

            const gap = 110;
            const columns = Math.max(1, Math.ceil(Math.sqrt(boxes.length)));
            const columnWidths = Array(columns).fill(0);
            boxes.forEach((item, index) => {
                const column = index % columns;
                columnWidths[column] = Math.max(columnWidths[column], item.width);
            });

            const rowHeights = [];
            boxes.forEach((item, index) => {
                const row = Math.floor(index / columns);
                rowHeights[row] = Math.max(rowHeights[row] || 0, item.height);
            });

            const columnX = [];
            let cursorX = 0;
            columnWidths.forEach((width, index) => {
                columnX[index] = cursorX;
                cursorX += width + (index === columnWidths.length - 1 ? 0 : gap);
            });

            const rowY = [];
            let cursorY = 0;
            rowHeights.forEach((height, index) => {
                rowY[index] = cursorY;
                cursorY += height + (index === rowHeights.length - 1 ? 0 : gap);
            });

            boxes.forEach((item, index) => {
                const column = index % columns;
                const row = Math.floor(index / columns);
                const offsetX = columnX[column] + (columnWidths[column] - item.width) / 2 - item.box.minX;
                const offsetY = rowY[row] + (rowHeights[row] - item.height) / 2 - item.box.minY;
                item.component.forEach(n => {
                    n.x += offsetX;
                    n.y += offsetY;
                });
            });
        }

        function fitViewBox() {
            const padding = 90;
            const box = boundsFor(nodes);
            const minX = box.minX - padding;
            const minY = box.minY - padding;
            const width = Math.max(320, box.maxX - box.minX + padding * 2);
            const height = Math.max(240, box.maxY - box.minY + padding * 2);
            svg.setAttribute('viewBox', `${minX} ${minY} ${width} ${height}`);
        }

        packComponents();
        render();
        fitViewBox();
        window.addEventListener('resize', fitViewBox);

        function makeTree(paths) {
            const root = {};
            paths.forEach(path => {
                let current = root;
                path.split('/').forEach((part, index, parts) => {
                    current[part] ||= index === parts.length - 1 ? path : {};
                    current = typeof current[part] === 'string' ? current : current[part];
                });
            });
            return root;
        }

        function renderTreeNode(name, value) {
            if (typeof value === 'string') {
                const link = document.createElement('a');
                link.className = 'tree-file';
                link.href = '#';
                link.textContent = name;
                link.title = value;
                link.addEventListener('click', event => {
                    event.preventDefault();
                    const node = nodeById.get(value);
                    if (node) openReader(node);
                });
                return link;
            }

            const details = document.createElement('details');
            details.open = name === 'insights' || name === 'relations' || name === 'writeup';
            const summary = document.createElement('summary');
            summary.textContent = name;
            details.appendChild(summary);
            const children = document.createElement('div');
            children.className = 'tree-children';
            Object.entries(value)
                .sort(([aName, aValue], [bName, bValue]) => {
                    const aFile = typeof aValue === 'string';
                    const bFile = typeof bValue === 'string';
                    if (aFile !== bFile) return aFile ? 1 : -1;
                    return aName.localeCompare(bName);
                })
                .forEach(([childName, childValue]) => children.appendChild(renderTreeNode(childName, childValue)));
            details.appendChild(children);
            return details;
        }

        const sidebar = document.getElementById('sidebar');
        const tree = document.getElementById('tree');
        const treeData = makeTree(nodes.map(n => n.rel_path).sort());
        Object.entries(treeData).forEach(([name, value]) => tree.appendChild(renderTreeNode(name, value)));
        document.getElementById('sidebar-toggle').addEventListener('click', () => sidebar.classList.toggle('closed'));
        document.getElementById('sidebar-close').addEventListener('click', () => sidebar.classList.add('closed'));
        document.getElementById('reader-close').addEventListener('click', closeReader);
    </script>
</body>
</html>'''

    return template.replace('{NODES_COUNT}', str(len(nodes))).replace('{EDGES_COUNT}', str(len(edges))).replace('__DATASET__', dataset)


def main() -> None:
    files = walk_markdown_files(ROOT_DIR)
    nodes: list[dict[str, object]] = []
    by_id: dict[str, dict[str, object]] = {}

    for file_path in files:
        rel_path = normalize_path(file_path.relative_to(ROOT_DIR))
        if not (rel_path.startswith('insights/') or rel_path.startswith('relations/') or rel_path.startswith('writeup/')):
            continue
        if file_path.name == 'README.md':
            continue

        raw_text = file_path.read_text(encoding='utf-8')
        kind = classify_node(rel_path)
        frontmatter, body = strip_frontmatter(raw_text)
        meta = parse_frontmatter(frontmatter)
        title = meta['title'] if kind == 'writeup' and isinstance(meta.get('title'), str) else get_title(body, file_path.stem)
        links = extract_links(raw_text, file_path)
        node = {
            'id': rel_path,
            'rel_path': rel_path,
            'kind': kind,
            'title': title,
            'meta': meta,
            'links': links,
            'markdown': raw_text,
        }
        nodes.append(node)
        by_id[rel_path] = node

    grouped = group_by_kind(nodes)
    ordered_kinds = ('insights', 'relations', 'writeup')
    total_height = max(1080, max(len(grouped[kind]) for kind in ordered_kinds) * 140 + 220)
    column_x = [220, 960, 1700]
    y_positions: dict[str, float] = {}

    for kind in ordered_kinds:
      sorted_nodes = sorted(grouped[kind], key=lambda item: str(item['title']).casefold())
      step = total_height / max(1, len(sorted_nodes) + 1)
      for index, node in enumerate(sorted_nodes):
          y = 140 + step * (index + 1)
          y_positions[str(node['id'])] = y
          node['y'] = y

    edges: list[dict[str, object]] = []
    seen: set[str] = set()

    for node in nodes:
        for target in node['links']:
            target_node = by_id.get(target)
            if not target_node or target_node['id'] == node['id']:
                continue

            key = f"{node['id']} -> {target_node['id']}"
            if key in seen:
                continue

            seen.add(key)
            edges.append(
                {
                    'source': node['id'],
                    'target': target_node['id'],
                    'sourceKind': node['kind'],
                    'targetKind': target_node['kind'],
                    'sourceY': y_positions[str(node['id'])],
                    'targetY': y_positions[str(target_node['id'])],
                    'weight': 0.55 if node['kind'] == 'relations' or target_node['kind'] == 'relations' else 0.3,
                }
            )

    html_text = build_html(nodes, edges)
    OUTPUT_FILE.write_text(html_text, encoding='utf-8')


if __name__ == '__main__':
    main()
