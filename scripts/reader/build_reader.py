#!/usr/bin/env python3
"""Build a reader map: the outline map with the full source text beside it.

    build_reader.py <doc.json> <spec.py> <out.html> [--outline-only]

doc.json comes from pdf_paragraphs.py or html_paragraphs.py. The spec holds
META, ROOT and BRANCHES (see examples/):

    ROOT     = (title, note, (from, to))
    BRANCHES = [(branch_id, label, colour, note, (from, to), leaves), ...]
    leaf     = (kind, text, (from, to), twigs)   kind: "" | highlight | source | question | own
    twig     = (text, (from, to))

Ranges are paragraph numbers. The build refuses to write unless every
paragraph belongs to exactly one leaf, each branch's leaves fill its range,
and each leaf's twigs fill the leaf: "the map covers the whole text" is
checked, not hoped for. Every leaf and twig then opens the text at its
paragraphs, and scrolling the text marks the leaf it is in.

--outline-only builds the same map without the text, for a source that may
not be redistributed. Locators then name the source's own section headings,
which a reader with any edition can find, instead of paragraph numbers.

The page starts from assets/template.html, so it keeps every interaction the
skill promises; reader.css and reader.js beside this script add the pane.
"""
import html, json, re, runpy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent.parent / 'assets' / 'template.html'
E = html.escape

UI = {
    'en': {
        'controls': 'Map controls',
        'hint': '<b>Click a card</b> to open the text at that point · <b>a heading</b> folds its branch · <b>drag</b> the dots to reorder',
        'hint_outline': '<b>Click</b> a heading to fold it · <b>drag</b> the dots or press <b>Alt</b>+arrows to reorder',
        'read_all': 'Full text', 'open_all': 'Open all', 'hide_all': 'Hide all',
        'restore': 'Restore order', 'copy': 'Copy as outline',
        'heading_hint': 'Click to hide or restore · Drag the node, or press Alt with the arrow keys, to reorder',
        'node_hint': 'Drag to reorder', 'hidden': '{n} hidden', 'moved': 'Branch {n} of {total}',
        'copied': 'Copied', 'copy_failed': 'Press ⌘C', 'full_text': 'Full text',
        'prev': 'Previous card', 'next': 'Next card', 'close': 'Close', 'close_title': 'Close (Esc)',
        'page': 'p.',
        'flags': ('key idea', 'from the source', 'open question', 'your words'),
    },
    'fi': {
        'controls': 'Rungon ohjaimet',
        'hint': '<b>Klikkaa korttia</b>: teksti aukeaa sen kohdalta · <b>otsikko</b> taittaa haaran · <b>raahaa</b> pisteistä',
        'hint_outline': '<b>Klikkaa</b> otsikkoa: haara taittuu · <b>raahaa</b> pisteistä tai paina <b>Alt</b> ja nuolta: järjestys',
        'read_all': 'Koko teksti', 'open_all': 'Avaa kaikki', 'hide_all': 'Kätke kaikki',
        'restore': 'Palauta järjestys', 'copy': 'Kopioi runkona',
        'heading_hint': 'Klikkaa: kätke tai palauta haara · raahaa pisteistä tai paina Alt ja nuolinäppäintä: siirrä',
        'node_hint': 'Raahaa siirtääksesi', 'hidden': '{n} kätkettyä', 'moved': 'Haara {n}/{total}',
        'copied': 'Kopioitu', 'copy_failed': 'Paina ⌘C', 'full_text': 'Koko teksti',
        'prev': 'Edellinen kortti', 'next': 'Seuraava kortti', 'close': 'Sulje', 'close_title': 'Sulje (Esc)',
        'page': 's.',
        'flags': ('ydinlause', 'lähteestä', 'avoin kysymys', 'omin sanoin'),
    },
}


