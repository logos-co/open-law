import './styles.css';
import {initBooks} from './books';
import {initContributors} from './contributors';
import {initWallet} from './wallet';

document.addEventListener('DOMContentLoaded', () => {
  initBooks();
  initContributors();
  initWallet();
});
