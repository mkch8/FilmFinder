document.addEventListener('DOMContentLoaded', function () {
    const moodForm = document.getElementById('mood-form');
    const recommendButton = document.getElementById('recommend-button');
    const radioButtons = document.querySelectorAll('input[name="mood"]');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            recommendButton.disabled = false;
        });
    });
});
