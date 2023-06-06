import {Dropdown, DropdownInterface} from 'flowbite';
import type {DropdownOptions} from 'flowbite';

// Triggers and elements for collections
const contextCollectionMenuTriggers: NodeListOf<HTMLElement> =
  document.querySelectorAll('[id^="dropdownCollectionContextButton"]');
const collectionContextMenu: NodeListOf<HTMLElement> =
  document.querySelectorAll('[data^="collection-context-menu-"]');

// Triggers and elements for sub_collections
const subCollectionContextMenu: NodeListOf<HTMLElement> =
  document.querySelectorAll('[data^="sub-collection-context-menu-"]');
const contextSubCollectionMenuTriggers: NodeListOf<HTMLElement> =
  document.querySelectorAll('[id^="dropdownSubCollectionContextButton"]');

// Triggers and elements for sub_collections
const sectionContextMenu: NodeListOf<HTMLElement> = document.querySelectorAll(
  '[data^="section-context-menu-"]',
);
const contextSectionMenuTriggers: NodeListOf<HTMLElement> =
  document.querySelectorAll('[id^="dropdownSectionContextButton"]');

let currentElement: DropdownInterface | null = null;

const options: DropdownOptions = {
  offsetSkidding: 200,
  offsetDistance: 0,
  onHide: () => {},
  onShow: tooltip => {
    // this will close opened menu if you trigger another one
    if (currentElement) {
      if (tooltip !== currentElement) {
        currentElement.hide();
      }
      currentElement = tooltip;
    } else {
      currentElement = tooltip;
    }
  },
  onToggle: () => {},
};

let collectionDropDownArray: Dropdown[] = [];
let subCollectionDropDownArray: Dropdown[] = [];
let sectionDropDownArray: Dropdown[] = [];

// Creating for each dropDownMenu in DOM a Dropdown from FlowBite
collectionContextMenu.forEach((menu, index) => {
  collectionDropDownArray.push(
    new Dropdown(menu, contextCollectionMenuTriggers[index], options),
  );
});
subCollectionContextMenu.forEach((menu, index) => {
  subCollectionDropDownArray.push(
    new Dropdown(menu, contextSubCollectionMenuTriggers[index], options),
  );
});
sectionContextMenu.forEach((menu, index) => {
  sectionDropDownArray.push(
    new Dropdown(menu, contextSectionMenuTriggers[index], options),
  );
});

export function rightClick() {
  const collectionElements: NodeListOf<HTMLHeadingElement> =
    document.querySelectorAll('[id^="accordion-collapse-heading-"]');
  const subCollectionElements: NodeListOf<HTMLHeadingElement> =
    document.querySelectorAll('[id^="accordion-nested-collapse-heading-"]');
  const sectionElement: NodeListOf<HTMLHeadingElement> =
    document.querySelectorAll('[id^="section-heading-"]');

  collectionElements.forEach((item, index) => {
    item.addEventListener('contextmenu', (event: any) => {
      event.preventDefault();
      if (event.currentTarget.id.startsWith('accordion-collapse-heading-')) {
        collectionDropDownArray[index].show();
      }
    });
  });
  subCollectionElements.forEach((item, index) => {
    item.addEventListener('contextmenu', (event: any) => {
      event.preventDefault();
      if (
        event.currentTarget.id.startsWith('accordion-nested-collapse-heading-')
      ) {
        subCollectionDropDownArray[index].show();
      }
    });
  });
  sectionElement.forEach((item, index) => {
    item.addEventListener('contextmenu', (event: any) => {
      event.preventDefault();
      if (event.currentTarget.id.startsWith('section-heading-')) {
        sectionDropDownArray[index].show();
      }
    });
  });
}
