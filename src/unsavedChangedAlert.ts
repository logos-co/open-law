const initAlertOnClick = (element: HTMLElement) => {
  element.addEventListener('click', () => {
    window.addEventListener('beforeunload', function (e) {
      var confirmationMessage =
        'It looks like you have been editing something. ' +
        'If you leave before saving, your changes will be lost.';

      (e || window.event).returnValue = confirmationMessage; //Gecko + IE
      return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
    });
  });
};

export const initUnsavedChangedAlerts = () => {
  const elementsSelectors = [
    '.book-label-input',
    '.book-about-input',
    '.book-tags-input',
    '.multiple-input-word',
    '.contributor-role-select',
    '.edit-permissions-btn',
    '.add-contributor-btn',
  ];

  elementsSelectors.forEach(selector => {
    const elements: NodeListOf<HTMLElement> =
      document.querySelectorAll(selector);
    elements.forEach(element => {
      initAlertOnClick(element);
    });
  });
};
