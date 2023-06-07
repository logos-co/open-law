export function indeterminateInputs() {
  const indeterminatedInputs = document.querySelectorAll(
    'input[indeterminate=true]',
  );

  indeterminatedInputs.forEach((element: HTMLInputElement) => {
    element.indeterminate = true;
  });
}
