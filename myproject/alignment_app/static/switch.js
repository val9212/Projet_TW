document.addEventListener('DOMContentLoaded', () => {
    const themeToggleCheckbox = document.getElementById('toggle-style');
    const themeLink = document.getElementById('theme-style');

    // Récupérer le thème sauvegardé
    let savedTheme = localStorage.getItem('theme');
    if (!savedTheme) {
        savedTheme = '/static/style/style.css';  // Par défaut, mode clair
    }

    // Appliquer le thème sauvegardé
    themeLink.setAttribute('href', savedTheme);

    // Mettre à jour l'état du switch en fonction du thème
    if (savedTheme === '/static/style/style_sombre.css') {
        themeToggleCheckbox.checked = true;
    } else {
        themeToggleCheckbox.checked = false;
    }

    // Ajouter l'événement change pour le switch
    themeToggleCheckbox.addEventListener('change', () => {
        const newTheme = themeToggleCheckbox.checked
            ? '/static/style/style_sombre.css'
            : '/static/style/style.css';

        themeLink.setAttribute('href', newTheme);
        // Sauvegarder le nouveau thème dans localStorage
        localStorage.setItem('theme', newTheme);
    });
});
