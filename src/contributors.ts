const searchAndShowResults = async (
  userSearchbar: any,
  searchResultsTbody: any,
  trExample: any,
  userIdInput: any,
): Promise<undefined> => {
  searchResultsTbody.innerHTML = '';

  const bookId = userSearchbar.getAttribute('data-book-id');
  const searchQuery = userSearchbar.value;
  if (!searchQuery.length) {
    return;
  }

  const urlParams = new URLSearchParams({
    q: searchQuery,
    book_id: bookId,
  });
  const res = await fetch('/user/search?' + urlParams);
  const json = await res.json();

  json.users.forEach((user: any) => {
    let clone = trExample.cloneNode(true);

    const selectUserBtn = clone.querySelector('.select-user-btn');
    selectUserBtn.setAttribute('data-user-id', user.id);
    selectUserBtn.addEventListener('click', (e: any) => {
      const allSelectBtns = document.querySelectorAll('.select-user-btn');
      allSelectBtns.forEach(btn => {
        btn.innerHTML = 'Select';
      });

      const userId = e.target.getAttribute('data-user-id');
      userIdInput.value = userId;

      selectUserBtn.innerHTML = 'Selected';
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
  const userIdInput: HTMLInputElement = document.querySelector('#user_id');

  if (!searchBtn && !userSearchbar && !userIdInput) {
    return;
  }

  const searchResultsTbody = document.querySelector('#search-results-tbody');
  const trExample: HTMLTableRowElement = document.querySelector('#tr-example');

  searchBtn.addEventListener('click', async e => {
    e.preventDefault();
    userIdInput.value = '';
    await searchAndShowResults(
      userSearchbar,
      searchResultsTbody,
      trExample,
      userIdInput,
    );
  });
}
