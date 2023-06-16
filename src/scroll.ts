const scrollToElement = (element: Element) => {
  var headerOffset = 160;
  var elementPosition = element.getBoundingClientRect().top;
  var offsetPosition = elementPosition + window.pageYOffset - headerOffset;

  window.scrollTo({
    top: offsetPosition,
    behavior: 'smooth',
  });
};

export function scroll() {
  const btns = document.querySelectorAll('[href^="#section-"]');
  if (btns) {
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        let link = btn.getAttribute('href');
        link = link.replace('#', '');
        const neededSection = document.querySelector(`[id^="${link}"]`);
        if (neededSection) {
          scrollToElement(neededSection);
        }
      });
    });
  }
  const collectionBtns = document.querySelectorAll('[href^="#collection-"]');
  if (collectionBtns) {
    collectionBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        let link = btn.getAttribute('href');
        link = link.replace('#', '');
        const neededSection = document.querySelector(`[id^="${link}"]`);
        if (neededSection) {
          scrollToElement(neededSection);
        }
      });
    });
  }
}
