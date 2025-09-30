document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
  // Apply saved theme on load
  if(!localStorage.getItem('theme')) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      } else if(localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('dark');
      }

  themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    
    // Save preference
    localStorage.setItem(
      'theme',
      document.documentElement.classList.contains('dark') ? 'dark' : 'light'
    );

    // Small spin effect
    const icon = themeToggle.querySelector("i:not(.hidden)");
    if (icon) {
      icon.classList.add("rotate-180");
      setTimeout(() => icon.classList.remove("rotate-180"), 500);
    }
  });
});