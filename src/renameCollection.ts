export function renameCollection() {
  const renameCollectionBtns = document.querySelectorAll(
    '[id^="rename-collection-button-"]',
  );
  const collectionRenameForms: NodeListOf<HTMLFormElement> =
    document.querySelectorAll('[id^="rename-collection-label-form-"]');
  if (renameCollectionBtns.length > 0 && collectionRenameForms.length > 0) {
    renameCollectionBtns.forEach((btn, index) => {
      btn.addEventListener('click', () => {
        const inputsForRename: NodeListOf<HTMLInputElement> =
          document.querySelectorAll(`[id^="edit-collection-label-"]`);
        inputsForRename[index].removeAttribute('readonly');
        const oldName = inputsForRename[index].value;
        inputsForRename[index].value = '';
        inputsForRename[index].focus();
        inputsForRename[index].addEventListener('blur', () => {
          inputsForRename[index].value = oldName;
        });
        collectionRenameForms[index].addEventListener('submit', async e => {
          e.preventDefault();
          const bookId =
            collectionRenameForms[index].getAttribute('data-book-id');
          const collectionId =
            collectionRenameForms[index].getAttribute('data-collection-id');
          const newLabel = inputsForRename[index].value;
          inputsForRename[index].readOnly = true;

          let url = `/book/${bookId}/${collectionId}/edit`;

          const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              label: newLabel,
            }),
          });
          if (response.status == 200) {
            location.reload();
          } else return;
        });
      });
    });
  }
}
