export function copyLink() {
  const btns = document.querySelectorAll('#copyLinkButton');
  if (btns) {
    btns.forEach(btn =>
      btn.addEventListener('click', () => {
        const copiedLink = btn.getAttribute('data-link');
        const el = document.createElement(`textarea`);
        let text = window.location.host;
        el.value = `${text}${copiedLink}`;
        el.setAttribute(`readonly`, ``);
        el.style.position = `absolute`;
        el.style.left = `-9999px`;
        document.body.appendChild(el);
        el.select();
        document.execCommand(`copy`);
        document.body.removeChild(el);
      }),
    );
  }
}
