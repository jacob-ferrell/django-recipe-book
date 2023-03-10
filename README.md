# CookBook

CookBook is a recipe book website which allows users to create, share, and discover recipes.

### Technologies Used
- HTML

- CSS

- Javascript

- Django Python

- PostgreSQL Database

### Resource Links

- The site utilizes the Edamam Recipe API for discovering and searching for new recipes.  https://developer.edamam.com/edamam-recipe-api

- CookBook's UI is derived from a template provided by Dennis Ivy, from this github repo: https://github.com/divanov11/StudyBud

### Project Goals

- The purpose of this project was to learn Django and explore its capabilities.  To force myself to learn Django's way of doing things, I purposely used as little Javascript as possible to create the site.  It is also for these reasons that I avoided using a front-end framework, such as React, which I am already accustomed to.

### Limitations

- Due to using the free tier of the Edamam Recipe API, which limits user's to a maximum of 8 calls a minute, rapid reloads or searches might cause the API to stop responding.  It is also for this reason that the 'My Favorites' page does not render the thumbnail image of each recipe, as this would require an individual API call for each recipe and could instantly exceed the limit.  Image URL's provided by the Edamam API also eventually expire, so saving that URL is not an option.

- As mentioned previously, this site was a learning excercise for Django Python and was intentionally designed to use as little Javascript as possible.  For these reasons, doing things such as adding ingredients/instructions to a custom recipe might feel a bit unconventional.  A full-stack project which better showcases my front-end skills can be found at this github repo: https://github.com/jacob-ferrell/bug-tracker and is hosted here: https://bug-tracker-rcf6.onrender.com/

- The Edamam Recipe API does not provide preparation instructions for its recipes, so the Recipe Details page will have a link user's can click to get this information, along with nutritional data.

### Features

- The home page displays a list of random recipes from the Edamam Recipe API (If the search field is blank).

- Users can type a query into the search bar to generate a new list of recipes from the Edamam Recipe API which match the search

- The user can create a personal account with basic information such as first name, last name, username and password

- If logged in, the user can create their own recipe by providing a recipe name, description, ingredients, and preparation instructions.

- The user can view all recipes they have created by clicking the 'My Recipes' link in the sidebar

- The user can view more information about a recipe from the Edamam API by clicking on the title.  From here, they can add or remove the recipe from 'My Favorites', allowing them to reference the recipe at a later time

- All favorited recipes can be viewed by clicking the 'My Favorites' link in the sidebar

- The most recent recipes created by other CookBook users will be displayed on the right of the home page under 'Recent Recipes'.  This will display the creator of the recipe, recipe title, and recipe description.  Clicking the recipe's title will allow the user to view the ingredients and preparation instruction.




