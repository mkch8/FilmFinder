document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');
    const searchForm = document.getElementById('search-form');

    searchInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length >= 1) {
            fetch(`/search?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = '';
                    if (data.length > 0) {
                        resultsContainer.style.display = 'block';
                        data.forEach(movie => {
                            const resultItem = document.createElement('div');
                            resultItem.classList.add('result-item');
                            resultItem.textContent = movie.title;
                            resultItem.addEventListener('click', () => {
                                window.location.href = `/film/${movie.id}`;
                            });
                            resultsContainer.appendChild(resultItem);
                        });
                    } else {
                        resultsContainer.style.display = 'none';
                    }
                });
        } else {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
        }
    });

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const query = searchInput.value;
        if (query.length >= 1) {
            fetch(`/search?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = '';
                    if (data.length > 0) {
                        resultsContainer.style.display = 'block';
                        data.forEach(movie => {
                            const resultItem = document.createElement('div');
                            resultItem.classList.add('result-item');
                            resultItem.textContent = movie.title;
                            resultItem.addEventListener('click', () => {
                                window.location.href = `/film/${movie.id}`;
                            });
                            resultsContainer.appendChild(resultItem);
                        });
                    } else {
                        resultsContainer.style.display = 'none';
                    }
                });
        }
    });
});
