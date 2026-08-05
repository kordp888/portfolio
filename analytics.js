/* Analytics — GA4 via GTM.
 * Event design: pageview alone proves nothing. These events answer
 * "which proof did a visitor actually engage with, and did they leave to check it?"
 *
 * Activate by setting ANALYTICS.gtmId (and optionally ga4Id for direct gtag).
 * Empty id = no network calls, no cookies. Safe to ship un-configured.
 */
const ANALYTICS = {
  gtmId: '',   // e.g. 'GTM-XXXXXXX'
  ga4Id: '',   // optional direct GA4, e.g. 'G-XXXXXXXXXX'
};

window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }

// Consent Mode v2 defaults — denied until granted. Keeps the site cookie-free
// for visitors who never interact with a consent prompt.
gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'granted',
  functionality_storage: 'granted',
});

(function loadContainers() {
  if (ANALYTICS.gtmId) {
    dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + ANALYTICS.gtmId;
    document.head.appendChild(s);
  }
  if (ANALYTICS.ga4Id) {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ANALYTICS.ga4Id;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', ANALYTICS.ga4Id, { send_page_view: true });
  }
})();

function track(event, params) {
  dataLayer.push(Object.assign({ event }, params));
  if (!ANALYTICS.gtmId && !ANALYTICS.ga4Id) console.debug('[analytics]', event, params);
}

const projectOf = (el) => {
  const card = el.closest('.card');
  return card ? card.querySelector('h3').textContent.trim() : null;
};

document.addEventListener('DOMContentLoaded', () => {
  track('site_view', {
    lang: document.documentElement.classList.contains('ko') ? 'ko' : 'en',
    viewport: window.innerWidth < 640 ? 'mobile' : 'desktop',
  });

  // Outbound clicks — the real conversion. Which proof did they go verify?
  document.querySelectorAll('a[href^="http"]').forEach((a) => {
    a.addEventListener('click', () => {
      const host = new URL(a.href).hostname;
      track('outbound_click', {
        destination: host,
        link_text: a.textContent.trim(),
        project: projectOf(a),
        placement: a.closest('.card') ? 'project_card'
                 : a.closest('header') ? 'hero'
                 : a.closest('footer') ? 'footer' : 'other',
      });
    });
  });

  // Hero CTA — intent to browse before any project is seen.
  document.querySelectorAll('.hero-cta a[href^="#"]').forEach((a) => {
    a.addEventListener('click', () => track('cta_click', { cta: 'see_projects' }));
  });

  // Language toggle — tells me which audience actually lands here.
  const langBtn = document.querySelector('.lang-btn');
  if (langBtn) {
    langBtn.addEventListener('click', () => {
      track('language_toggle', {
        lang: document.documentElement.classList.contains('ko') ? 'ko' : 'en',
      });
    });
  }

  // Section reach — how far down the story a visitor gets.
  if ('IntersectionObserver' in window) {
    const seenSections = new Set();
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting || seenSections.has(e.target.id)) return;
        seenSections.add(e.target.id);
        track('section_view', { section: e.target.id });
      });
    }, { threshold: 0.4 });
    document.querySelectorAll('section[id]').forEach((s) => sectionObserver.observe(s));

    // Per-project card view — which of the three proofs got attention.
    const seenCards = new Set();
    const cardObserver = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        const name = e.target.querySelector('h3').textContent.trim();
        if (!e.isIntersecting || seenCards.has(name)) return;
        seenCards.add(name);
        track('project_view', { project: name });
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('.card').forEach((c) => cardObserver.observe(c));
  }

  // Engaged visit — 30s without leaving. Separates real readers from bounces.
  setTimeout(() => track('engaged_visit', { seconds: 30 }), 30000);
});
