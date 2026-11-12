document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  if (!form) return;

  const checkbox = form.querySelector('input[type="checkbox"][name="consent"]');
  const submit = form.querySelector('#submit-appeal');

  if (!checkbox || !submit) return;

  const sync = () => {
    submit.disabled = !checkbox.checked;
  };

  checkbox.addEventListener('change', sync);
  sync();
});