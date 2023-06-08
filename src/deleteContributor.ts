import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';
export function deleteContributor() {
  const deleteContributorModal: HTMLElement = document.querySelector(
    '#delete_contributor_modal',
  );

  const deleteContributorModalBtns = document.querySelectorAll(
    '#callDeleteContributorModal',
  );
  const userIdInDeleteContributorModal: HTMLInputElement =
    document.querySelector('#delete_contributor_modal_user_id');

  const deleteContributorForm: HTMLFormElement = document.querySelector(
    '#delete_contributor_modal_form',
  );

  if (
    deleteContributorModal &&
    deleteContributorModalBtns &&
    userIdInDeleteContributorModal &&
    deleteContributorForm
  ) {
    const deleteModalCloseBtn = document.querySelector(
      '#modalDeleteContributorCloseButton',
    );
    if (deleteModalCloseBtn) {
      deleteModalCloseBtn.addEventListener('click', () => {
        contributorDeleteModal.hide();
      });
    }
    deleteContributorModalBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const userId = btn.getAttribute('data-user-id');
        userIdInDeleteContributorModal.value = userId;
        contributorDeleteModal.show();
      }),
    );
    const modalOptions: ModalOptions = {
      placement: 'bottom-right',
      closable: true,
      onHide: () => {
        deleteContributorForm.setAttribute('action', '');
      },
      onShow: () => {},
      onToggle: () => {},
    };

    const contributorDeleteModal: ModalInterface = new Modal(
      deleteContributorModal,
      modalOptions,
    );
  }
}
