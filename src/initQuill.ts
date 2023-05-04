const Quill = require('./quill');

export function initQuill() {
  var toolbarOptions = [
    ['bold', 'italic', 'underline'],
    [{list: 'ordered'}, {list: 'bullet'}],
    [{header: [1, 2, 3, 4, 5, 6, false]}],
    [{indent: '-1'}, {indent: '+1'}],
    ['clean'],
  ];
  const editorElement = document.querySelector('#editor');
  if (editorElement) {
    var quill = new Quill('#editor', {
      theme: 'snow',
      modules: {
        toolbar: toolbarOptions,
      },
    });
  }
}
