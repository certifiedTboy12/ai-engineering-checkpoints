/**
 * Array of products
 */
const products = [
  {
    id: 1,
    name: "Shoes",
    price: 100,
    description: "A pair of shoe",
    image: "./assets/shoe.png",
    quantity: 0,
    liked: false,
  },

  {
    id: 2,
    name: "Socks",
    price: 20,
    description: "This is a socks",
    image: "./assets/socks.png",
    quantity: 0,
    liked: false,
  },

  {
    id: 3,
    name: "Bag",
    price: 50,
    description: "This is a bag",
    image: "./assets/bag.png",
    quantity: 0,
    liked: false,
  },
];

// select the main container holding all the cart items
let productContainer = document.querySelector(".list-products");
let totalPrice = document.querySelector(".total");

/**
 * @function renderCartItems
 * @description a function that renders all the products on the screen
 */
function renderCartItems() {
  // empty the product container before updating the ui to avoid duplicate items
  productContainer.innerHTML = "";

  totalPrice.textContent = products.reduce(
    (total, product) => total + product.price * product.quantity,
    0,
  );

  // iterate over each item of the arr using the for of loop
  for (let product of products) {
    const cartContainer = document.createElement("div");
    cartContainer.setAttribute("class", "card-body");
    cartContainer.innerHTML = `<div class="card" style="width: 18rem">
              <img src=${product?.image} class="card-img-top" alt=${product?.name} />
              <div class="card-body">
                <h5 class="card-title">${product?.name}</h5>
                <p class="card-text">${product?.description}</p>
                <h4 class="unit-price">${product?.price} $</h4>
                <div>
                  <i class="fas fa-plus-circle" data-id=${product?.id}></i>
                  <span class="quantity">${product?.quantity}</span>
                  <i class="fas fa-minus-circle" data-id=${product?.id}></i>
                </div>
                <div>
                  <i class="fas fa-trash-alt" data-id=${product?.id}></i>
                  <i class="fas fa-heart ${product.liked ? "liked" : ""}" data-id=${product?.id}></i>
                </div>
              </div>
            </div>`;

    // append all the cartContainer created as a child to the main product container
    productContainer.appendChild(cartContainer);
  }
}

// call the renderCartItems function on window load
window.onload = () => {
  renderCartItems();
};

// Use event delegation to handle clicks on icons
productContainer.addEventListener("click", (event) => {
  const target = event.target;
  const productId = Number(target.dataset.id); // Convert product ID to a number

  // Exit the function if the clicked element doesn't have a product ID
  if (!productId) {
    return;
  }

  // Find the product in the array
  const product = products.find((p) => p.id === productId);

  // Check which icon was clicked using its class
  if (target.classList.contains("fa-plus-circle")) {
    // Increase product quantity
    product.quantity++;
  } else if (target.classList.contains("fa-minus-circle")) {
    // Decrease product quantity, but not below 0
    if (product.quantity > 0) {
      product.quantity--;
    }
  } else if (target.classList.contains("fa-trash-alt")) {
    // Find the index of the product to remove
    const productIndex = products.findIndex((p) => p.id === productId);
    // Remove the product from the array
    if (productIndex > -1) {
      products.splice(productIndex, 1);
    }
  } else if (target.classList.contains("fa-heart")) {
    // Toggle the liked status in the data
    product.liked = !product.liked;
  }

  // After any action, re-render the cart to show the updated state
  renderCartItems();
});
