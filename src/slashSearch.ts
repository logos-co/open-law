export function slashSearch() {
  let firstClick: boolean = true;
  window.addEventListener('keypress', e => {
    const searchInput: HTMLInputElement =
      document.querySelector('#mainSearchInput');
    if (e.key === '/' && searchInput) {
      if (firstClick) {
        e.preventDefault();
        firstClick = false;
      }
      console.log(e.key);
      searchInput.focus();
    }
    searchInput.addEventListener('blur', () => {
      firstClick = true;
    });
  });
}
