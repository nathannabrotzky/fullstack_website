document.addEventListener("DOMContentLoaded", function () {
  fetch("/shop/cart/count/")
    .then(response => response.json())
    .then(data => {
      updateCartCount(data.count);
    })
    .catch(error => {
      console.error("Failed to load cart count:", error);
    });
});

function updateCartCount(count) {
  const cartCount = document.getElementById("cart-count");
  if (cartCount && count > 0) {
    cartCount.textContent = count;
    cartCount.className.remove("hidden");
  }
  if (cartCount && count === 0) {
    cartCount.textContent = "";
    cartCount.className.add("hidden");
  }
}