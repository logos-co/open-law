import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function deleteSection() {
  const deleteSectionModal: HTMLElement = document.querySelector(
    '#delete-section-modal',
  );

  const deleteSectionModalBtns = document.querySelectorAll(
    '#callDeleteSectionModal',
  );
  const collectionIdInDeleteSectionModal: HTMLInputElement =
    document.querySelector('#delete_section_modal_collection_id');
  const subCollectionIdInDeleteSectionModal: HTMLInputElement =
    document.querySelector('#delete_section_modal_sub_collection_id');
  const sectionIdInDeleteSectionModal: HTMLInputElement =
    document.querySelector('#delete_section_modal_section_id');

  const deleteSectionForm: HTMLFormElement = document.querySelector(
    '#delete_section_modal_form',
  );

  if (
    deleteSectionModal &&
    deleteSectionModalBtns &&
    collectionIdInDeleteSectionModal &&
    subCollectionIdInDeleteSectionModal &&
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
        const collectionId = btn.getAttribute('data-collection-id');
        const subCollectionId = btn.getAttribute('data-sub-collection-id');
        const sectionId = btn.getAttribute('data-section-id');
        collectionIdInDeleteSectionModal.value = collectionId;
        subCollectionIdInDeleteSectionModal.value = subCollectionId;
        sectionIdInDeleteSectionModal.value = sectionId;
        let newActionPath: string = '';
        if (subCollectionId === '_') {
          newActionPath = defaultActionPath.replace(
            '0/0/0/delete_section',
            `${collectionId}/${sectionId}/delete_section`,
          );
        } else {
          newActionPath = defaultActionPath.replace(
            '0/0/0/delete_section',
            `${collectionId}/${subCollectionId}/${sectionId}/delete_section`,
          );
        }

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
