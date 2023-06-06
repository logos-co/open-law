// Will be useful in next OpenLaw version

interface Permissions {
  [key: string]: number[];
}

const updatePermissionsJSON = (
  permissionsJSON: Permissions,
  checkBoxTrees: Element,
) => {
  const inputs: NodeListOf<HTMLInputElement> = checkBoxTrees.querySelectorAll(
    'input[type=checkbox]',
  );
  inputs.forEach(element => {
    const accessTo: string = `${element.getAttribute('data-access-to')}`;
    const accessToId: number = parseInt(
      element.getAttribute('data-access-to-id'),
    );
    const checked = element.checked;
    if (checked && !permissionsJSON[accessTo].includes(accessToId)) {
      permissionsJSON[accessTo].push(accessToId);
    } else if (!checked && permissionsJSON[accessTo].includes(accessToId)) {
      permissionsJSON[accessTo] = permissionsJSON[accessTo].filter(
        el => el != accessToId,
      );
    }
  });
};

const uncheckParentInputs = (checkbox: HTMLElement) => {
  const parentLiElement: HTMLElement =
    checkbox.parentElement.parentElement.parentElement.parentElement;

  const dataPermission = checkbox.getAttribute('data-permission');

  const parentInputElement: HTMLInputElement = parentLiElement.querySelector(
    `input[type=checkbox][data-permission=${dataPermission}]`,
  );

  if (!parentInputElement.disabled) {
    parentInputElement.checked = false;
  }

  if (parentInputElement.getAttribute('data-root') != 'true') {
    uncheckParentInputs(parentInputElement);
  }
};

const handleCheckboxClick = (checkbox: HTMLInputElement) => {
  const parentLiElement: HTMLElement = checkbox.parentElement.parentElement;

  const checked = checkbox.checked;

  if (!checked) {
    uncheckParentInputs(checkbox);
  }

  const dataPermission = checkbox.getAttribute('data-permission');

  const checkboxes = parentLiElement.querySelectorAll(
    `input[type=checkbox][data-permission=${dataPermission}]`,
  );

  checkboxes.forEach((checkbox: HTMLInputElement) => {
    if (!checkbox.disabled) {
      checkbox.checked = checked;
    }
  });
};

export const initCheckBoxTree = () => {
  const permissionsJSON: Permissions = {
    book: [],
    sub_collection: [],
    collection: [],
    section: [],
  };
  const permissionsJsonInput: HTMLInputElement =
    document.querySelector('#permissions_json');
  const checkBoxTrees = document.querySelectorAll('.checkbox-tree');

  checkBoxTrees.forEach((checkBoxTree: Element) => {
    const checkboxes = checkBoxTree.querySelectorAll('input[type=checkbox]');

    checkboxes.forEach((checkbox: HTMLInputElement) => {
      checkbox.addEventListener('click', () => {
        handleCheckboxClick(checkbox);
        updatePermissionsJSON(permissionsJSON, checkBoxTree);
        permissionsJsonInput.value = JSON.stringify(permissionsJSON);
      });
    });
  });
};
