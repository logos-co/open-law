export function initEditVersion() {
  const versionIdInput: HTMLInputElement =
    document.querySelector('.version-id-input');
  const versionSemverInput: HTMLInputElement = document.querySelector(
    '.version-semver-input',
  );

  if (versionIdInput && versionSemverInput) {
    const editBtns = document.querySelectorAll('.edit-version-label-btns');
    editBtns.forEach(el => {
      const versionId = el.getAttribute('data-version-id');
      const versionSemver = el.getAttribute('data-version-semver');

      versionIdInput.value = versionId;
      versionSemverInput.value = versionSemver;
    });
  }
}
