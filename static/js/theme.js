/**
 * Theme Toggle Functionality
 * Handles light/dark mode switching with localStorage persistence
 */

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = isDark ? '☀️ Light' : '🌙 Dark';
}

// Load saved theme on page load
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.body.classList.add('dark-mode');
        const btn = document.querySelector('.theme-toggle');
        if (btn) btn.textContent = '☀️ Light';
    }
}

// Initialize theme as soon as script loads
initTheme();

