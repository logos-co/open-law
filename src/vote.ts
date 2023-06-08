const REQUEST_URLS: {[key: string]: string} = {
  interpretation: '/vote/interpretation/',
  comment: '/vote/comment/',
};

const voteClickEventListener = async (
  btn: Element,
  voteCountElement: Element,
  setStrokeToVoteBtns: (positive: boolean | null) => void,
) => {
  const voteFor = btn.getAttribute('data-vote-for');

  if (!(voteFor in REQUEST_URLS)) {
    console.error('Unknown data-vote-for attribute');
    return;
  }

  const positive = btn.getAttribute('data-positive');
  const entityId = btn.getAttribute('data-entity-id');
  const requestUrl = REQUEST_URLS[voteFor] + entityId;
  const response = await fetch(requestUrl, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({positive: positive}),
  });

  const json = await response.json();
  const voteCount = json.vote_count;
  voteCountElement.innerHTML = json.vote_count;

  voteCountElement.classList.remove('text-red-500');
  voteCountElement.classList.remove('text-green-500');
  if (voteCount > 0) {
    voteCountElement.classList.add('text-green-500');
  } else if (voteCount < 0) {
    voteCountElement.classList.add('text-red-500');
  }

  const currentUserVote = json.current_user_vote;
  setStrokeToVoteBtns(currentUserVote);
};

export function initVote() {
  const voteBlocks = document.querySelectorAll('.vote-block');
  voteBlocks.forEach(voteBlock => {
    const voteCountElement = voteBlock.querySelector('.vote-count');
    const voteBtns = voteBlock.querySelectorAll('.vote-button');

    const setStrokeToVoteBtns = (positive: boolean | null) => {
      voteBtns.forEach(btn => {
        const svg = btn.querySelector('svg');
        const dataPositive = btn.getAttribute('data-positive');
        svg.classList.remove('stroke-red-500');
        svg.classList.remove('stroke-green-500');

        if (dataPositive == `${positive}` && positive == true) {
          svg.classList.add('stroke-green-500');
        } else if (dataPositive == `${positive}` && positive == false) {
          svg.classList.add('stroke-red-500');
        }
      });
    };

    voteBtns.forEach(btn => {
      btn.addEventListener('click', e => {
        voteClickEventListener(btn, voteCountElement, setStrokeToVoteBtns);
      });
    });
  });
}
