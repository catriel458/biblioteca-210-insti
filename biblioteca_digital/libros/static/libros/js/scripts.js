function toggleSearchInput() {
    const searchInput = document.getElementById('searchInput');
    searchInput.classList.toggle('active');
    searchInput.focus();
}

function searchBooks() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('bookList');
    const li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        const strong = li[i].getElementsByTagName('strong')[0];
        const spans = li[i].getElementsByClassName('book-details');
        const textContent = strong.textContent.toLowerCase() + Array.from(spans).map(span => span.textContent.toLowerCase()).join(' ');

        if (textContent.indexOf(filter) > -1) {
            li[i].style.display = '';
        } else {
            li[i].style.display = 'none';
        }
    }
}
