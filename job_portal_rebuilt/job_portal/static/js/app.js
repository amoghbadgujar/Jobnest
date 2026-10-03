document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-save-url]').forEach((button) => {
    button.addEventListener('click', async () => {
      const url = button.dataset.saveUrl;
      const original = button.innerHTML;
      button.disabled = true;
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
          }
        });
        const data = await response.json();
        button.classList.toggle('saved', data.saved);
        const compact = button.closest('.detail-actions');
        button.innerHTML = data.saved
          ? (compact ? '♥ Saved' : '♥')
          : (compact ? '♡ Save Job' : '♡');
      } catch (error) {
        button.innerHTML = original;
        alert('Could not update saved jobs. Please try again.');
      } finally {
        button.disabled = false;
      }
    });
  });

  document.querySelectorAll('input[type="file"]').forEach((input) => {
    input.addEventListener('change', () => {
      const file = input.files?.[0];
      if (file && file.size > 5 * 1024 * 1024) {
        alert('Please choose a file smaller than 5 MB.');
        input.value = '';
      }
    });
  });
});

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^|; )' + name.replace(/([.$?*|{}()\[\]\\/+^])/g, '\\$1') + '=([^;]*)'));
  return match ? decodeURIComponent(match[2]) : '';
}
