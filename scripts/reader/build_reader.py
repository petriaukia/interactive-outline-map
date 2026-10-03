#!/usr/bin/env python3
"""Build a reader map: the outline map with the full source text beside it.

    build_reader.py <doc.json> <spec.py> <out.html>

doc.json comes from pdf_paragraphs.py. The spec holds META, ROOT and BRANCHES
(see examples/simon-1960.py):

    ROOT     = (title, note, (from, to))
    BRANCHES = [(branch_id, label, colour, note, (from, to), leaves), ...]
    leaf     = (kind, text, (from, to), twigs)   kind: "" | highlight | source | question | own
    twig     = (text, (from, to))

Ranges are paragraph numbers. The build refuses to write unless every
paragraph belongs to exactly one leaf, each branch's leaves fill its range,
and each leaf's twigs fill the leaf: "the map covers the whole text" is
checked, not hoped for. Every leaf and twig then opens the text at its
paragraphs, and scrolling the text marks the leaf it is in.

The page starts from assets/template.html, so it keeps every interaction the
skill promises; reader.css and reader.js beside this script add the pane.
"""
import html, json, re, runpy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent.parent / 'assets' / 'template.html'
E = html.escape

UI_FI = {
    'controls': 'Rungon ohjaimet',
    'hint': '<b>Klikkaa korttia</b>: teksti aukeaa sen kohdalta · <b>otsikko</b> taittaa haaran · <b>raahaa</b> pisteistä',
    'read_all': 'Koko teksti', 'open_all': 'Avaa kaikki', 'hide_all': 'Kätke kaikki',
    'restore': 'Palauta järjestys', 'copy': 'Kopioi runkona',
    'heading_hint': 'Klikkaa: kätke tai palauta haara · raahaa pisteistä tai paina Alt ja nuolinäppäintä: siirrä',
    'node_hint': 'Raahaa siirtääksesi', 'hidden': '{n} kätkettyä', 'moved': 'Haara {n}/{total}',
    'copied': 'Kopioitu', 'copy_failed': 'Paina ⌘C', 'full_text': 'Koko teksti',
    'prev': 'Edellinen kortti', 'next': 'Seuraava kortti', 'close': 'Sulje', 'close_title': 'Sulje (Esc)',
    'page': 's.',
    'flags': ('ydinlause', 'lähteestä', 'avoin kysymys', 'omin sanoin'),
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

def main(doc_path, spec_path, out_path):
    d = json.load(open(doc_path))
    spec = runpy.run_path(spec_path)
    META, ROOT, BRANCHES = spec['META'], spec['ROOT'], spec['BRANCHES']
    ui = {**UI_FI, **META.get('ui', {})}
    tl = META.get('text_lang', META.get('lang', 'en'))
    notes = d['notes']

    # paragraphs, the headings in front of them, and where each note is called
    paras, heads, pending, note_at = [], {}, [], {}
    if META.get('title_note'): note_at[META['title_note']] = 0
    for b in d['blocks']:
        if b['type'] in ('h1', 'h2'):
            pending.append(b); continue
        paras.append({'n': len(paras) + 1, 'page': b['page'], 'text': b['text'], 'notes': []})
        if pending: heads[len(paras)] = pending; pending = []
    for k in sorted(notes, key=int):
        if k in note_at: continue
        for pn, hs in heads.items():
            if any(h.get('raw', '').endswith(k) and re.search(r'\D' + k + '$', h.get('raw', '')) for h in hs):
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
            note_at[k] = next((p['n'] for p in reversed(paras) if p['page'] <= notes[k]['page']), 1)
    for k, pn in note_at.items():
        if pn: paras[pn - 1]['notes'].append(k)

    check_coverage(BRANCHES, len(paras))
    page_of = {p['n']: p['page'] for p in paras}
    pg = ui['page']
    def pages(r):
        a, z = page_of[r[0]], page_of[r[1]]
        return f'{pg} {a}' if a == z else f'{pg} {a}–{z}'
    def loc(r):
        lab = f'¶{r[0]}' if r[0] == r[1] else f'¶{r[0]}–{r[1]}'
        return f'<a class="loc" href="#p{r[0]}" data-from="{r[0]}" data-to="{r[1]}">{lab} <span>· {pages(r)}</span></a>'
    def sup(k):
        return f'<sup class="nref"><a href="#note-{k}" id="nref-{k}">{k}</a></sup>'

    owner, out = {}, []
    for bi, (bid, label, colour, note, br, leaves) in enumerate(BRANCHES):
        out.append(f'    <article class="branch" data-branch-id="{bid}" style="--bc:{colour}">')
        out.append(f'      <div class="bhead"><span class="grip" aria-hidden="true"></span><span class="dot">{bi+1}</span>'
                   f'<span class="label">{E(label)}</span><span class="state" aria-hidden="true"></span></div>')
        out.append(f'      <p class="bnote">{E(note)} {loc(br)}</p>')
        out.append('      <div class="leaves">')
        for li, (kind, text, r, twigs) in enumerate(leaves):
            for p in range(r[0], r[1] + 1): owner[p] = bi
            tw = ('<div class="twig">' + ''.join(f'<div data-from="{x}" data-to="{y}">{E(t)} {loc((x, y))}</div>'
                                                 for t, (x, y) in twigs) + '</div>') if twigs else ''
            out.append(f'        <div class="leaf{" " + kind if kind else ""}" data-from="{r[0]}" data-to="{r[1]}" '
                       f'id="leaf-{bid}-{li+1}"><span class="ltext">{E(text)}</span> {loc(r)}{tw}</div>')
        out.append('      </div>\n    </article>\n')

    rd = [f'<header class="rd-title" lang="{tl}">']
    tn = META.get('title_note')
    rd.append(META.get('reader_title_html', '<h2>{h1}{note1}</h2>').format(
        h1=E(META.get('h1', '')), note1=sup(tn) if tn else ''))
    if tn: rd.append(f'<p class="fn" id="note-{tn}"><b>{tn}</b> {E(notes[tn]["text"])}</p>')
    rd.append('</header>')
    last = 0
    for p in paras:
        for h in heads.get(p['n'], []):
            k = next((k for k, pn in note_at.items() if pn == p['n'] and re.search(r'\D' + k + '$', h.get('raw', ''))), None)
            tag = 'h3' if h['type'] == 'h1' else 'h4'
            rd.append(f'<{tag} lang="{tl}">{E(h["text"])}{" " + sup(k) if k else ""}</{tag}>')
        marker = ''
        if p['page'] != last:
            marker = f'<span class="pg">{pg} {p["page"]}</span>'; last = p['page']
        body = re.sub('\x00(\\d+)\x01', lambda m: sup(m.group(1)), E(p['text']))
        rd.append(f'<p class="para" id="p{p["n"]}" data-n="{p["n"]}" style="--bc:{BRANCHES[owner[p["n"]]][2]}" '
                  f'lang="{tl}"><a class="pn" href="#p{p["n"]}">¶{p["n"]}</a>{marker}{body}</p>')
        for k in p['notes']:
            rd.append(f'<p class="fn" id="note-{k}" lang="{tl}"><b>{k}</b> {E(notes[k]["text"])}</p>')

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
    rep('<html lang="en">', f'<html lang="{lang}">')
    rep('<title>Interactive outline map</title>',
        f'<title>{E(META["title"])}</title>\n<script>document.documentElement.classList.add("js")</script>')
    rep('</style>', css + '</style>')
    a = lambda s: E(s, quote=True)
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
    t = re.sub(r'<div class="hint">.*?</div>', lambda m: f'<div class="hint">{ui["hint"]}</div>', t, count=1, flags=re.S)
    rep('<button type="button" id="expand-all">Open all</button>',
        f'<button type="button" id="read-all">{E(ui["read_all"])}</button>\n        '
        f'<button type="button" id="expand-all">{E(ui["open_all"])}</button>')
    rep('>Hide all<', f'>{E(ui["hide_all"])}<')
    rep('>Restore order<', f'>{E(ui["restore"])}<')
    rep('>Copy as outline<', f'>{E(ui["copy"])}<')
    root = f'<h2>{E(ROOT[0])}</h2>\n    <p>{E(ROOT[1])} {loc(ROOT[2])}</p>'
    t = re.sub(r'<section class="root">.*?</section>', lambda m: f'<section class="root">\n    {root}\n  </section>', t, count=1, flags=re.S)
    t = re.sub(r'<section class="trunk">.*?</section>', lambda m: '<section class="trunk">\n' + '\n'.join(out) + '  </section>', t, count=1, flags=re.S)
    t = re.sub(r'<div class="legend">.*?</div>\n</main>', '<div class="legend"></div>\n</main>', t, count=1, flags=re.S)
    reader = (f'\n<aside class="reader" id="teksti" aria-label="{a(ui["full_text"])}">\n  <div class="rd-bar">\n'
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
    print(f'{out_path}: {len(paras)} paragraphs, {len(notes)} footnotes, {len(BRANCHES)} branches, {leaves} leaves; coverage exact')

if __name__ == '__main__':
    if len(sys.argv) != 4: sys.exit(__doc__)
    main(*sys.argv[1:])
