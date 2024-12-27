document.addEventListener('DOMContentLoaded', () => {
    const themeToggleCheckbox = document.getElementById('toggle-style');
    const themeLink = document.getElementById('theme-style');

    let savedTheme = localStorage.getItem('theme');
    if (!savedTheme) {
        savedTheme = themeCSS.light;
    }

    themeLink.setAttribute('href', savedTheme);

    themeToggleCheckbox.checked = (savedTheme === themeCSS.dark);

    themeToggleCheckbox.addEventListener('change', () => {
        const newTheme = themeToggleCheckbox.checked ? themeCSS.dark : themeCSS.light;

        themeLink.setAttribute('href', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});