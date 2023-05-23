export function initGoBack() {
  const goBackBtn: HTMLButtonElement =
    document.querySelector('#tabGoBackButton');
  if (goBackBtn) {
    goBackBtn.addEventListener('click', () => {
      window.history.back();
    });
  }
}
