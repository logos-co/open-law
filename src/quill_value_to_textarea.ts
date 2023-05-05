const quill_value_to_textarea = (): undefined => {
  const aboutInput: HTMLInputElement = document.querySelector('#about');
  const qlEditor: HTMLElement = document.querySelector('.ql-editor');
  const editorContent = qlEditor.innerHTML;
  aboutInput.value = editorContent;
  return undefined;
};
const quill_interpretation_to_textarea = (): undefined => {
  const interpretationTextInput: HTMLInputElement = document.querySelector(
    '#interpretation-text',
  );
  const qlInterpretationEditor: HTMLElement = document.querySelector(
    '#interpretation-editor',
  );
  const editorContent = qlInterpretationEditor.innerHTML;
  console.log('editorContent', editorContent);
  interpretationTextInput.value = editorContent;
  return undefined;
};

export function initQuillValueToTextArea() {
  const qlEditor: HTMLElement = document.querySelector('.ql-editor');

  if (qlEditor) {
    qlEditor.addEventListener('DOMSubtreeModified', () => {
      quill_value_to_textarea();
    });
  }

  //
  const qlInterpretationEditor: HTMLElement = document.querySelector(
    '#interpretation-editor',
  );

  if (qlInterpretationEditor) {
    qlInterpretationEditor.addEventListener('DOMSubtreeModified', () => {
      quill_interpretation_to_textarea();
    });
  }
}
