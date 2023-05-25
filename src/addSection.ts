import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function addSection() {
  const addSectionModal: HTMLElement =
    document.querySelector('#add-section-modal');

  const addSectionModalBtns = document.querySelectorAll('#callAddSectionModal');
  const collectionIdInAddSectionModal: HTMLInputElement =
    document.querySelector('#add_section_modal_collection_id');
  const subCollectionIdInAddSectionModal: HTMLInputElement =
    document.querySelector('#add_section_modal_sub_collection_id');

  const addSectionForm: HTMLFormElement = document.querySelector(
    '#add_section_modal_form',
  );
  if (
    addSectionModal &&
    addSectionModalBtns &&
    collectionIdInAddSectionModal &&
    subCollectionIdInAddSectionModal &&
    addSectionForm
  ) {
    const defaultActionPath = addSectionForm.getAttribute('action');

    const addModalCloseBtn = document.querySelector('#modalSectionCloseButton');
    if (addModalCloseBtn) {
      addModalCloseBtn.addEventListener('click', () => {
        sectionModal.hide();
      });
    }
    addSectionModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const collectionId = btn.getAttribute('data-collection-id');
        const subCollectionId = btn.getAttribute('data-sub-collection-id');
        collectionIdInAddSectionModal.value = collectionId;
        subCollectionIdInAddSectionModal.value = subCollectionId;
        let newActionPath: string = '';
        if (subCollectionId === '_') {
          newActionPath = defaultActionPath.replace(
            '0/0/create_section',
            `${collectionId}/create_section`,
          );
        } else {
          newActionPath = defaultActionPath.replace(
            '0/0/create_section',
            `${collectionId}/${subCollectionId}/create_section`,
          );
        }
        if (newActionPath.includes('/0')) {
          console.log('ALERT');
          return;
        }

        addSectionForm.setAttribute('action', `${newActionPath}`);
        sectionModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      placement: 'bottom-right',
      closable: true,
      onHide: () => {
        addSectionForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const sectionModal: ModalInterface = new Modal(
      addSectionModal,
      modalOptions,
    );
  }
}
