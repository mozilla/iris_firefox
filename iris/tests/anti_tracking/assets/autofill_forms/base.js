"use strict";

document.addEventListener("DOMContentLoaded", () => {
  let forms = document.querySelectorAll("form");
  for (let form of forms) {
    form.reset();
  }
});