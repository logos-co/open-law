import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function editInterpretations() {
  const editInterpretationModal: HTMLElement = document.querySelector(
    '#edit_interpretation_modal',
  );
  const editInterpretationModalBtns = document.querySelectorAll(
    '#callEditInterpretationModal',
  );
  const interpretationIdInEditInterpretationModal: HTMLInputElement =
    document.querySelector('#edit_interpretation_modal_interpretation_id');
  const interpretationTextInEditInterpretationModal: HTMLInputElement =
    document.querySelector('#edit-interpretation-text-input');
  const editInterpretationForm: HTMLFormElement = document.querySelector(
    '#edit_interpretation_modal_form',
  );
  const editInterpretationTextQuillOnModal: HTMLInputElement =
    document.querySelector('#edit-interpretation-text');
  // edit
  const modalOptions: ModalOptions = {
    placement: 'bottom-right',
    closable: true,
    onHide: () => {
      editInterpretationForm.setAttribute('action', '');
    },
    onShow: () => {},
    onToggle: () => {},
  };
  const interpretationEditModal: ModalInterface = new Modal(
    editInterpretationModal,
    modalOptions,
  );

  if (
    editInterpretationModal &&
    editInterpretationModalBtns &&
    interpretationIdInEditInterpretationModal &&
    interpretationTextInEditInterpretationModal &&
    editInterpretationForm &&
    editInterpretationTextQuillOnModal
  ) {
    const defaultActionPath = editInterpretationForm.getAttribute('action');

    const editModalCloseBtn = document.querySelector(
      '#modalEditInterpretationCloseButton',
    );
    if (editModalCloseBtn) {
      editModalCloseBtn.addEventListener('click', () => {
        interpretationEditModal.hide();
      });
    }
    editInterpretationModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const interpretationId = btn.getAttribute(
          'data-edit-interpretation-id',
        );
        interpretationIdInEditInterpretationModal.value = interpretationId;
        const interpretationText = btn.getAttribute(
          'data-edit-interpretation-text',
        );
        interpretationTextInEditInterpretationModal.value = interpretationText;
        editInterpretationTextQuillOnModal.innerHTML = interpretationText;

        let newActionPath: string = '';
        newActionPath = defaultActionPath.replace(
          '0/interpretation_edit',
          `${interpretationId}/interpretation_edit`,
        );

        editInterpretationForm.setAttribute('action', `${newActionPath}`);
        interpretationEditModal.show();
      }),
    );
  }
}
