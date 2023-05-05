const quill_value_to_textarea = (): undefined => {
  const aboutInput: HTMLButtonElement = document.querySelector('#about');
  const qlEditor: HTMLButtonElement = document.querySelector('.ql-editor');
  const editorContent = qlEditor.innerHTML;
  aboutInput.value = editorContent;
  return undefined;
};
const quill_interpretation_to_textarea = (): undefined => {
  const interpretationTextInput: HTMLButtonElement = document.querySelector(
    '#interpretation-text',
  );
  const qlInterpretationEditor: HTMLButtonElement = document.querySelector(
    '.ql-interpretation-editor',
  );
  const editorContent = qlInterpretationEditor.innerHTML;
  interpretationTextInput.value = editorContent;
  return undefined;
};

export function initQuillValueToTextArea() {
  const qlEditor: HTMLButtonElement = document.querySelector('.ql-editor');

  if (qlEditor) {
    qlEditor.addEventListener('DOMSubtreeModified', async e => {
      quill_value_to_textarea();
    });
  }

  //
  const qlInterpretationEditor: HTMLButtonElement = document.querySelector(
    '.ql-interpretation-editor',
  );

  if (!qlInterpretationEditor) {
    qlInterpretationEditor.addEventListener('DOMSubtreeModified', async e => {
      quill_interpretation_to_textarea();
    });
  }
}
