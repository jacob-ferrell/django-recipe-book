const addToFavoritesButtons = document.querySelectorAll('.favorite-heart');
addToFavoritesButtons.forEach(button => button.addEventListener('click', addToFavorites))

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

const url = window.location.href;
if (url.includes('my-recipes')) {
    document.getElementById('my-recipes-link').classList.add('active')
} else if (url.includes('my-favorites')) {
    document.getElementById('my-favorites-link').classList.add('active')
} else {
    document.getElementById('home-link').classList.add('active')
}

function addToFavorites(e) {
    e.preventDefault()
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    console.log(e.target.dataset)
    fetch('/add-to-favorites/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({...e.target.dataset})
    })
    .then(res => console.log(res))
}