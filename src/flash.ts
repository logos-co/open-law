import {Dismiss} from 'flowbite';
import type {DismissOptions, DismissInterface} from 'flowbite';

export function flash() {
  // target element that will be dismissed
  const $targetEl: HTMLElement = document.querySelector('[id^=toast-]');

  // optional trigger element
  const $triggerEl: HTMLElement = document.querySelector('#closeToastBtn');

  // options object
  const options: DismissOptions = {
    transition: 'transition-opacity',
    duration: 1000,
    timing: 'ease-out',
  };

  /*
   * targetEl: required
   * triggerEl: optional
   * options: optional
   */
  const dismiss: DismissInterface = new Dismiss($targetEl, $triggerEl, options);

  if ($targetEl && $triggerEl) {
    $triggerEl.addEventListener('click', () => {
      dismiss.hide();
    });
    setTimeout(() => {
      dismiss.hide();
    }, 5000);
  }
}
