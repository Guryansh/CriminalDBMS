// Select relevant HTML elements
const filterButtons = document.querySelectorAll("#filter-buttons button");
const filterableCards = document.querySelectorAll("#filterable-cards .card");

// Function to filter cards based on filter buttons
const filterCards = (e) => {
    document.querySelector("#filter-buttons .active").classList.remove("active");
    e.target.classList.add("active");
    filterableCards.forEach(card => {
        const categoriesString = card.dataset.categories;

        // Split the string into an array using ',' as the delimiter
        const categories = categoriesString.split(' ');
        console.log(categories)
        // show the card if it matches the clicked filter or show all cards if "all" filter is clicked
        if (card.dataset.name === e.target.dataset.filter || e.target.dataset.filter === "all" || categories.includes(e.target.dataset.filter)) {
            return card.classList.replace("hide", "show");
        }
        card.classList.add("hide");
    });
}

filterButtons.forEach(button => button.addEventListener("click", filterCards));

const button = document.querySelector('button.btn.mb-2.mx-1[data-filter="result"]');

// Check if the button is found
if (button) {
    // Trigger a click event on the button
    button.click();
} else {
    console.error('Button not found');
}