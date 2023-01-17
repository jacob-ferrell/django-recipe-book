const addToFavoritesButtons = document.querySelectorAll('.favorite-heart');
addToFavoritesButtons.forEach(button => button.addEventListener('click', addToFavorites))
console.log('hello')
function addToFavorites(e) {
    e.preventDefault()
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    console.log(e.target.dataset.recipe)
    fetch('/add-to-favorites/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({recipe: e.target.dataset.recipe})
    })
    .then(res => console.log(res))
}