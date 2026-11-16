/**
 * tooltip-init.js
 * Converts all span[title] elements to Bootstrap 5 popovers (click to toggle).
 * Runs after the DOM is ready. Works with Quarto's [term]{title="..."} syntax.
 */
document.addEventListener('DOMContentLoaded', function () {
  // Find every span that has a title attribute
  document.querySelectorAll('span[title]').forEach(function (el) {
    // Transfer the title to popover data attributes
    el.setAttribute('data-bs-toggle', 'popover');
    el.setAttribute('data-bs-trigger', 'click');
    el.setAttribute('data-bs-placement', 'top');
    el.setAttribute('data-bs-content', el.getAttribute('title'));
    el.setAttribute('data-bs-custom-class', 'definition-popover');
    // Remove title so native browser tooltip doesn't also fire
    el.removeAttribute('title');
    // Initialize Bootstrap popover on this element
    new bootstrap.Popover(el, { html: false });
  });

  // Close any open popover when clicking elsewhere
  document.addEventListener('click', function (e) {
    if (!e.target.closest('span[data-bs-toggle="popover"]')) {
      document.querySelectorAll('span[data-bs-toggle="popover"]').forEach(function (el) {
        var pop = bootstrap.Popover.getInstance(el);
        if (pop) pop.hide();
      });
    }
  });
});
