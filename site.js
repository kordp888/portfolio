'use strict';
function setLanguage(lang) {
  const ko = lang !== 'en';
  document.documentElement.classList.toggle('ko', ko);
  document.documentElement.lang = ko ? 'ko' : 'en';
  document.title = ko ? '황석하 Derrick Hwang · Forward Deployed Engineer' : 'Derrick Hwang · Forward Deployed Engineer';
  const toggle = document.querySelector('.lang-btn');
  toggle.textContent = ko ? 'EN' : '한국어';
  toggle.setAttribute('aria-label', ko ? 'Switch to English' : '한국어로 전환');
  document.querySelectorAll('[data-alt-ko]').forEach(img => { img.alt = ko ? img.dataset.altKo : img.dataset.altEn; });
  try { localStorage.setItem('lang', ko ? 'ko' : 'en'); } catch (_) {}
}
function toggleLang() { setLanguage(document.documentElement.lang === 'ko' ? 'en' : 'ko'); }
let savedLanguage = 'ko';
try { savedLanguage = localStorage.getItem('lang') || 'ko'; } catch (_) {}
setLanguage(savedLanguage);
document.querySelector('.lang-btn').addEventListener('click', toggleLang);
const menuButton = document.querySelector('.menu-btn');
const menu = document.querySelector('.nav-links');
function closeMenu() { menu.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); }
menuButton.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});
menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.classList.contains('open')) { closeMenu(); menuButton.focus(); }
});
