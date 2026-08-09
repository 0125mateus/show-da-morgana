/**
 * Cortinas: começam fechadas → abrem e ficam amarradas nas laterais.
 * API: openCurtains() | closeCurtains() | toggleCurtains()
 *
 * Eventos:
 *   curtains:open   — no momento em que a abertura começa
 *   curtains:opened — quando a animação termina (~4.5s)
 */
(function () {
  "use strict";

  var OPEN_DELAY_MS = 700;
  var OPEN_DURATION_MS = 4500;
  var ROOT_ID = "theaterCurtain";
  var CLOSED_CLASS = "curtains-closed";

  function getRoot() {
    return document.getElementById(ROOT_ID);
  }

  function openCurtains() {
    var root = getRoot();
    if (!root) return;
    if (!root.classList.contains(CLOSED_CLASS)) return;

    root.classList.remove(CLOSED_CLASS);
    window.dispatchEvent(new CustomEvent("curtains:open"));

    window.setTimeout(function () {
      window.dispatchEvent(new CustomEvent("curtains:opened"));
    }, OPEN_DURATION_MS);
  }

  function closeCurtains() {
    var root = getRoot();
    if (!root) return;
    root.classList.add(CLOSED_CLASS);
    window.dispatchEvent(new CustomEvent("curtains:close"));
  }

  function toggleCurtains() {
    var root = getRoot();
    if (!root) return;
    if (root.classList.contains(CLOSED_CLASS)) openCurtains();
    else closeCurtains();
  }

  function autoOpen() {
    var root = getRoot();
    if (!root) return;

    var reduced =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduced) {
      openCurtains();
      return;
    }

    window.setTimeout(openCurtains, OPEN_DELAY_MS);
  }

  window.openCurtains = openCurtains;
  window.closeCurtains = closeCurtains;
  window.toggleCurtains = toggleCurtains;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", autoOpen);
  } else {
    autoOpen();
  }
})();
