const recipeSearch = `https://api.spoonacular.com/recipes/complexSearch?query=` //GET request to search menu items

let searchButton = document.querySelector('#search')

//search button and value
if (searchButton !== null) {
searchButton.addEventListener("click", function(){
    let searchTerm = document.getElementById("searchTerm").value;
    getData(searchTerm);
  })
}

//sends request with value from search term
async function getData(searchTerm) {
    let response = await axios.get(`${recipeSearch}${searchTerm}&number=24&${API_KEY}`);
    let data = await response.data;
    useApiData(data)
}

//appends results to recipe area
function useApiData(data) {
  $('#recipes').empty();
  if (data.results.length == 0) {
    $('#recipes').append(`No recipes found`)
  }
  data.results.forEach(function(result) {
    $('#recipes').append(`
    <div class="card rounded" style="max-width: 18rem;">
    <img class="card-img-top" src="${result.image}" alt="Card image cap">
    <div class="card-body">
      <h5 class="card-title">
    <form method="POST" action="/recipes/${result.id}/fav" class="justify-content-center">
      <button class="btn btn-sm {{'btn-primary' if ${result.id} in recipes else 'btn-secondary'}}">
      <i class="far fa-heart"></i> 
      <input type="hidden" name="recipe_name" value="${result.title}">
      </button>
    </form>
    <a href="/recipes/${result.id}" id="show_recipe">${result.title}</a> </h5>
      <p class="card-text"></p>
    </div>`)
  })

}



