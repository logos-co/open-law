export function initComments() {
  // deleting comment
  const deleteCommentBtn: HTMLButtonElement = document.querySelector(
    '#delete_comment_btn',
  );
  const deleteCommentInputOnModal: HTMLInputElement =
    document.querySelector('#comment_id');
  if (deleteCommentBtn && deleteCommentInputOnModal) {
    deleteCommentBtn.addEventListener('click', () => {
      const id = deleteCommentBtn.getAttribute('data-comment-id');
      console.log(id);
      deleteCommentInputOnModal.value = id;
    });
  }
}
