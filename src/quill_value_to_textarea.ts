const quill_value_to_textarea = (): undefined => {
  const aboutInput: HTMLButtonElement = document.querySelector('#about');
  const qlEditor: HTMLButtonElement = document.querySelector('.ql-editor');
  const editorContent = qlEditor.innerHTML;
  aboutInput.value = editorContent;

  console.log(editorContent);

  return undefined;
};

export function initQuill() {
  const qlEditor: HTMLButtonElement = document.querySelector('.ql-editor');

  if (!qlEditor) {
    return;
  }

  qlEditor.addEventListener('DOMSubtreeModified', async e => {
    quill_value_to_textarea();
  });
}
