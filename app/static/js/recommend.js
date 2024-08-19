document.addEventListener('DOMContentLoaded', function () {
    const moodForm = document.getElementById('mood-form');
    const recommendButton = document.getElementById('recommend-button');
    const radioButtons = document.querySelectorAll('input[name="mood"]');
    const loaderWrapper = document.querySelector('.loader-wrapper');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            recommendButton.disabled = false;
        });
    });

    moodForm.addEventListener('submit', function (event) {
        loaderWrapper.style.display = 'flex'; // Show the loader
    });
});
