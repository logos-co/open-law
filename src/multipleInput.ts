export function initMultipleInput() {
  const settingsForm = document.querySelector('.settings-form');
  settingsForm.addEventListener('keypress', (e: any) => {
    if (e.keyCode === 13) {
      e.preventDefault();
    }
  });

  const tagsToSubmitInput: HTMLInputElement =
    document.querySelector('.tags-to-submit');
  const multipleInput: any = document.querySelector('.multiple-input');

  const wordsBlock: HTMLDivElement = multipleInput.parentElement.querySelector(
    '.multiple-input-items',
  );
  const wordDivs = wordsBlock.querySelectorAll('.multiple-input-word');
  const addedWords: string[] = [];
  wordDivs.forEach(el => {
    addedWords.push(el.innerHTML);
  });

  tagsToSubmitInput.value = addedWords.join();

  multipleInput.addEventListener('keyup', (event: any) => {
    if (event.keyCode === 13 || event.keyCode === 188) {
      if (!multipleInput.value) {
        return;
      }

      let inputValue = multipleInput.value.trim();
      inputValue =
        inputValue.charAt(0).toUpperCase() + inputValue.substr(1).toLowerCase();
      if (
        inputValue.substring(inputValue.length - 1, inputValue.length) == ','
      ) {
        inputValue = inputValue.substring(0, inputValue.length - 1);
        event.target.value = inputValue;
      }

      if (addedWords.includes(inputValue)) {
        return;
      }

      const wordDiv = document.createElement('div');
      wordDiv.className =
        'multiple-input-word bg-sky-500 rounded text-center py-1/2 px-2';
      wordDiv.innerHTML = inputValue;
      addedWords.push(inputValue);

      wordsBlock.appendChild(wordDiv);
      multipleInput.value = '';
      tagsToSubmitInput.value = addedWords.join();
    } else if (event.keyCode === 8 && multipleInput.value.length === 0) {
      const addedWordsDivs = document.querySelectorAll('.multiple-input-word');
      const lastAdded = addedWordsDivs[addedWordsDivs.length - 1];
      if (!lastAdded) {
        return;
      }
      const word = lastAdded.innerHTML;
      if (word || word != '') {
        multipleInput.value = word;
        lastAdded.remove();

        addedWords.slice(0, addedWords.length - 1);
        tagsToSubmitInput.value = addedWords.join();
      }
    }
  });
}
