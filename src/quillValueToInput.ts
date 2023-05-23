const quillValueToInput = (quillElementId: string): undefined => {
  const inputElement: HTMLInputElement = document.querySelector(
    `#${quillElementId}-input`,
  );

  if (!inputElement) {
    return;
  }
  const qlEditor: HTMLElement = document.querySelector('#' + quillElementId);
  const editorContent = qlEditor.innerHTML;
  inputElement.value = editorContent;
  return undefined;
};

export function initQuillValueToInput() {
  const qlEditors: NodeListOf<HTMLElement> =
    document.querySelectorAll('.quill-editor');
  qlEditors.forEach(el => {
    const quillElementId = el.id;
    if (!quillElementId) {
      console.error(
        'Please set attribute id to element with class .quill-editor',
      );
      return;
    }
    el.addEventListener('DOMSubtreeModified', () => {
      quillValueToInput(quillElementId);
    });
  });
}
