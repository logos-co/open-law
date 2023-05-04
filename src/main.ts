import './styles.css';
import {initBooks} from './books';
import {initContributors} from './contributors';
import {initWallet} from './wallet';
import {initQuill} from './initQuill';
import {initQuillValueToTextArea} from './quill_value_to_textarea';

document.addEventListener('DOMContentLoaded', () => {
  initBooks();
  initContributors();
  initQuill();
  initQuillValueToTextArea();
  initWallet();
});
