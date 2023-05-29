export function initInterpretations() {
  // delete
  const deleteInterpretationBtns: NodeListOf<HTMLButtonElement> =
    document.querySelectorAll('#delete_interpretation_btn');
  const deleteInterpretationInputOnModal: HTMLInputElement =
    document.querySelector('#interpretation_id');
  if (deleteInterpretationBtns && deleteInterpretationInputOnModal) {
    deleteInterpretationBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-interpretation-id');
        deleteInterpretationInputOnModal.value = id;
      }),
    );
  }
  // edit
  const editInterpretationsBtns: NodeListOf<HTMLButtonElement> =
    document.querySelectorAll('#edit_interpretation_btn');
  const editInterpretationInputOnModal: HTMLInputElement =
    document.querySelector('#edit_interpretation_id');
  const editInterpretationTextInputOnModal: HTMLInputElement =
    document.querySelector('#edit-interpretation-text-input');
  const editInterpretationTextQuillOnModal: HTMLInputElement =
    document.querySelector('#edit-interpretation-text');
  if (
    editInterpretationsBtns &&
    editInterpretationInputOnModal &&
    editInterpretationTextInputOnModal &&
    editInterpretationTextQuillOnModal
  ) {
    editInterpretationsBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-edit-interpretation-id');
        const text = btn.getAttribute('data-edit-interpretation-text');
        editInterpretationInputOnModal.value = id;
        editInterpretationTextInputOnModal.value = text;
        editInterpretationTextQuillOnModal.innerHTML = text;
      }),
    );
  }
}
