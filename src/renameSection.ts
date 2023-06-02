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
        const scrfInput: HTMLInputElement =
          document.querySelector('#csrf_token');
        const oldName = inputsForRename[index].value;
        inputsForRename[index].removeAttribute('readonly');
        inputsForRename[index].value = oldName;
        inputsForRename[index].focus();
        inputsForRename[index].selectionStart = inputsForRename[
          index
        ].selectionEnd = 257;
        inputsForRename[index].addEventListener('blur', () => {
          inputsForRename[index].value = oldName;
        });
        console.log(sectionRenameForms[index]);
        sectionRenameForms[index].addEventListener('submit', async e => {
          e.preventDefault();
          const bookId = sectionRenameForms[index].getAttribute('data-book-id');
          const sectionId =
            sectionRenameForms[index].getAttribute('data-section-id');
          const newLabel = inputsForRename[index].value;
          inputsForRename[index].readOnly = true;

          let url = '';
          url = `/book/${bookId}/${sectionId}/edit_section`;

          const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              label: newLabel,
              section_id: sectionId,
              csrf_token: scrfInput ? scrfInput.value : '',
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
