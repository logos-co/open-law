// Default SortableJS
import Sortable from 'sortablejs';

export function initDnD() {
  const divsForSectionsDnD: NodeListOf<HTMLDivElement> =
    document.querySelectorAll('#draggableSectionItems');
  const divsForSubCollectionsDnD: NodeListOf<HTMLDivElement> =
    document.querySelectorAll('[data-dnd="dnd-sub-collection"]');
  const divsAreEmpty = document.querySelectorAll('#empty-dnd-entity');
  divsForSectionsDnD.forEach((div: HTMLDivElement) =>
    Sortable.create(div, {
      group: {
        name: 'sections',
        pull: true,
        put: ['sections'],
      },
      animation: 100,
      filter: '.filter',
      onEnd: async function (/**Event*/ evt) {
        var itemEl = evt.item; // dragged HTMLElement
        const bookId = itemEl.getAttribute('data-book-id');
        const sectionId = itemEl.getAttribute('data-entity-id');
        if (bookId && sectionId) {
          const requestUrl = `/book/${bookId}/${sectionId}/section/change_position`;
          const response = await fetch(requestUrl, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              position: evt.newDraggableIndex,
              collection_id: evt.to.getAttribute('data-entity-id'),
            }),
          });
          if (response.status === 200) {
            window.location.reload();
          } else {
            return;
          }
        }
      },
    }),
  );
  divsForSubCollectionsDnD.forEach((div: HTMLDivElement) =>
    Sortable.create(div, {
      group: {
        name: 'sub_collections',
        pull: true,
        put: ['sub_collections'],
      },
      animation: 100,
      filter: '.filter',
      onEnd: async function (/**Event*/ evt) {
        var itemEl = evt.item; // dragged HTMLElement
        const bookId = itemEl.getAttribute('data-book-id');
        const collectionId = itemEl.getAttribute('data-entity-id');
        if (bookId && collectionId) {
          const requestUrl = `/book/${bookId}/${collectionId}/collection/change_position`;
          const response = await fetch(requestUrl, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              position: evt.newDraggableIndex,
              collection_id: evt.to.getAttribute('data-entity-id'),
            }),
          });
          if (response.status === 200) {
            window.location.reload();
          } else {
            return;
          }
        }
      },
    }),
  );
  divsAreEmpty.forEach((div: HTMLDivElement) =>
    Sortable.create(div, {
      group: {
        name: 'empty',
        pull: false,
        put: ['sub_collections', 'sections'],
      },
      animation: 100,
      fallbackOnBody: true,
      swapThreshold: 20,
      filter: '.filter',
    }),
  );
}
