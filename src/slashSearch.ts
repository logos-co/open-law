export function slashSearch() {
  let firstClick: boolean = true;
  const searchBtn: HTMLButtonElement = document.querySelector(
    '#global-search-button',
  );
  const searchInput: HTMLInputElement =
    document.querySelector('#mainSearchInput');
  window.addEventListener('keypress', e => {
    if (e.key === '/' && searchInput) {
      if (firstClick) {
        e.preventDefault();
        firstClick = false;
      }
      searchInput.focus();
    }
    searchInput.addEventListener('blur', () => {
      firstClick = true;
    });
  });
  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', async (e: any) => {
      e.preventDefault();
      const urlParams = new URLSearchParams({
        q: searchInput.value,
      });
      const res = await fetch('/search_interpretations?' + urlParams);
      if (res.status === 200) {
        window.location.replace(res.url);
      } else {
        return;
      }
    });
  }
}
