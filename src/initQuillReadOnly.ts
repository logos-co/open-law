export function initQuillReadOnly() {
  const readonlyQls = document.querySelectorAll('.ql-editor-readonly');

  readonlyQls.forEach(el => {
    const ql = el.querySelector('.ql-editor');
    if (ql) {
      ql.removeAttribute('contenteditable');
    }
  });
}
