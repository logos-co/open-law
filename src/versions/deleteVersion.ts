export function initDeleteVersion() {
  const versionIdInput: HTMLInputElement = document.querySelector(
    '.delete-version-id-input',
  );

  if (versionIdInput) {
    const deleteBtns = document.querySelectorAll('.delete-version-btn');
    deleteBtns.forEach(el => {
      el.addEventListener('click', () => {
        const versionId = el.getAttribute('data-version-id');
        versionIdInput.value = versionId;
      });
    });
  }
}
