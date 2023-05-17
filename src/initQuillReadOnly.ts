export function initQuillReadOnly() {
  const readonlyQls = document.querySelectorAll('.ql-editor-readonly');

  readonlyQls.forEach(el => {
    const ql = el.querySelector('.ql-editor');
    if (ql) {
      ql.removeAttribute('contenteditable');

      ql.classList.remove('ql-editor');
      ql.classList.add('ql-editor-readonly');
    }

    const qlTooltip = el.querySelector('.ql-tooltip');
    if (qlTooltip) {
      qlTooltip.remove();
    }

    const qlClipboard = el.querySelector('.ql-clipboard');
    if (qlClipboard) {
      qlClipboard.remove();
    }
  });
}
