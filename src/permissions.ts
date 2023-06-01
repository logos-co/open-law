export const initPermissions = () => {
  const editBtns = document.querySelectorAll('.edit-permissions-btn');

  editBtns.forEach(element => {
    const bookIdInput: HTMLInputElement = document.querySelector(
      '#permission_modal_book_id',
    );
    const userIdInput: HTMLInputElement = document.querySelector(
      '#permission_modal_user_id',
    );
    element.addEventListener('click', () => {
      const book_id = element.getAttribute('data-book-id');
      const user_id = element.getAttribute('data-user-id');

      bookIdInput.value = book_id;
      userIdInput.value = user_id;
    });
  });
};
