// Swiggy Help Page - Interactive JS

function activateHelpCat(link, sectionId) {
  // Remove active state from all links
  document.querySelectorAll('.help-cat-link').forEach(function(l) {
    l.classList.remove('active-help-cat');
  });
  link.classList.add('active-help-cat');

  // Hide all sections
  document.querySelectorAll('.help-section').forEach(function(s) {
    s.classList.remove('active-section');
  });

  // Show target section
  var target = document.getElementById(sectionId);
  if (target) {
    target.classList.add('active-section');
  }
}

function toggleFaq(btn) {
  var answer = btn.nextElementSibling;
  var isOpen = answer.classList.contains('open');

  // Close all FAQs in the same list (accordion behavior)
  var parentList = btn.closest('.faq-list');
  if (parentList) {
    parentList.querySelectorAll('.faq-a').forEach(function(a) {
      a.classList.remove('open');
    });
    parentList.querySelectorAll('.faq-q').forEach(function(q) {
      q.classList.remove('open');
    });
  }

  // If it was closed, open it
  if (!isOpen) {
    answer.classList.add('open');
    btn.classList.add('open');
  }
}
