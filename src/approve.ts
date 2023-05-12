const REQUEST_URLS: {[key: string]: string} = {
  interpretation: '/approve/interpretation/',
  comment: '/approve/comment/',
};

const approveClickEventListener = async (btn: Element) => {
  const approve = btn.getAttribute('data-approve');

  if (!(approve in REQUEST_URLS)) {
    console.error('Unknown data-approve attribute');
    return;
  }

  const entityId = btn.getAttribute('data-entity-id');

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
