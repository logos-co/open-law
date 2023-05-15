const Quill = require('./quill');

export function initQuill() {
  var icons = Quill.import('ui/icons');
  console.log(icons['header']);
  // prettier-ignore
  icons.header['false'] = '<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000"viewBox="-8 -7 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3z"/></svg>';
  icons.header[1] = `<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000" viewBox="-5 -7 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3zm9.52.779H10V3h3.36v7h-1.84V4.779z"/></svg>`;
  icons.header[2] = `<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000" viewBox="-4.5 -7 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3zm12.88 4.352V10H10V8.986l.1-.246 1.785-1.913c.43-.435.793-.77.923-1.011.124-.23.182-.427.182-.587 0-.14-.04-.242-.127-.327a.469.469 0 0 0-.351-.127.443.443 0 0 0-.355.158c-.105.117-.165.288-.173.525l-.012.338h-1.824l.016-.366c.034-.735.272-1.33.718-1.77.446-.44 1.02-.66 1.703-.66.424 0 .805.091 1.14.275.336.186.606.455.806.8.198.343.3.7.3 1.063 0 .416-.23.849-.456 1.307-.222.45-.534.876-1.064 1.555l-.116.123-.254.229h1.938z"/></svg>`;
  icons.header[3] = `<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000" viewBox="-4.5 -6.5 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3zm12.453 2.513l.043.055c.254.334.38.728.38 1.172 0 .637-.239 1.187-.707 1.628-.466.439-1.06.658-1.763.658-.671 0-1.235-.209-1.671-.627-.436-.418-.673-.983-.713-1.676L10 7.353h1.803l.047.295c.038.238.112.397.215.49.1.091.23.137.402.137a.566.566 0 0 0 .422-.159.5.5 0 0 0 .158-.38c0-.163-.067-.295-.224-.419-.17-.134-.438-.21-.815-.215l-.345-.004v-1.17l.345-.004c.377-.004.646-.08.815-.215.157-.124.224-.255.224-.418a.5.5 0 0 0-.158-.381.566.566 0 0 0-.422-.159.568.568 0 0 0-.402.138c-.103.092-.177.251-.215.489l-.047.295H10l.022-.37c.04-.693.277-1.258.713-1.675.436-.419 1-.628 1.67-.628.704 0 1.298.22 1.764.658.468.441.708.991.708 1.629a1.892 1.892 0 0 1-.424 1.226z"/></svg>`;
  icons.header[4] = `<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000" viewBox="-4.5 -7 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3zm10.636 4.74H10V7.302l.06-.198 2.714-4.11h1.687v3.952h.538V8.74h-.538V10h-1.825V8.74zm.154-1.283V5.774l-1.1 1.683h1.1z"/></svg>`;
  icons.header[5] = `<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000" viewBox="-4 -6.5 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3zm8.003 4.317h2.68c.386 0 .699-.287.699-.642 0-.355-.313-.642-.698-.642H10.01l.002-.244L10 3h5.086v1.888h-3.144l.014.617h1.114c1.355 0 2.469.984 2.523 2.23.052 1.21-.972 2.231-2.288 2.28l-.095.001-3.21-.02V8.73l.003-.414z"/></svg>`;
  icons.header[6] = `<svg style="scale: 1.6;" xmlns="http://www.w3.org/2000/svg" fill="#000000" viewBox="-4.5 -7 24 24" preserveAspectRatio="xMinYMin"><path d="M2 4h4V1a1 1 0 1 1 2 0v8a1 1 0 1 1-2 0V6H2v3a1 1 0 1 1-2 0V1a1 1 0 1 1 2 0v3zm11.949 2.057c.43.44.651.999.651 1.64 0 .629-.228 1.18-.67 1.62-.442.437-.99.663-1.613.663a2.212 2.212 0 0 1-1.649-.693c-.43-.45-.652-.985-.652-1.58 0-.224.034-.449.1-.672.063-.211.664-1.627.837-1.966.251-.491.65-1.204 1.197-2.137l1.78.652-.917 1.88c.249.113.733.386.936.593zm-1.63.765a.85.85 0 0 0-.858.863.85.85 0 0 0 .252.613.865.865 0 0 0 1.48-.614.844.844 0 0 0-.25-.611.866.866 0 0 0-.623-.251z"/></svg>`;

  var toolbarOptions = [
    ['bold', 'italic', 'underline'],
    [{list: 'ordered'}, {list: 'bullet'}],
    [{indent: '-1'}, {indent: '+1'}],
    ['clean'],
    [
      {header: false},
      {header: 1},
      {header: 2},
      {header: 3},
      {header: 4},
      {header: 5},
      {header: 6},
    ],
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
