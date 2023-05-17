export function renameSection() {
  const renameSectionBtns = document.querySelectorAll(
    '[id^="rename-section-button-"]',
  );
  const sectionRenameForms: NodeListOf<HTMLFormElement> =
    document.querySelectorAll('[id^="rename-section-label-form-"]');
  if (renameSectionBtns.length > 0 && sectionRenameForms.length > 0) {
    renameSectionBtns.forEach((btn, index) => {
      btn.addEventListener('click', () => {
        const inputsForRename: NodeListOf<HTMLInputElement> =
          document.querySelectorAll(`[id^="edit-section-label-"]`);
        const oldName = inputsForRename[index].value;
        inputsForRename[index].removeAttribute('readonly');
        inputsForRename[index].value = '';
        inputsForRename[index].focus();
        inputsForRename[index].addEventListener('blur', () => {
          inputsForRename[index].value = oldName;
        });
        sectionRenameForms[index].addEventListener('submit', async e => {
          e.preventDefault();
          const bookId = sectionRenameForms[index].getAttribute('data-book-id');
          const collectionId =
            sectionRenameForms[index].getAttribute('data-collection-id');
          const subCollectionId = sectionRenameForms[index].getAttribute(
            'data-sub-collection-id',
          );
          const sectionId =
            sectionRenameForms[index].getAttribute('data-section-id');
          const newLabel = inputsForRename[index].value;
          inputsForRename[index].readOnly = true;

          let url = '';
          if (subCollectionId === '_') {
            url = `/book/${bookId}/${collectionId}/${sectionId}/edit_section_label`;
          } else {
            url = `/book/${bookId}/${collectionId}/${subCollectionId}/${sectionId}/edit_section_label`;
          }

          const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              label: newLabel,
              section_id: sectionId,
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
