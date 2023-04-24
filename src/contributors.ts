import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';

const searchAndShowResults = async (
  userSearchBtn: any,
  userSearchbar: any,
  searchResultsTbody: any,
  trExample: any,
) => {
  searchResultsTbody.innerHTML = '';

  const searchQuery = userSearchbar.value
  if (!searchQuery.length) {
    return;
  }
  const res = await fetch('/user/search?q=' + searchQuery);
  const json = await res.json();

  json.users.forEach((user: any) => {
    let clone = trExample.cloneNode(true);

    const selectUserBtn = clone.querySelector('.select-user-btn');
    selectUserBtn.setAttribute('data-user-id', user.id);
    selectUserBtn.addEventListener('click', (e: any) => {
      console.log('e', e.target);
      userSearchBtn.setAttribute('disabled', true);
      userSearchbar.setAttribute('disabled', true);
    });

    const usernameTh = clone.querySelector('.username-th');
    usernameTh.innerHTML = user.username;

    clone.classList.remove('hidden');
    searchResultsTbody.appendChild(clone);
  });
  return undefined;
};

export function initContributors() {
  const searchBtn: HTMLButtonElement = document.querySelector('#search-btn');
  const userSearchbar: HTMLInputElement = document.querySelector('#username');

  const searchResultsTbody = document.querySelector('#search-results-tbody');
  const trExample: HTMLTableRowElement = document.querySelector('#tr-example');

  searchBtn.addEventListener('click', async e => {
    await searchAndShowResults(
      searchBtn,
      userSearchbar
      searchResultsTbody,
      trExample,
    );
  });
}
