import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function addSubCollection() {
  const addSubCollectionModal: HTMLElement = document.querySelector(
    '#add-sub-collection-modal',
  );

  const addSubCollectionModalBtns = document.querySelectorAll(
    '#callAddSubCollectionModal',
  );
  const collectionIdInAddSubCollectionModal: HTMLInputElement =
    document.querySelector('#add_sub_collection_modal_collection_id');

  const addSubCollectionForm: HTMLFormElement = document.querySelector(
    '#add_sub_collection_modal_form',
  );
  if (
    addSubCollectionModal &&
    addSubCollectionModalBtns &&
    collectionIdInAddSubCollectionModal &&
    addSubCollectionForm
  ) {
    const defaultActionPath = addSubCollectionForm.getAttribute('action');

    const addModalCloseBtn = document.querySelector(
      '#modalSubCollectionCloseButton',
    );
    if (addModalCloseBtn) {
      addModalCloseBtn.addEventListener('click', () => {
        subCollectionModal.hide();
      });
    }
    addSubCollectionModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const collectionId = btn.getAttribute('data-collection-id');
        collectionIdInAddSubCollectionModal.value = collectionId;
        const newActionPath = defaultActionPath.replace(
          'create_collection',
          `${collectionId}/create_sub_collection`,
        );

        addSubCollectionForm.setAttribute('action', `${newActionPath}`);
        subCollectionModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      placement: 'bottom-right',
      closable: true,
      onHide: () => {
        addSubCollectionForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const subCollectionModal: ModalInterface = new Modal(
      addSubCollectionModal,
      modalOptions,
    );
  }
}
