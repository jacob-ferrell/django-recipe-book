const addToFavoritesButtons = document.querySelectorAll(".favorite-heart");
addToFavoritesButtons.forEach((button) =>
  button.addEventListener("click", addToFavorites)
);

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

const url = window.location.href;
/* if (url.includes('my-recipes')) {
    document.getElementById('my-recipes-link').classList.add('active')
} else if (url.includes('my-favorites')) {
    document.getElementById('my-favorites-link').classList.add('active')
} else {
    document.getElementById('home-link').classList.add('active')
} */

async function addToFavorites(e) {
  const addLink = document.getElementById("add-to-favorites");

  e.preventDefault();
  const csrf_token = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const res = await fetch("/add-to-favorites/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    body: JSON.stringify({ ...e.target.dataset }),
  });
  const json = await res.json();
  console.log(json, e.target.dataset.favorite);
  if (json.status !== "success") return;
  if (json.added) {
    return (addLink.textContent = "Remove From Favorites");
  }
  addLink.textContent = "Add To Favorites";
}

function editItem(e) {
  const type = e.target.dataset.type;
  const id = e.target.dataset.id;
  const prev = e.target.dataset.prev;
  let parent = e.target.parentNode;
  parent.innerHTML = "";
  const inputField = document.createElement("input");
  inputField.value = prev;
  parent.appendChild(inputField);
  const submit = document.createElement("button");
  submit.textContent = "Submit";
  parent.appendChild(submit);

  submit.addEventListener("click", async (e) => {
    e.preventDefault();
    const csrf_token = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;
    const url = "/edit-item/";
    const newValue = inputField.value;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
      body: JSON.stringify({ text: inputField.value, type, pk: id }),
    });
    const json = await res.json();
    console.log(json.status)
    if (json.status !== "success") return;
    parent.innerHTML = `<li>${inputField.value}<button data-id="${id}" data-prev="${inputField.value}" data-type="${type}" onclick="editItem(event)">Edit</button><button data-type="${type}" data-id="${id}" onclick="deleteItem(event)">Delete</button></li>`;
  });
}

async function deleteItem(e) {
  e.preventDefault();
  const csrf_token = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const url = "/delete-item/";
  const type = e.target.dataset.type;
  const id = e.target.dataset.id;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    body: JSON.stringify({ type, pk: id }),
  });
  const json = await res.json()
  console.log(json)
  if (json.status != 'success') return;
  e.target.parentNode.remove();
}
