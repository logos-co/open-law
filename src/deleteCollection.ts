import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function deleteCollection() {
  const deleteCollectionModal: HTMLElement = document.querySelector(
    '#delete-collection-modal',
  );

  const deleteCollectionModalBtns = document.querySelectorAll(
    '#callDeleteCollectionModal',
  );
  const collectionIdInDeleteCollectionModal: HTMLInputElement =
    document.querySelector('#delete_collection_modal_collection_id');

  const deleteCollectionForm: HTMLFormElement = document.querySelector(
    '#delete_collection_modal_form',
  );

  if (
    deleteCollectionModal &&
    deleteCollectionModalBtns &&
    collectionIdInDeleteCollectionModal &&
    deleteCollectionForm
  ) {
    const defaultActionPath = deleteCollectionForm.getAttribute('action');

    const deleteModalCloseBtn = document.querySelector(
      '#modalDeleteCollectionCloseButton',
    );
    if (deleteModalCloseBtn) {
      deleteModalCloseBtn.addEventListener('click', () => {
        collectionDeleteModal.hide();
      });
    }
    deleteCollectionModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const collectionId = btn.getAttribute('data-collection-id');
        collectionIdInDeleteCollectionModal.value = collectionId;
        let newActionPath: string = '';

        newActionPath = defaultActionPath.replace(
          '0/delete',
          `${collectionId}/delete`,
        );

        deleteCollectionForm.setAttribute('action', `${newActionPath}`);
        collectionDeleteModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      placement: 'bottom-right',
      closable: true,
      onHide: () => {
        deleteCollectionForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const collectionDeleteModal: ModalInterface = new Modal(
      deleteCollectionModal,
      modalOptions,
    );
  }
}
