export function initComments() {
  // deleting comment
  const deleteCommentBtns: NodeListOf<HTMLButtonElement> =
    document.querySelectorAll('#delete_comment_btn');
  const deleteCommentInputOnModal: HTMLInputElement =
    document.querySelector('#comment_id');
  if (deleteCommentBtns && deleteCommentInputOnModal) {
    deleteCommentBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-comment-id');
        deleteCommentInputOnModal.value = id;
      }),
    );
  }
  // edit comment
  const editCommentBtns: NodeListOf<HTMLButtonElement> =
    document.querySelectorAll('#edit_comment_btn');
  const editCommentInputOnModal: HTMLInputElement =
    document.querySelector('#edit_comment_id');
  const editCommentTextInputOnModal: HTMLInputElement = document.querySelector(
    '#edit-comment-text-input',
  );
  const editCommentTextQuillOnModal: HTMLInputElement =
    document.querySelector('#edit-comment-text');

  if (
    editCommentBtns &&
    editCommentInputOnModal &&
    editCommentTextInputOnModal
  ) {
    editCommentBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-edit-comment-id');
        const text = btn.getAttribute('data-edit-comment-text');
        console.log('text', text);
        editCommentInputOnModal.value = id;
        editCommentTextInputOnModal.value = text;
        editCommentTextQuillOnModal.innerHTML = text;
      }),
    );
  }
}
