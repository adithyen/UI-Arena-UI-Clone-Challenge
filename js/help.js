// help page accordion and category nav

function activateHelpCat(link, sectionId) {
  // update nav
  document.querySelectorAll('.help-cat-link').forEach(l => l.classList.remove('active-help-cat'));
  link.classList.add('active-help-cat');
  // show correct section
  document.querySelectorAll('.help-section').forEach(s => s.style.display = 'none');
  const target = document.getElementById(sectionId);
  if (target) target.style.display = 'block';
}

function toggleFaq(btn) {
  const answer = btn.nextElementSibling;
  const isOpen = answer.classList.contains('open');
  // close all first
  document.querySelectorAll('.faq-a').forEach(a => a.classList.remove('open'));
  document.querySelectorAll('.faq-q').forEach(q => q.classList.remove('open'));
  if (!isOpen) {
    answer.classList.add('open');
    btn.classList.add('open');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});
