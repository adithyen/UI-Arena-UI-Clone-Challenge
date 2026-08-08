// Swiggy Help & Support Page Interactive Logic

function activateHelpCat(link, sectionId) {
  // Update sidebar active link state
  document.querySelectorAll('.help-cat-link').forEach(l => l.classList.remove('active-help-cat'));
  link.classList.add('active-help-cat');

  // Hide all sections and show selected section
  document.querySelectorAll('.help-section').forEach(s => {
    s.classList.remove('active-section');
    s.style.display = 'none';
  });

  const target = document.getElementById(sectionId);
  if (target) {
    target.style.display = 'block';
    // Trigger animation
    requestAnimationFrame(() => {
      target.classList.add('active-section');
    });
  }
}

function toggleFaq(btn) {
  const answer = btn.nextElementSibling;
  const isOpen = answer.classList.contains('open');

  // Accordion behavior: close others in same section
  const parentList = btn.closest('.faq-list');
  if (parentList) {
    parentList.querySelectorAll('.faq-a').forEach(a => a.classList.remove('open'));
    parentList.querySelectorAll('.faq-q').forEach(q => q.classList.remove('open'));
  }

  if (!isOpen) {
    answer.classList.add('open');
    btn.classList.add('open');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Handle URL hash if present (e.g. help.html#instamart)
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const targetLink = document.querySelector(`.help-cat-link[href="#${hash}"]`);
    if (targetLink) {
      activateHelpCat(targetLink, hash);
    }
  }

  // Bind sign in drawer trigger if present
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) {
    signInBtn.addEventListener('click', e => {
      e.preventDefault();
      if (typeof openSignIn === 'function') openSignIn();
    });
  }
});
