const Quill = require('./quill');

export function initQuill() {
  var toolbarOptions = [
    ['bold', 'italic', 'underline'],
    [{list: 'ordered'}, {list: 'bullet'}],
    [{header: [1, 2, 3, 4, 5, 6, false]}],
    [{indent: '-1'}, {indent: '+1'}],
    ['clean'],
  ];
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
    new Quill('#' + quillElementId, {
      theme: 'snow',
      modules: {
        toolbar: toolbarOptions,
      },
    });
  });
}
