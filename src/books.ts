import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';

// // For your js code
const $addUserModalElement: HTMLElement =
  document.querySelector('#add-book-modal');

const modalOptions: ModalOptions = {
  placement: 'bottom-right',
  closable: true,
  onHide: () => {
    console.log('modal is hidden');
  },
  onShow: () => {
    console.log('user id: ');
  },
  onToggle: () => {
    console.log('modal has been toggled');
  },
};

const addModal: ModalInterface = new Modal($addUserModalElement, modalOptions);

export function initBooks() {
  // closing add book modal
  const addModalCloseBtn = document.querySelector('#modalAddCloseButton');
  if (addModalCloseBtn) {
    addModalCloseBtn.addEventListener('click', () => {
      addModal.hide();
    });
  }
}
