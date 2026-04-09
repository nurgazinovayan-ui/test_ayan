const toggleBtn = document.getElementById('themeToggle');
const rootBody = document.body;

const preferredTheme = localStorage.getItem('theme');
if (preferredTheme === 'light') {
  rootBody.classList.add('light');
  toggleBtn.textContent = '☀';
}

toggleBtn.addEventListener('click', () => {
  rootBody.classList.toggle('light');
  const isLight = rootBody.classList.contains('light');
  toggleBtn.textContent = isLight ? '☀' : '☾';
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});
