import './styles.css';
import {initBooks} from './books';
import {initContributors} from './contributors';
import {initWallet} from './wallet';
import {initQuill} from './initQuill';
import {initQuillValueToInput} from './quillValueToInput';

document.addEventListener('DOMContentLoaded', () => {
  initBooks();
  initContributors();
  initQuill();
  initQuillValueToInput();
  initWallet();
});
