export function renameSubCollection() {
  const renameSubCollectionBtns = document.querySelectorAll(
    '[id^="rename-sub-collection-button-"]',
  );
  const subCollectionRenameForms: NodeListOf<HTMLFormElement> =
    document.querySelectorAll('[id^="rename-sub-collection-label-form-"]');
  if (
    renameSubCollectionBtns.length > 0 &&
    subCollectionRenameForms.length > 0
  ) {
    renameSubCollectionBtns.forEach((btn, index) => {
      btn.addEventListener('click', () => {
        const inputsForRename: NodeListOf<HTMLInputElement> =
          document.querySelectorAll(`[id^="edit-sub-collection-label-"]`);
        const oldName = inputsForRename[index].value;
        inputsForRename[index].removeAttribute('readonly');
        inputsForRename[index].value = '';
        inputsForRename[index].focus();
        inputsForRename[index].addEventListener('blur', () => {
          inputsForRename[index].value = oldName;
        });
        subCollectionRenameForms[index].addEventListener('submit', async e => {
          e.preventDefault();
          const bookId =
            subCollectionRenameForms[index].getAttribute('data-book-id');
          const collectionId =
            subCollectionRenameForms[index].getAttribute('data-collection-id');
          const subCollectionId = subCollectionRenameForms[index].getAttribute(
            'data-sub-collection-id',
          );
          const newLabel = inputsForRename[index].value;
          inputsForRename[index].readOnly = true;

          let url = `/book/${bookId}/${collectionId}/${subCollectionId}/edit`;

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
