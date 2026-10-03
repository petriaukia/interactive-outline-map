
  /* ---- Reading pane -------------------------------------------------------
     Every leaf and twig names a paragraph range of the full text. Clicking it
     opens the text at the first paragraph and tints the range; scrolling the
     text marks the leaf that covers the paragraph on screen, so the map and
     the text always point at each other. */
  const reader = document.querySelector('.reader');
  const rbody = reader.querySelector('.rd-body');
  const crumb = reader.querySelector('.rd-crumb');
  const paras = [...rbody.querySelectorAll('.para')];
  const paraOf = n => document.getElementById('p' + n);
  const leaves = () => [...trunk.querySelectorAll('.leaves > .leaf')];
  const leafFor = para => {
    const n = +para.dataset.n;
    return leaves().find(leaf => +leaf.dataset.from <= n && n <= +leaf.dataset.to);
  };
  const twigFor = (leaf, n) => leaf && [...leaf.querySelectorAll('.twig div[data-from]')]
    .find(twig => +twig.dataset.from <= n && n <= +twig.dataset.to);
  const rangeLabel = (a, b) => a === b ? '¶' + a : '¶' + a + '–' + b;
  let current = null;   /* the leaf the reader is on */
  let quietUntil = 0;
  let range = null;

  function setCrumb(leaf, from, to) {
    const branch = leaf && leaf.closest('.branch');
    crumb.style.setProperty('--bc', branch ? branch.style.getPropertyValue('--bc') : 'var(--gray)');
    crumb.querySelector('.dot').textContent = branch ? branch.querySelector('.dot').textContent : '·';
    crumb.querySelector('.t').textContent = branch ? labelOf(branch) : text.fullText;
    crumb.querySelector('.r').textContent = from ? rangeLabel(from, to) : '';
  }

  function markReading(leaf, n) {
    trunk.querySelectorAll('.is-reading').forEach(node => node.classList.remove('is-reading'));
    if (!leaf) return;
    leaf.classList.add('is-reading');
    const twig = twigFor(leaf, n);
    if (twig) twig.classList.add('is-reading');
  }

  function openAt(from, to, opts = {}) {
    const wasOpen = body.classList.contains('reading');
    body.classList.add('reading');
    reader.setAttribute('aria-hidden', 'false');
    paras.forEach(p => p.classList.toggle('on', !!from && +p.dataset.n >= from && +p.dataset.n <= to));
    range = from ? [from, to] : null;
    const target = from ? paraOf(from) : null;
    const leaf = target ? leafFor(target) : null;
    current = leaf;
    setCrumb(leaf, from, to);
    markReading(leaf, from);
    requestAnimationFrame(() => {
      const top = target ? rbody.scrollTop + target.getBoundingClientRect().top - rbody.getBoundingClientRect().top - 12 : 0;
      const smooth = wasOpen && !reducedMotion;
      /* While the pane glides to the target, the paragraphs it passes must
         not take over the crumb and the map. */
      quietUntil = Date.now() + (smooth ? 2000 : 150);
      rbody.addEventListener('scrollend', () => { quietUntil = 0; }, { once: true });
      rbody.scrollTo({ top: Math.max(0, top), behavior: smooth ? 'smooth' : 'auto' });
    });
    if (!opts.keepFocus) reader.querySelector('.rd-close').focus({ preventScroll: true });
    try { history.replaceState(null, '', from ? '#p' + from : '#teksti'); } catch (_) {}
  }

  function closeReader() {
    body.classList.remove('reading');
    reader.setAttribute('aria-hidden', 'true');
    trunk.querySelectorAll('.is-reading').forEach(node => node.classList.remove('is-reading'));
    try { history.replaceState(null, '', location.pathname + location.search); } catch (_) {}
    if (current) current.focus && current.querySelector('.loc').focus({ preventScroll: true });
  }

  function step(delta) {
    const list = leaves();
    let i = current ? list.indexOf(current) + delta : 0;
    if (i < 0 || i >= list.length) return;
    const leaf = list[i];
    const branch = leaf.closest('.branch');
    if (branch.classList.contains('is-collapsed')) { setCollapsed(branch, false); save(); }
    openAt(+leaf.dataset.from, +leaf.dataset.to, { keepFocus: true });
    leaf.scrollIntoView({ block: 'nearest', behavior: reducedMotion ? 'auto' : 'smooth' });
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a.loc');
    if (link) {
      event.preventDefault();
      openAt(+link.dataset.from, +link.dataset.to);
      return;
    }
    const pn = event.target.closest('.para .pn');
    if (pn) {   /* from the text back to the map */
      event.preventDefault();
      const leaf = leafFor(pn.closest('.para'));
      if (!leaf) return;
      const branch = leaf.closest('.branch');
      if (branch.classList.contains('is-collapsed')) { setCollapsed(branch, false); save(); }
      markReading(leaf, +pn.closest('.para').dataset.n);
      current = leaf;
      leaf.scrollIntoView({ block: 'center', behavior: reducedMotion ? 'auto' : 'smooth' });
      if (!matchMedia('(min-width:1180px)').matches) closeReader();
      return;
    }
    const hit = event.target.closest('.leaves .twig div[data-from], .leaves > .leaf');
    if (!hit || event.target.closest('a')) return;
    if (String(window.getSelection && getSelection()).trim()) return;   /* the reader is selecting text */
    openAt(+hit.dataset.from, +hit.dataset.to);
  });

  reader.querySelector('.rd-close').addEventListener('click', closeReader);
  reader.querySelector('.rd-prev').addEventListener('click', () => step(-1));
  reader.querySelector('.rd-next').addEventListener('click', () => step(1));
  document.getElementById('read-all').addEventListener('click', () => openAt(0, 0));
  document.addEventListener('keydown', event => {
    if (!body.classList.contains('reading')) return;
    if (event.key === 'Escape') closeReader();
  });

  /* While the text scrolls, the map follows: the leaf that covers the
     paragraph at the top of the pane is marked, and on a wide screen it is
     brought into view if it has scrolled out. */
  let spyQueued = false;
  rbody.addEventListener('scroll', () => {
    if (spyQueued || Date.now() < quietUntil) return;
    spyQueued = true;
    requestAnimationFrame(() => {
      spyQueued = false;
      const edge = rbody.getBoundingClientRect().top + 40;
      const para = paras.find(p => p.getBoundingClientRect().bottom > edge);
      if (!para) return;
      const leaf = leafFor(para);
      if (!leaf) return;
      const n = +para.dataset.n;
      markReading(leaf, n);
      if (leaf !== current) {
        current = leaf;
        const inRange = range && n >= range[0] && n <= range[1];
        setCrumb(leaf, inRange ? range[0] : +leaf.dataset.from, inRange ? range[1] : +leaf.dataset.to);
        if (matchMedia('(min-width:1180px)').matches && !leaf.closest('.is-collapsed')) {
          const box = leaf.getBoundingClientRect();
          if (box.top < 0 || box.bottom > innerHeight) leaf.scrollIntoView({ block: 'center', behavior: reducedMotion ? 'auto' : 'smooth' });
        }
      }
    });
  }, { passive: true });

  reader.setAttribute('aria-hidden', 'true');
  const start = /^#p(\d+)$/.exec(location.hash);
  if (start) {
    const leaf = leafFor(paraOf(+start[1]) || paras[0]);
    if (leaf) openAt(+leaf.dataset.from, +leaf.dataset.to, { keepFocus: true });
  } else if (location.hash === '#teksti') openAt(0, 0, { keepFocus: true });
