import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';

const REQUEST_URLS: {[key: string]: string} = {
  interpretation: '/approve/interpretation/',
  comment: '/approve/comment/',
};

const setAllApproveIconsToInactive = () => {
  const approvedIconElements = document.querySelectorAll('.approved-icon');
  approvedIconElements.forEach(el => {
    el.classList.remove('hidden');
    el.classList.add('hidden');
  });

  const notApprovedIconElements =
    document.querySelectorAll('.not-approved-icon');
  notApprovedIconElements.forEach(el => {
    el.classList.remove('hidden');
  });
};

// prettier-ignore
const $approveInterpretationModalElement: HTMLElement = document.querySelector( '#approve_interpretation_modal', );
const modalOptions: ModalOptions = {onShow: () => {}};
// prettier-ignore
const approveModal: ModalInterface = new Modal( $approveInterpretationModalElement, modalOptions, );

const approveClickEventListener = async (btn: Element) => {
  const approve = btn.getAttribute('data-approve');

  if (!(approve in REQUEST_URLS)) {
    console.error('Unknown data-approve attribute');
    return;
  }

  const entityId = btn.getAttribute('data-entity-id');

  const approvedInterpretationIdBlock = document.querySelector(
    '.approved-interpretation-id',
  );
  if (approve == 'interpretation') {
    // prettier-ignore
    if (approvedInterpretationIdBlock) {
      const approvedInterpretationId = parseInt(
        approvedInterpretationIdBlock.innerHTML,
      );
      if (approvedInterpretationId && approvedInterpretationId != parseInt(entityId)) {
        approveModal.show();

        const approvedInterpretationForm: HTMLFormElement =
          document.querySelector('#approve-interpretation-form');

        const submitFormEventListener = async (e: any) => {
          e.preventDefault();
          approvedInterpretationForm.removeEventListener(
            'submit',
            submitFormEventListener,
          );
          sendApproveRequest(
            approve,
            entityId,
            btn,
            approvedInterpretationIdBlock,
          );
          setAllApproveIconsToInactive();
          approveModal.hide();
        };
        approvedInterpretationForm.addEventListener(
          'submit',
          submitFormEventListener,
        );
        return;
      }
    }
  }

  sendApproveRequest(approve, entityId, btn, approvedInterpretationIdBlock);
};

const sendApproveRequest = async (
  approve: string,
  entityId: string,
  btn: Element,
  approvedInterpretationIdBlock?: Element,
) => {
  const requestUrl = REQUEST_URLS[approve] + entityId;
  const response = await fetch(requestUrl, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const json = await response.json();
  const approved = json.approve;
  if (approve == 'interpretation') {
    if (approved) {
      approvedInterpretationIdBlock!.innerHTML = entityId;
    } else {
      approvedInterpretationIdBlock!.innerHTML = '';
    }
  }

  const approvedIconSvg = btn.querySelector('.approved-icon');
  const notApprovedIconSvg = btn.querySelector('.not-approved-icon');

  approvedIconSvg.classList.remove('hidden');
  notApprovedIconSvg.classList.remove('hidden');
  if (approved) {
    notApprovedIconSvg.classList.add('hidden');
  } else {
    approvedIconSvg.classList.add('hidden');
  }
};

export function initApprove() {
  const approveButtons = document.querySelectorAll('.approve-button');
  approveButtons.forEach(approveButton => {
    approveButton.addEventListener('click', () => {
      approveClickEventListener(approveButton);
    });
  });
}