def check_coverage(branches, total):
    seen = []
    for bid, _, _, _, (lo, hi), leaves in branches:
        got = []
        for _, text, (a, z), twigs in leaves:
            got += range(a, z + 1)
            if twigs:
                tw = [n for _, (x, y) in twigs for n in range(x, y + 1)]
                if tw != list(range(a, z + 1)):
                    sys.exit(f'twigs of "{text[:40]}" do not fill ¶{a}–{z}: {tw}')
        if got != list(range(lo, hi + 1)):
            sys.exit(f'leaves of branch {bid} do not fill ¶{lo}–{hi}')
        seen += got
    if seen != list(range(1, total + 1)):
        missing = sorted(set(range(1, total + 1)) - set(seen))
        sys.exit(f'the map does not cover the text exactly once; missing {missing[:20]}')


def inline(text, sup):
    """Escape a paragraph and turn the splitters' tokens back into markup."""
    t = E(text)
    t = t.replace('[[i]]', '<i>').replace('[[/i]]', '</i>').replace('[[br]]', '<br>')
    t = re.sub(r'\[\[note:(\d+)\]\]', lambda m: sup(m.group(1)), t)
    return re.sub('\x00(\\d+)\x01', lambda m: sup(m.group(1)), t)


def main(doc_path, spec_path, out_path, outline_only=False):
    d = json.load(open(doc_path))
    spec = runpy.run_path(spec_path)
    META, ROOT, BRANCHES = spec['META'], spec['ROOT'], spec['BRANCHES']
    base = META.get('ui', 'en')
    ui = dict(UI[base]) if isinstance(base, str) else {**UI['en'], **base}
    tl = META.get('text_lang', META.get('lang', 'en'))
    notes = d['notes']

    # paragraphs, the headings in front of them, and where each note is called
    paras, heads, pending, note_at = [], {}, [], {}
    if META.get('title_note'): note_at[META['title_note']] = 0
    section, sections = '', {}
    for b in d['blocks']:
        if b['type'] in ('h1', 'h2'):
            pending.append(b)
            section = b['text']
            continue
        paras.append({'n': len(paras) + 1, 'page': b.get('page'), 'kind': b.get('kind', ''),
                      'text': b['text'], 'notes': []})
        sections[len(paras)] = section
        if pending: heads[len(paras)] = pending; pending = []
    for p in paras:   # notes the splitter already placed
        for k in re.findall(r'\[\[note:(\d+)\]\]', p['text']):
            note_at.setdefault(k, p['n'])
    for k in sorted(notes, key=int):
        if k in note_at: continue
        for pn, hs in heads.items():
            if any(re.search(r'\D' + k + '$', h.get('raw', '')) for h in hs):
                note_at[k] = pn
        if k in note_at: continue
        rx = re.compile(r'(?<=[a-z.?”,;:)])' + k + r'(?=\s|$)')
        start = max(list(note_at.values()) + [1])
        for p in paras[start - 1:]:
            if rx.search(p['text']):
                p['text'] = rx.sub('\x00' + k + '\x01', p['text'], count=1)
                note_at[k] = p['n']; break
        if k not in note_at:
            print(f'warning: footnote {k} has no marker; shown after its page', file=sys.stderr)
            note_at[k] = next((p['n'] for p in reversed(paras) if (p['page'] or 0) <= (notes[k].get('page') or 0)), 1)
    for k, pn in note_at.items():
        if pn: paras[pn - 1]['notes'].append(k)

    check_coverage(BRANCHES, len(paras))
    page_of = {p['n']: p['page'] for p in paras}
    pg = ui['page']

    def pages(r):
        a, z = page_of[r[0]], page_of[r[1]]
        if a is None: return ''
        return f' <span>· {pg} {a}</span>' if a == z else f' <span>· {pg} {a}–{z}</span>'

    def loc(r):
        if outline_only:   # name the source's own sections, which any edition has
            names = []
            for n in range(r[0], r[1] + 1):
                s = sections.get(n) or META.get('first_section', '')
                if s and s not in names: names.append(s)
            label = names[0] if len(names) == 1 else f'{names[0]} – {names[-1]}' if names else ''
            return f'<span class="loc">{E(label)}</span>' if label else ''
        lab = f'¶{r[0]}' if r[0] == r[1] else f'¶{r[0]}–{r[1]}'
        return f'<a class="loc" href="#p{r[0]}" data-from="{r[0]}" data-to="{r[1]}">{lab}{pages(r)}</a>'

    def sup(k):
        return f'<sup class="nref"><a href="#note-{k}" id="nref-{k}">{k}</a></sup>'

    def rng(r):
        return '' if outline_only else f' data-from="{r[0]}" data-to="{r[1]}"'

    owner, out = {}, []
    for bi, (bid, label, colour, note, br, leaves) in enumerate(BRANCHES):
        out.append(f'    <article class="branch" data-branch-id="{bid}" style="--bc:{colour}">')
        out.append(f'      <div class="bhead"><span class="grip" aria-hidden="true"></span><span class="dot">{bi+1}</span>'
                   f'<span class="label">{E(label)}</span><span class="state" aria-hidden="true"></span></div>')
        out.append(f'      <p class="bnote">{E(note)} {loc(br)}</p>')
        out.append('      <div class="leaves">')
        for li, (kind, text, r, twigs) in enumerate(leaves):
            for p in range(r[0], r[1] + 1): owner[p] = bi
            tw = ('<div class="twig">' + ''.join(f'<div{rng((x, y))}>{E(t)} {loc((x, y))}</div>'
                                                 for t, (x, y) in twigs) + '</div>') if twigs else ''
            out.append(f'        <div class="leaf{" " + kind if kind else ""}"{rng(r)} '
                       f'id="leaf-{bid}-{li+1}"><span class="ltext">{E(text)}</span> {loc(r)}{tw}</div>')
        out.append('      </div>\n    </article>\n')

    rd = [f'<header class="rd-title" lang="{tl}">']
    tn = META.get('title_note')
    rd.append(META.get('reader_title_html', '<h2>{h1}{note1}</h2>').format(
        h1=E(META.get('h1', '')), note1=sup(tn) if tn else ''))
    if tn: rd.append(f'<p class="fn" id="note-{tn}"><b>{tn}</b> {inline(notes[tn]["text"], sup)}</p>')
    rd.append('</header>')
    last = None
    for p in paras:
        for h in heads.get(p['n'], []):
            k = next((k for k, pn in note_at.items() if pn == p['n'] and re.search(r'\D' + k + '$', h.get('raw', ''))), None)
            tag = 'h3' if h['type'] == 'h1' else 'h4'
            rd.append(f'<{tag} lang="{tl}">{E(h["text"])}{" " + sup(k) if k else ""}</{tag}>')
        marker = ''
        if p['page'] is not None and p['page'] != last:
            marker = f'<span class="pg">{pg} {p["page"]}</span>'; last = p['page']
        cls = 'para' + (' ' + p['kind'] if p['kind'] else '')
        rd.append(f'<p class="{cls}" id="p{p["n"]}" data-n="{p["n"]}" style="--bc:{BRANCHES[owner[p["n"]]][2]}" '
                  f'lang="{tl}"><a class="pn" href="#p{p["n"]}">¶{p["n"]}</a>{marker}{inline(p["text"], sup)}</p>')
        for k in p['notes']:
            rd.append(f'<p class="fn" id="note-{k}" lang="{tl}"><b>{k}</b> {inline(notes[k]["text"], sup)}</p>')

    t = TEMPLATE.read_text(encoding='utf-8')

    def rep(old, new):
        nonlocal t
        if old not in t: sys.exit(f'template changed; cannot find: {old[:60]}')
        t = t.replace(old, new, 1)

    css = (HERE / 'reader.css').read_text(encoding='utf-8')
    f = ui['flags']
    css = re.sub(r'--flag-key-idea:"[^"]*";--flag-source:"[^"]*";--flag-question:"[^"]*";--flag-own:"[^"]*"',
                 f'--flag-key-idea:"{f[0]}";--flag-source:"{f[1]}";--flag-question:"{f[2]}";--flag-own:"{f[3]}"', css)
    lang = META.get('lang', 'en')
    a = lambda s: E(s, quote=True)
    rep('<html lang="en">', f'<html lang="{lang}">')
    head_script = '' if outline_only else '\n<script>document.documentElement.classList.add("js")</script>'
    rep('<title>Interactive outline map</title>', f'<title>{E(META["title"])}</title>{head_script}')
    rep('</style>', css + '</style>')
    rep('<body data-map-key="replace-with-a-stable-map-key">',
        f'<body data-map-key="{a(META["map_key"])}"\n  data-heading-hint="{a(ui["heading_hint"])}"\n'
        f'  data-node-hint="{a(ui["node_hint"])}" data-hidden-label="{a(ui["hidden"])}" data-move-status="{a(ui["moved"])}"\n'
        f'  data-copied-label="{a(ui["copied"])}" data-copy-failed-label="{a(ui["copy_failed"])}" data-full-text="{a(ui["full_text"])}">')
    h1_lang = f' lang="{tl}"' if tl != lang else ''
    rep('<h1>Replace the map title</h1>', f'<h1{h1_lang}>{E(META["h1"])}</h1>')
    src = META.get('source_html', '').format(paras=len(paras), pdf=E(META.get('pdf_href', '')))
    rep('<p class="source">For a map of a document, its source and a link to it. Delete this line otherwise.</p>',
        f'<p class="source">{src}</p>' if src else '')
    rep('aria-label="Map controls"', f'aria-label="{a(ui["controls"])}"')
    hint = ui['hint_outline'] if outline_only else ui['hint']
    t = re.sub(r'<div class="hint">.*?</div>', lambda m: f'<div class="hint">{hint}</div>', t, count=1, flags=re.S)
    read_all = '' if outline_only else f'<button type="button" id="read-all">{E(ui["read_all"])}</button>\n        '
    rep('<button type="button" id="expand-all">Open all</button>',
        f'{read_all}<button type="button" id="expand-all">{E(ui["open_all"])}</button>')
    rep('>Hide all<', f'>{E(ui["hide_all"])}<')
    rep('>Restore order<', f'>{E(ui["restore"])}<')
    rep('>Copy as outline<', f'>{E(ui["copy"])}<')
    root = f'<h2>{E(ROOT[0])}</h2>\n    <p>{E(ROOT[1])} {loc(ROOT[2])}</p>'
    t = re.sub(r'<section class="root">.*?</section>', lambda m: f'<section class="root">\n    {root}\n  </section>', t, count=1, flags=re.S)
    t = re.sub(r'<section class="trunk">.*?</section>', lambda m: '<section class="trunk">\n' + '\n'.join(out) + '  </section>', t, count=1, flags=re.S)
    t = re.sub(r'<div class="legend">.*?</div>\n</main>', '<div class="legend"></div>\n</main>', t, count=1, flags=re.S)
    if not outline_only:
        reader = (f'\n<aside class="reader" id="full-text" aria-label="{a(ui["full_text"])}">\n  <div class="rd-bar">\n'
                  f'    <div class="rd-crumb"><span class="dot">·</span><span class="t">{E(ui["full_text"])}</span><span class="r"></span></div>\n'
                  f'    <button type="button" class="rd-prev" title="{a(ui["prev"])}" aria-label="{a(ui["prev"])}">↑</button>\n'
                  f'    <button type="button" class="rd-next" title="{a(ui["next"])}" aria-label="{a(ui["next"])}">↓</button>\n'
                  f'    <button type="button" class="rd-close" title="{a(ui["close_title"])}">{E(ui["close"])}</button>\n'
                  '  </div>\n  <div class="rd-body">\n' + '\n'.join(rd) + '\n  </div>\n</aside>\n')
        rep('</main>\n', '</main>\n' + reader)
        rep("    copyFailed: body.dataset.copyFailedLabel || 'Press ⌘C'",
            "    copyFailed: body.dataset.copyFailedLabel || 'Press ⌘C',\n    fullText: body.dataset.fullText || 'Full text'")
        rep('  sizeLeafGuides();\n})();', '  sizeLeafGuides();\n' + (HERE / 'reader.js').read_text(encoding='utf-8') + '})();')
    Path(out_path).write_text(t, encoding='utf-8')
    leaves = sum(len(b[5]) for b in BRANCHES)
    mode = 'outline only, no source text' if outline_only else 'with the full text'
    print(f'{out_path}: {len(paras)} paragraphs, {len(notes)} footnotes, {len(BRANCHES)} branches, '
          f'{leaves} leaves; coverage exact; {mode}')


if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    if len(args) != 3: sys.exit(__doc__)
    main(*args, outline_only='--outline-only' in sys.argv)
