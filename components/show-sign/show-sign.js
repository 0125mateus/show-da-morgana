/**
 * Letreiro — gera lâmpadas ao redor da borda oval
 */
(function () {
  "use strict";

  function placeBulbs(sign) {
    var lights = sign.querySelector(".show-sign__lights");
    if (!lights) return;

    lights.innerHTML = "";

    var count = window.matchMedia("(max-width: 560px)").matches ? 28 : 42;
    /* Centra as lâmpadas no anel dourado entre a borda externa e a face */
    var rx = 48.2;
    var ry = 45.5;

    for (var i = 0; i < count; i++) {
      var angle = (Math.PI * 2 * i) / count - Math.PI / 2;
      var x = 50 + Math.cos(angle) * rx;
      var y = 50 + Math.sin(angle) * ry;

      var bulb = document.createElement("span");
      bulb.className = "show-sign__bulb";
      bulb.style.left = x + "%";
      bulb.style.top = y + "%";
      bulb.style.animationDelay = (i * 0.08).toFixed(2) + "s";
      lights.appendChild(bulb);
    }
  }

  function init() {
    var signs = document.querySelectorAll(".show-sign");
    signs.forEach(placeBulbs);

    window.addEventListener("resize", function () {
      signs.forEach(placeBulbs);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
