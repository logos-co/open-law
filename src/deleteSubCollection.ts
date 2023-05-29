import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function deleteSubCollection() {
  const deleteSubCollectionModal: HTMLElement = document.querySelector(
    '#delete-sub-collection-modal',
  );

  const deleteSubCollectionModalBtns = document.querySelectorAll(
    '#callDeleteSubCollectionModal',
  );
  const collectionIdInDeleteSubCollectionModal: HTMLInputElement =
    document.querySelector('#delete_sub_collection_modal_collection_id');
  const subCollectionIdInDeleteSubCollectionModal: HTMLInputElement =
    document.querySelector('#delete_sub_collection_modal_sub_collection_id');

  const deleteSubCollectionForm: HTMLFormElement = document.querySelector(
    '#delete_sub_collection_modal_form',
  );

  if (
    deleteSubCollectionModal &&
    deleteSubCollectionModalBtns &&
    collectionIdInDeleteSubCollectionModal &&
    subCollectionIdInDeleteSubCollectionModal &&
    deleteSubCollectionForm
  ) {
    const defaultActionPath = deleteSubCollectionForm.getAttribute('action');

    const deleteModalCloseBtn = document.querySelector(
      '#modalDeleteSubCollectionCloseButton',
    );
    if (deleteModalCloseBtn) {
      deleteModalCloseBtn.addEventListener('click', () => {
        subCollectionDeleteModal.hide();
      });
    }
    deleteSubCollectionModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const subCollectionId = btn.getAttribute('data-sub-collection-id');
        collectionIdInDeleteSubCollectionModal.value = subCollectionId;
        let newActionPath: string = '';

        newActionPath = defaultActionPath.replace(
          '0/delete',
          `${subCollectionId}/delete`,
        );

        deleteSubCollectionForm.setAttribute('action', `${newActionPath}`);
        subCollectionDeleteModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      placement: 'bottom-right',
      closable: true,
      onHide: () => {
        deleteSubCollectionForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const subCollectionDeleteModal: ModalInterface = new Modal(
      deleteSubCollectionModal,
      modalOptions,
    );
  }
}
