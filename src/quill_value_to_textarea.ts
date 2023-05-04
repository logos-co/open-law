const quill_value_to_textarea = (): undefined => {
  const aboutInput: HTMLButtonElement = document.querySelector('#about');
  const qlEditor: HTMLButtonElement = document.querySelector('.ql-editor');
  const editorContent = qlEditor.innerHTML;
  aboutInput.value = editorContent;
  return undefined;
};

export function initQuillValueToTextArea() {
  const qlEditor: HTMLButtonElement = document.querySelector('.ql-editor');

  if (!qlEditor) {
    return;
  }

  qlEditor.addEventListener('DOMSubtreeModified', async e => {
    quill_value_to_textarea();
  });
}
