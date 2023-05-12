const starClickEventListener = async (btn: Element, totalStars: Element) => {
  const bookId = btn.getAttribute('data-book-id');

  const requestUrl = '/star/' + bookId;
  const response = await fetch(requestUrl, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const json = await response.json();
  const currentUserStar = json.current_user_star;
  const starsCount = json.stars_count;

  totalStars.innerHTML = starsCount;

  btn.classList.remove('fill-yellow-300');
  if (currentUserStar) {
    btn.classList.add('fill-yellow-300');
  } else {
    btn.classList.remove('fill-yellow-300');
  }
};

export function initStar() {
  const bookStarsBlocks = document.querySelectorAll('.book-star-block');

  bookStarsBlocks.forEach(bookStarsBlock => {
    const bookStarBtn = bookStarsBlock.querySelector('.star-btn');
    const totalStarsDiv = bookStarsBlock.querySelector('.total-stars');

    bookStarBtn.addEventListener('click', () => {
      starClickEventListener(bookStarBtn, totalStarsDiv);
    });
  });
}
