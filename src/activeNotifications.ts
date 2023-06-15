export function activeNotifications() {
  const notificationButton = document.querySelector(
    '#dropdownNotificationButton',
  );
  if (notificationButton) {
    notificationButton.addEventListener('click', () => {
      console.log('CLICK');
    });
  }
}
