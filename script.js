'use strict';

// Navegación compartida: menú móvil, Escape y cierre al elegir una página.
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', 'Abrir menú');
  navigation?.classList.remove('open');
}
menuButton?.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(expanded));
  menuButton.setAttribute('aria-label', expanded ? 'Cerrar menú' : 'Abrir menú');
  navigation.classList.toggle('open', expanded);
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);
document.querySelectorAll('[data-year]').forEach(element => {
  element.textContent = new Intl.DateTimeFormat('es-BO', { year: 'numeric', timeZone: 'America/La_Paz' }).format(new Date());
});

// Filtra el HTML ya presente: las reseñas también se pueden leer sin JavaScript.
const search = document.querySelector('#teacher-search');
if (search && window.schoolStaff) {
  const { teachers, areas } = window.schoolStaff;
  const areaNames = new Map(areas.map(area => [area.id, area.name]));
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const entries = teachers.map(teacher => ({
    ...teacher,
    element: document.getElementById(teacher.id),
    searchable: normalize(teacher.name + ' ' + teacher.areas.map(area => areaNames.get(area)).join(' '))
  }));
  let selectedArea = 'all';
  const filter = () => {
    const query = normalize(search.value);
    const terms = query.split(/\s+/).filter(Boolean);
    let count = 0;
    entries.forEach(teacher => {
      const visible = (selectedArea === 'all' || teacher.areas.includes(selectedArea))
        && terms.every(term => teacher.searchable.includes(term));
      teacher.element.hidden = !visible;
      if (visible) count++;
    });
    document.querySelectorAll('.subject-group').forEach(group => {
      group.hidden = !group.querySelector('.teacher-card:not([hidden])');
    });
    document.querySelectorAll('.shared-specialty').forEach(element => {
      element.hidden = selectedArea !== 'all' || query.length > 0;
    });
    document.querySelector('.empty-state').hidden = count !== 0;
    document.querySelector('#results-status').textContent = selectedArea === 'all' && !query
      ? 'Todas las áreas del plantel'
      : count === 1 ? '1 docente encontrado' : count + ' docentes encontrados';
    document.querySelectorAll('[data-area]').forEach(button => {
      const active = button.dataset.area === selectedArea;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  };
  search.addEventListener('input', filter);
  document.querySelectorAll('[data-area]').forEach(button => {
    button.addEventListener('click', () => {
      selectedArea = button.dataset.area;
      filter();
    });
  });
  document.querySelector('#reset-search').addEventListener('click', () => {
    selectedArea = 'all';
    search.value = '';
    filter();
    search.focus();
  });
}

// Carrusel sin reproducción automática: flechas, indicadores, teclado y gestos.
const carousel = document.querySelector('.carousel');
if (carousel) {
  const slides = [...carousel.querySelectorAll('.slide')];
  const dots = [...carousel.querySelectorAll('[data-slide]')];
  let current = 0;
  function showSlide(index) {
    const focusedSlide = document.activeElement?.closest('.slide');
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => { slide.hidden = i !== current; });
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === current);
      dot.setAttribute('aria-pressed', String(i === current));
    });
    if (focusedSlide) slides[current].querySelector('button').focus({ preventScroll: true });
    document.querySelector('#carousel-status').textContent = slides[current].querySelector('img').alt;
  }
  carousel.querySelectorAll('[data-direction]').forEach(button => {
    button.addEventListener('click', () => showSlide(current + Number(button.dataset.direction)));
  });
  dots.forEach(dot => dot.addEventListener('click', () => showSlide(Number(dot.dataset.slide))));
  carousel.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showSlide(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  let start = null;
  let suppressClickUntil = 0;
  const slidesElement = carousel.querySelector('.slides');
  slidesElement.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse') start = { x: event.clientX, y: event.clientY };
  });
  slidesElement.addEventListener('pointerup', event => {
    if (!start) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    start = null;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.3) {
      suppressClickUntil = Date.now() + 400;
      showSlide(current + (dx < 0 ? 1 : -1));
    }
  });
  slidesElement.addEventListener('pointercancel', () => { start = null; });
  slidesElement.addEventListener('click', event => {
    if (Date.now() < suppressClickUntil) {
      event.preventDefault();
      event.stopPropagation();
    }
  }, true);
}

// Dialog nativo: foco contenido, retorno al disparador y cierre con Escape.
const lightbox = document.querySelector('.lightbox');
if (lightbox) {
  const photos = [];
  document.querySelectorAll('[data-full]').forEach(button => {
    if (!photos.some(photo => photo.src === button.dataset.full)) {
      photos.push({ src: button.dataset.full, alt: button.querySelector('img').alt });
    }
  });
  const enlarged = lightbox.querySelector('.lightbox-image');
  let current = 0;
  let trigger = null;
  function showPhoto(index) {
    current = (index + photos.length) % photos.length;
    enlarged.src = photos[current].src;
    enlarged.alt = photos[current].alt;
    document.querySelector('#lightbox-status').textContent = photos[current].alt;
  }
  document.querySelectorAll('[data-full]').forEach(button => {
    button.addEventListener('click', () => {
      trigger = button;
      showPhoto(photos.findIndex(photo => photo.src === button.dataset.full));
      lightbox.showModal();
      document.body.classList.add('modal-open');
      lightbox.querySelector('.lightbox-close').focus();
    });
  });
  lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
  lightbox.querySelector('.lightbox-prev').addEventListener('click', () => showPhoto(current - 1));
  lightbox.querySelector('.lightbox-next').addEventListener('click', () => showPhoto(current + 1));
  lightbox.addEventListener('click', event => {
    if (event.target === lightbox) lightbox.close();
  });
  lightbox.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showPhoto(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  lightbox.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    trigger?.focus({ preventScroll: true });
  });
  let start = null;
  enlarged.addEventListener('touchstart', event => {
    start = { x: event.changedTouches[0].clientX, y: event.changedTouches[0].clientY };
  }, { passive: true });
  enlarged.addEventListener('touchend', event => {
    if (!start) return;
    const dx = event.changedTouches[0].clientX - start.x;
    const dy = event.changedTouches[0].clientY - start.y;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.3) showPhoto(current + (dx < 0 ? 1 : -1));
    start = null;
  }, { passive: true });
}
