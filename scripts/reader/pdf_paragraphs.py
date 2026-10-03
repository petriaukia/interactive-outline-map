#!/usr/bin/env python3
"""Split a text PDF into numbered paragraphs, headings and footnotes.

    pdf_paragraphs.py <source.pdf> <spec.py> <doc.json>

Needs `pdftotext` (poppler) on the PATH. The layout mode keeps the indents the
splitter relies on:

- a body line indented 3-5 spaces, or starting "a. " .. "c. ", opens a paragraph;
- a bare number at the left margin opens a footnote, and its indented lines,
  plus any indented line longer than body text, belong to the footnote;
- page numbers (a lone number far to the right) are dropped;
- headings are matched exactly against the spec's heads_h1 / heads_h2.

Line-end hyphens are resolved against /usr/share/dict/words: "automa-tion"
joins, "old-fashioned" keeps its hyphen. What the dictionary gets wrong goes in
the spec's word_fixes. Print the result and read it before you write an outline:
the splitter is a heuristic, and a merged or split paragraph moves every number.
"""
import json, re, runpy, subprocess, sys

def main(pdf, spec_path, out):
    spec = runpy.run_path(spec_path)['META']
    text = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, check=True).stdout
    try:
        words = {w.strip().lower() for w in open('/usr/share/dict/words')}
    except OSError:
        words = set()
    skip = [re.compile(p) for p in spec.get('skip_lines', [])]
    h1, h2 = set(spec.get('heads_h1', [])), set(spec.get('heads_h2', []))

    blocks, notes = [], {}
    cur = curnote = None

    def flush():
        nonlocal cur
        if cur: blocks.append(cur); cur = None

    for page_no, page in enumerate(text.split('\f'), 1):
        infoot = False
        for line in page.split('\n'):
            s = line.strip()
            if not s or any(rx.search(s) for rx in skip):
                continue
            ind = len(line) - len(line.lstrip())
            if re.fullmatch(r'\d+', s) and ind > 20:
                continue                                   # page number
            if re.fullmatch(r'\d+', s) and ind == 0:
                infoot, curnote = True, s
                notes[s] = {'page': page_no, 'lines': []}
                continue
            if curnote and ((infoot and ind >= 3) or (3 <= ind <= 6 and len(line) > 84)):
                notes[curnote]['lines'].append(s); infoot = True
                continue
            infoot = False
            if s in h1 or s in h2:
                flush()
                blocks.append({'type': 'h1' if s in h1 else 'h2', 'text': (s.title() if s.isupper() else re.sub(r'\d+$', '', s)),
                               'raw': s, 'page': page_no})
                continue
            if 3 <= ind <= 5 or re.match(r'^[a-c]\. ', line):
                flush(); cur = {'type': 'p', 'lines': [s], 'page': page_no}
                continue
            if cur is None: cur = {'type': 'p', 'lines': [s], 'page': page_no}
            else: cur['lines'].append(s)
    flush()

    def join(lines):
        out = lines[0]
        for l in lines[1:]:
            if out.endswith('-') and l[:1].islower():
                a, b = re.findall(r'(\w+)-$', out), re.findall(r'^(\w+)', l)
                w = ((a[0] if a else '') + (b[0] if b else '')).lower()
                if w in words or w.rstrip('s') in words or w[:-2] in words or w[:-1] in words or not a:
                    out = out[:-1] + l
                elif a[0].lower() in words and b[0].lower() in words and len(b[0]) > 3 and len(a[0]) > 2:
                    out = out + l
                else:
                    out = out[:-1] + l
            else:
                out = out + ' ' + l
        return out

    fixes = spec.get('word_fixes', {})
    def fix(t):
        for a, b in fixes.items(): t = t.replace(a, b)
        return t
    for b in blocks:
        if b['type'] == 'p': b['text'] = fix(join(b.pop('lines')))
    for k in notes: notes[k]['text'] = fix(join(notes[k].pop('lines')))
    json.dump({'blocks': blocks, 'notes': notes}, open(out, 'w'), ensure_ascii=False, indent=1)

    n = 0
    for b in blocks:
        if b['type'] == 'p':
            n += 1; print(f"[{n}] s.{b['page']} {b['text'][:90]}")
        else:
            print(f"=== {b['text']}")
    print(f"{n} paragraphs, {len(notes)} footnotes -> {out}")

if __name__ == '__main__':
    if len(sys.argv) != 4: sys.exit(__doc__)
    main(*sys.argv[1:])
