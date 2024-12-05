document.addEventListener('DOMContentLoaded', () => {
    const themeToggleCheckbox = document.getElementById('toggle-style');
    const themeLink = document.getElementById('theme-style');

    let savedTheme = localStorage.getItem('theme');
    if (!savedTheme) {
        savedTheme = '/static/style/style.css';
    }

    themeLink.setAttribute('href', savedTheme);

    if (savedTheme === '/static/style/style_sombre.css') {
        themeToggleCheckbox.checked = true;
    } else {
        themeToggleCheckbox.checked = false;
    }

    themeToggleCheckbox.addEventListener('change', () => {
        const newTheme = themeToggleCheckbox.checked
            ? '/static/style/style_sombre.css'
            : '/static/style/style.css';

        themeLink.setAttribute('href', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});
