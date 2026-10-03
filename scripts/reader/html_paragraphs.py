#!/usr/bin/env python3
"""Split an HTML edition (Project Gutenberg style) into paragraphs, headings and footnotes.

    html_paragraphs.py <source.html> <spec.py> <doc.json>

Reads the spec's META:

- html_start / html_end: regexes; only the markup between them is read;
- html_heading: regex for a heading tag inside that region (default <h2>);
- html_note_p / html_note_ref: regexes for a footnote paragraph and for the
  reference to it, each with the note number as group 1;
- word_fixes: plain replacements applied to every paragraph.

Blockquotes (verse, long quotations) become paragraphs of their own, marked
kind "quote", with their line breaks as [[br]]. Footnotes are collected from the whole file, so a note called in the title is
not lost. "--" becomes an em dash, italics survive as [[i]]…[[/i]], and a note
reference becomes [[note:N]]; build_reader.py turns both back into markup.
HTML editions have no pages, so the map's locators carry paragraph numbers only.
"""
import html, json, re, runpy, sys

def clean(fragment, note_ref, fixes, lines=False):
    t = re.sub(note_ref, lambda m: f'[[note:{m.group(1)}]]', fragment, flags=re.S)
    t = re.sub(r'<i>(.*?)</i>', r'[[i]]\1[[/i]]', t, flags=re.S)
    t = re.sub(r'<br\s*/?>|</p>\s*<p[^>]*>', ' [[br]] ' if lines else ' ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t).replace('--', '—')
    t = re.sub(r'[ \t\r\n]+', ' ', t)   # not \s: keep the no-break spaces that indent verse
    t = re.sub(r' ?\[\[br\]\] ?', '[[br]]', t).strip(' ')
    t = re.sub(r'^(\[\[br\]\])+|(\[\[br\]\])+$', '', t)
    for a, b in fixes.items(): t = t.replace(a, b)
    return t

def main(src, spec_path, out):
    m = runpy.run_path(spec_path)['META']
    raw = open(src, 'rb').read()
    enc = re.search(rb'charset=([\w-]+)', raw)
    doc = raw.decode(enc.group(1).decode() if enc else 'utf-8', errors='replace')
    note_p = m.get('html_note_p', r'<p id="footnote(\d+)">(.*?)</p>')
    note_ref = m.get('html_note_ref', r'<a id="foottag(\d+)"[^>]*>.*?</a>')
    fixes = m.get('word_fixes', {})
    notes = {}
    for k, body in re.findall(note_p, doc, re.S):
        body = re.sub(r'^\s*<a[^>]*>.*?</a>\s*', '', body, flags=re.S)   # the back-link "[1]"
        notes[k] = {'page': None, 'text': clean(body, note_ref, fixes)}
    start = re.search(m['html_start'], doc).start()
    end = re.search(m['html_end'], doc[start:]).start() + start
    region = re.sub(note_p, '', doc[start:end], flags=re.S)
    heading = m.get('html_heading', r'<h2[^>]*>(.*?)</h2>')
    blocks = []
    for tok in re.finditer(heading + r'|<blockquote[^>]*>(.*?)</blockquote>|<p[^>]*>(.*?)</p>', region, re.S):
        if tok.group(2) is not None:   # verse and long quotations keep their lines
            text = clean(tok.group(2), note_ref, fixes, lines=True)
            if text: blocks.append({'type': 'p', 'kind': 'quote', 'text': text, 'page': None})
        elif tok.group(1) is not None:
            h = clean(tok.group(1), note_ref, fixes)
            if h.isupper():   # CHAPTER II -> Chapter II, keeping roman numerals
                h = ' '.join(w if re.fullmatch(r'[IVXLC]+', w) else w.capitalize() for w in h.split())
            blocks.append({'type': 'h1', 'text': h, 'page': None})
        else:
            text = clean(tok.group(3), note_ref, fixes)
            if text: blocks.append({'type': 'p', 'text': text, 'page': None})
    json.dump({'blocks': blocks, 'notes': notes}, open(out, 'w'), ensure_ascii=False, indent=1)
    n = 0
    for b in blocks:
        if b['type'] == 'p':
            n += 1; print(f"[{n}]{' Q' if b.get('kind') else ''} {len(b['text'].split())}w {b['text'][:90]}")
        else:
            print(f"=== {b['text']}")
    print(f"{n} paragraphs, {len(notes)} footnotes -> {out}")

if __name__ == '__main__':
    if len(sys.argv) != 4: sys.exit(__doc__)
    main(*sys.argv[1:])
