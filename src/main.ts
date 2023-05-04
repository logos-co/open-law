import './styles.css';
import {initBooks} from './books';
import {initContributors} from './contributors';
import {initQuill} from './quill_value_to_textarea';

document.addEventListener('DOMContentLoaded', () => {
  initBooks();
  initContributors();
  initQuill();
});
