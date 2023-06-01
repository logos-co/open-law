import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function deleteInterpretation() {
  const deleteInterpretationModal: HTMLElement = document.querySelector(
    '#delete-interpretation-modal',
  );

  const deleteInterpretationModalBtns = document.querySelectorAll(
    '#callDeleteInterpretationModal',
  );

  const interpretationIdInDeleteInterpretationModal: HTMLInputElement =
    document.querySelector('#delete_interpretation_modal_interpretation_id');

  const deleteInterpretationForm: HTMLFormElement = document.querySelector(
    '#delete_interpretation_modal_form',
  );

  if (
    deleteInterpretationModal &&
    deleteInterpretationModalBtns &&
    interpretationIdInDeleteInterpretationModal &&
    deleteInterpretationForm
  ) {
    const defaultActionPath = deleteInterpretationForm.getAttribute('action');

    const deleteModalCloseBtn = document.querySelector(
      '#modalDeleteInterpretationCloseButton',
    );
    if (deleteModalCloseBtn) {
      deleteModalCloseBtn.addEventListener('click', () => {
        interpretationDeleteModal.hide();
      });
    }
    deleteInterpretationModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const interpretationId = btn.getAttribute('data-interpretation-id');
        interpretationIdInDeleteInterpretationModal.value = interpretationId;
        let newActionPath: string = '';

        newActionPath = defaultActionPath.replace(
          '0/delete_interpretation',
          `${interpretationId}/delete_interpretation`,
        );
        console.log(defaultActionPath);

        deleteInterpretationForm.setAttribute('action', `${newActionPath}`);
        interpretationDeleteModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      closable: true,
      onHide: () => {
        deleteInterpretationForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const interpretationDeleteModal: ModalInterface = new Modal(
      deleteInterpretationModal,
      modalOptions,
    );
  }
}
