document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('fake_b');

    button.style.transition = 'left 0.4s ease, top 0.4s ease'; // transition

    function moveButton() {
        const offset = 50;
        const buttonRect = button.getBoundingClientRect();
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        let newX, newY;

        //bouton bordure droite
        if (buttonRect.left < offset) { // gauche
            newX = windowWidth;
        } else if (buttonRect.right > windowWidth - offset) { // droite
            newX = -buttonRect.width;
        } else {
            // aléatoire
            newX = Math.random() * (windowWidth - buttonRect.width);
        }

        // bouton bordure haut/bas
        if (buttonRect.top < offset) { // haut
            newY = windowHeight;
        } else if (buttonRect.bottom > windowHeight - offset) { // bas
            newY = -buttonRect.height;
        } else {
            // aléatoire
            newY = Math.random() * (windowHeight - buttonRect.height);
        }

        button.style.position = 'absolute';
        button.style.left = newX + 'px';
        button.style.top = newY + 'px';
    }

    // Déplace bouton quand souris se rapproche
    document.addEventListener('mousemove', function (event) {
        const buttonRect = button.getBoundingClientRect();
        const buttonCenterX = buttonRect.left + buttonRect.width / 2;
        const buttonCenterY = buttonRect.top + buttonRect.height / 2;

        // Calcule distance souris bouton
        const distance = Math.sqrt(Math.pow(event.clientX - buttonCenterX, 2) + Math.pow(event.clientY - buttonCenterY, 2));

        if (distance < 150) {
            moveButton();
        }
    });

    document.getElementById('fake_b').addEventListener('click', function() {
    window.location.href = 'https://www.youtube.com/watch?v=xvFZjo5PgG0';
});
});
