import './styles.css';
import {initBooks} from './books';
import {initContributors} from './contributors';

document.addEventListener('DOMContentLoaded', event => {
  initBooks();
  initContributors();
});
