export function scroll() {
  const btns = document.querySelectorAll('[href^="#section-"]');
  if (btns) {
    btns.forEach((btn, index) => {
      btn.addEventListener('click', () => {
        let link = btn.getAttribute('href');
        link = link.replace('#', '');
        const neededSection = document.querySelector(`[id^="${link}"]`);
        if (neededSection) {
          neededSection.scrollIntoView(true);
        }
      });
    });
  }
}
