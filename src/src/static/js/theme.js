const themeToggleButton = document.getElementById('theme');
const body = document.body;

const currentTheme = localStorage.getItem('theme') || 'dark';
body.classList.add(`${currentTheme}-mode`);

themeToggleButton.addEventListener('click', () => {
  if (body.classList.contains('light-mode')) {
    body.classList.remove('light-mode');
    body.classList.add('dark-mode');
    localStorage.setItem('theme', 'dark');
  } else {
    body.classList.remove('dark-mode');
    body.classList.add('light-mode');
    localStorage.setItem('theme', 'light');
  }
});