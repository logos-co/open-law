export function quickSearch() {
  const currentSearchInput = document.querySelector('#mainSearchInput');
  if (currentSearchInput) {
    currentSearchInput.addEventListener('input', e => {
      e.preventDefault();
      console.log(e);
    });
  }
}
