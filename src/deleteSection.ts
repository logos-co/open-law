import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function deleteSection() {
  const deleteSectionModal: HTMLElement = document.querySelector(
    '#delete-section-modal',
  );

  const deleteSectionModalBtns = document.querySelectorAll(
    '#callDeleteSectionModal',
  );
  const sectionIdInDeleteSectionModal: HTMLInputElement =
    document.querySelector('#delete_section_modal_section_id');

  const deleteSectionForm: HTMLFormElement = document.querySelector(
    '#delete_section_modal_form',
  );

  if (
    deleteSectionModal &&
    deleteSectionModalBtns &&
    sectionIdInDeleteSectionModal &&
    deleteSectionForm
  ) {
    const defaultActionPath = deleteSectionForm.getAttribute('action');

    const deleteModalCloseBtn = document.querySelector(
      '#modalDeleteSectionCloseButton',
    );
    if (deleteModalCloseBtn) {
      deleteModalCloseBtn.addEventListener('click', () => {
        sectionDeleteModal.hide();
      });
    }
    deleteSectionModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const sectionId = btn.getAttribute('data-section-id');
        sectionIdInDeleteSectionModal.value = sectionId;
        let newActionPath: string = '';
        newActionPath = defaultActionPath.replace(
          '0/delete_section',
          `${sectionId}/delete_section`,
        );

        deleteSectionForm.setAttribute('action', `${newActionPath}`);
        sectionDeleteModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      placement: 'bottom-right',
      closable: true,
      onHide: () => {
        deleteSectionForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const sectionDeleteModal: ModalInterface = new Modal(
      deleteSectionModal,
      modalOptions,
    );
  }
}
