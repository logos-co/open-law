const refreshAccessLevelTree = async (userId: string, bookId: string) => {
  const urlParams = new URLSearchParams({
    user_id: userId,
    book_id: bookId,
  });
  const res = await fetch('/permission/access_tree?' + urlParams);
  const json = await res.json();

  Object.entries(json.access_tree).map(([key, ids]: [string, number[]]) => {
    const checkboxes = document.querySelectorAll(
      `input[type=checkbox][data-access-to=${key}]`,
    );

    checkboxes.forEach((element: HTMLInputElement) => {
      const id = parseInt(element.getAttribute('data-access-to-id'));
      if (ids.includes(id)) {
        element.checked = true;
      }
    });
  });
};

export function initRefreshAccessLevelTree() {
  const editPermissionsBtns = document.querySelectorAll(
    '.edit-permissions-btn',
  );

  editPermissionsBtns.forEach(element => {
    const userId = element.getAttribute('data-user-id');
    const bookId = element.getAttribute('data-book-id');
    element.addEventListener('click', () => {
      refreshAccessLevelTree(userId, bookId);
    });
  });
}
