// ================================================================
// gen.lib — Premium Animations & Interactions
// ================================================================

(function () {
  'use strict';

  // ── LOADING SCREEN ──────────────────────────────────────────────
  window.addEventListener('load', () => {
    setTimeout(() => {
      const loader = document.getElementById('loading-screen');
      if (loader) loader.classList.add('hidden');
    }, 2800);
  });

  // ── CURSOR GLOW ─────────────────────────────────────────────────
  const cursorGlow = document.querySelector('.cursor-glow');
  if (cursorGlow) {
    let mx = 0, my = 0, cx = 0, cy = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    const animateCursor = () => {
      cx += (mx - cx) * 0.08;
      cy += (my - cy) * 0.08;
      cursorGlow.style.left = cx + 'px';
      cursorGlow.style.top  = cy + 'px';
      requestAnimationFrame(animateCursor);
    };
    animateCursor();
  }

  // ── NAV SCROLL EFFECT ───────────────────────────────────────────
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });
  }

  // ── SMOOTH INERTIA SCROLLING ─────────────────────────────────────
  // Disabled fixed positioning smooth scroll as it intercepts browser coordinate mapping,
  // making input elements unclickable with a mouse. Using standard native scroll instead.
  /*
  let scrollCurrent = 0;
  let scrollTarget  = 0;
  let isScrolling   = false;

  const scrollWrapper = document.querySelector('.scroll-container');
  if (scrollWrapper && window.innerWidth > 768) {
    document.body.style.overflow = 'hidden';
    scrollWrapper.style.position = 'fixed';
    scrollWrapper.style.top = '0';
    scrollWrapper.style.left = '0';
    scrollWrapper.style.right = '0';
    scrollWrapper.style.willChange = 'transform';

    const updateBodyHeight = () => {
      document.body.style.height = scrollWrapper.scrollHeight + 'px';
    };
    updateBodyHeight();
    new ResizeObserver(updateBodyHeight).observe(scrollWrapper);

    window.addEventListener('wheel', e => {
      scrollTarget += e.deltaY;
      scrollTarget = Math.max(0, Math.min(scrollTarget, scrollWrapper.scrollHeight - window.innerHeight));
      if (!isScrolling) { isScrolling = true; smoothScroll(); }
    }, { passive: true });

    const smoothScroll = () => {
      scrollCurrent += (scrollTarget - scrollCurrent) * 0.085;
      const diff = Math.abs(scrollTarget - scrollCurrent);
      scrollWrapper.style.transform = `translateY(${-scrollCurrent}px)`;
      if (diff > 0.5) requestAnimationFrame(smoothScroll);
      else { isScrolling = false; scrollCurrent = scrollTarget; scrollWrapper.style.transform = `translateY(${-scrollCurrent}px)`; }
      triggerReveal();
    };
  }
  */

  // ── CLEANUP: Force-reset any stale styles from old cached JS ──────
  // This ensures scroll-container uses normal document flow even if
  // the browser served a cached copy of the old script previously.
  const scrollWrapper = document.querySelector('.scroll-container');
  if (scrollWrapper) {
    scrollWrapper.style.position = '';
    scrollWrapper.style.top = '';
    scrollWrapper.style.left = '';
    scrollWrapper.style.right = '';
    scrollWrapper.style.willChange = '';
    scrollWrapper.style.transform = '';
  }
  document.body.style.overflow = '';
  document.body.style.height = '';

  // ── SCROLL REVEAL ───────────────────────────────────────────────
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');

  const triggerReveal = () => {
    const viewH = window.innerHeight;
    reveals.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < viewH * 0.9 && rect.bottom > 0) el.classList.add('visible');
    });
  };

  window.addEventListener('scroll', triggerReveal, { passive: true });
  triggerReveal(); // run on load too

  // Stagger children of .stagger containers
  document.querySelectorAll('.stagger').forEach(container => {
    [...container.children].forEach((child, i) => {
      child.style.setProperty('--i', i);
      child.style.transitionDelay = `${i * 0.08}s`;
    });
  });

  // ── BOOK SHELF ANIMATION ─────────────────────────────────────────
  const booksRow = document.querySelector('.books-row');
  if (booksRow) {
    const bookColors = [
      ['#4a0082','#6a0dad'],['#2d0070','#5b0099'],['#1a0050','#3d0080'],
      ['#6b0099','#8b00e8'],['#3b0070','#5b00a8'],['#1d0060','#4a0090'],
      ['#7a00a0','#9a00c0'],['#250060','#450080'],['#550090','#7500b0'],
      ['#0f0040','#2f0060'],['#600090','#8000b0'],['#380070','#580090']
    ];
    const bookHeights = [120,140,110,155,125,145,115,135,150,118,142,128];

    bookColors.forEach(([c1, c2], i) => {
      const spine = document.createElement('div');
      spine.className = 'book-spine';
      spine.style.cssText = `
        height: ${bookHeights[i]}px;
        background: linear-gradient(to right, ${c1}, ${c2});
        width: ${28 + Math.random()*10}px;
      `;
      booksRow.appendChild(spine);
    });
  }

  // ── SCROLL-DRIVEN BOOK FALL ──────────────────────────────────────
  const heroBookScene = document.querySelector('.book-scene');
  let bookFallTriggered = false;

  if (heroBookScene) {
    const triggerBookFall = () => {
      if (bookFallTriggered) return;
      const scrollY = scrollWrapper ? Math.abs(parseFloat(scrollWrapper.style.transform?.replace(/[^-\d.]/g,'')) || 0) : window.scrollY;
      const threshold = window.innerHeight * 0.2;

      if (scrollY > threshold) {
        bookFallTriggered = true;
        spawnFallingBooks();
      }
    };

    window.addEventListener('scroll', triggerBookFall, { passive: true });

    // Also trigger via wheel for inertia mode
    window.addEventListener('wheel', () => setTimeout(triggerBookFall, 100), { passive: true });

    const spawnFallingBooks = () => {
      const scene = heroBookScene;
      const colors = ['#4a0082','#6a0dad','#7500b0','#8b00e8','#5b0099','#3d0080'];
      for (let i = 0; i < 5; i++) {
        const book = document.createElement('div');
        book.className = 'book-falling';
        const h = 100 + Math.random() * 60;
        const startY = -(200 + Math.random() * 200);
        const startRot = -20 + Math.random() * 40;
        const leftPos = 100 + i * 80 + Math.random() * 30;
        const col = colors[i % colors.length];
        book.style.cssText = `
          width: ${26 + Math.random()*10}px;
          height: ${h}px;
          background: linear-gradient(to right, ${col}cc, ${col});
          left: ${leftPos}px;
          bottom: 12px;
          --start-y: ${startY}px;
          --start-rot: ${startRot}deg;
          --fall-duration: ${0.9 + Math.random() * 0.5}s;
          --fall-delay: ${i * 0.15}s;
        `;
        scene.appendChild(book);
      }
    };
  }

  // ── FLOATING PARTICLES ───────────────────────────────────────────
  const particleContainer = document.querySelector('.particles');
  if (particleContainer) {
    for (let i = 0; i < 40; i++) {
      const p = document.createElement('div');
      p.className = 'particle';
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      p.style.cssText = `
        left: ${x}%;
        top: ${y}%;
        --dur: ${6 + Math.random() * 10}s;
        --delay: ${Math.random() * 8}s;
        --dx1: ${-30 + Math.random()*60}px;
        --dy1: ${-20 + Math.random()*-40}px;
        --dx2: ${-50 + Math.random()*100}px;
        --dy2: ${-40 + Math.random()*-80}px;
        --dx3: ${-80 + Math.random()*160}px;
        --dy3: ${-80 + Math.random()*-140}px;
        opacity: 0;
        width: ${1 + Math.random()*2}px;
        height: ${1 + Math.random()*2}px;
      `;
      particleContainer.appendChild(p);
    }
  }

  // ── TEXT SCRAMBLE / TYPEWRITER ────────────────────────────────────
  class TextScramble {
    constructor(el) {
      this.el = el;
      this.chars = '!<>-_\\/[]{}—=+*^?#________';
      this.update = this.update.bind(this);
    }

    setText(newText) {
      const oldText = this.el.innerText;
      const length = Math.max(oldText.length, newText.length);
      const promise = new Promise(resolve => this.resolve = resolve);
      this.queue = [];
      for (let i = 0; i < length; i++) {
        const from = oldText[i] || '';
        const to   = newText[i] || '';
        const start = Math.floor(Math.random() * 20);
        const end   = start + Math.floor(Math.random() * 20);
        this.queue.push({ from, to, start, end });
      }
      cancelAnimationFrame(this.frameReq);
      this.frame = 0;
      this.update();
      return promise;
    }

    update() {
      let output = '';
      let complete = 0;
      for (let i = 0, n = this.queue.length; i < n; i++) {
        let { from, to, start, end, char } = this.queue[i];
        if (this.frame >= end) {
          complete++;
          output += to;
        } else if (this.frame >= start) {
          if (!char || Math.random() < 0.28) {
            char = this.chars[Math.floor(Math.random() * this.chars.length)];
            this.queue[i].char = char;
          }
          output += `<span style="opacity:0.4;color:var(--purple-bright)">${char}</span>`;
        } else {
          output += from;
        }
      }
      this.el.innerHTML = output;
      if (complete === this.queue.length) {
        this.resolve();
      } else {
        this.frameReq = requestAnimationFrame(this.update);
        this.frame++;
      }
    }
  }

  // Apply scramble to elements with data-scramble attribute
  document.querySelectorAll('[data-scramble]').forEach(el => {
    const original = el.textContent;
    const scrambler = new TextScramble(el);
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          scrambler.setText(original);
          observer.disconnect();
        }
      });
    }, { threshold: 0.5 });
    observer.observe(el);
  });

  // ── COUNTER ANIMATION ─────────────────────────────────────────────
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    let started = false;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !started) {
          started = true;
          animateCount(el, 0, target, 2000, suffix);
        }
      });
    }, { threshold: 0.5 });
    observer.observe(el);
  });

  function animateCount(el, start, end, duration, suffix) {
    const startTime = performance.now();
    const easeOut = t => 1 - Math.pow(1 - t, 3);
    const animate = currentTime => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value = Math.floor(easeOut(progress) * (end - start) + start);
      el.textContent = value.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }

  // ── PARALLAX DEPTH ────────────────────────────────────────────────
  const parallaxEls = document.querySelectorAll('[data-parallax]');
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    parallaxEls.forEach(el => {
      const speed = parseFloat(el.dataset.parallax) || 0.3;
      el.style.transform = `translateY(${scrollY * speed}px)`;
    });
  }, { passive: true });

  // ── MAGNETIC BUTTONS ──────────────────────────────────────────────
  document.querySelectorAll('.btn-primary, .btn-ghost').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      btn.style.transform = `translate(${x * 0.15}px, ${y * 0.2}px) translateY(-2px)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });

  // ── RIPPLE EFFECT ON BUTTONS ───────────────────────────────────────
  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const ripple = document.createElement('span');
      const rect   = btn.getBoundingClientRect();
      const size   = Math.max(rect.width, rect.height);
      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${e.clientX - rect.left - size/2}px;
        top:  ${e.clientY - rect.top - size/2}px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        transform: scale(0);
        animation: rippleAnim 0.6s ease forwards;
        pointer-events: none;
      `;
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  const style = document.createElement('style');
  style.textContent = '@keyframes rippleAnim { to { transform: scale(4); opacity: 0; } }';
  document.head.appendChild(style);

  // ── MESSAGES AUTO-DISMISS ─────────────────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
  

})();
