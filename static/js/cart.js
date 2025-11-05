function refreshCart() {
  fetch("/shop/cart/fragment/")
    .then(response => response.json())
    .then(data => {
      console.log("Cart HTML:", data.html); // ✅ Inspect output
      const cartPreview = document.querySelector(".cart-preview");
      if (cartPreview) {
        cartPreview.innerHTML = data.html;
        updateCartCount(data.count); 
        attachRemoveListeners();
        setupCheckoutModals();
      } else {
        console.warn("No .cart-preview element found");
      }
    });
}


function attachAddListeners() {
  document.querySelectorAll(".add-to-cart-form").forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(form);
      fetch(form.action, {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        body: formData
      }).then(() => refreshCart());
    });
  });
}

function attachRemoveListeners() {
  document.querySelectorAll(".remove-from-cart-form").forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(form);
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      fetch(form.action, {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": csrfToken
 },
        body: formData
      }).then(() => refreshCart());
    });
  });
}

function setupCheckoutModals() {
  const checkoutModal = document.getElementById("checkout-modal");
  const confirmationModal = document.getElementById("confirmation-modal");
  const checkoutForm = document.getElementById("checkout-form");

  const openCheckout = document.querySelector(".view-cart-button");
  if (openCheckout) {
    openCheckout.addEventListener("click", () => {
      checkoutModal.classList.remove("hidden");
    });
  }

  document.querySelectorAll(".close-button").forEach(btn => {
    btn.addEventListener("click", () => {
      checkoutModal.classList.add("hidden");
      confirmationModal.classList.add("hidden");
    });
  });

  if (checkoutForm) {
    checkoutForm.addEventListener("submit", function (e) {
      e.preventDefault();
      checkoutModal.classList.add("hidden");
      confirmationModal.classList.remove("hidden");
      // Optionally clear cart or send data to server here
    });
  }
}

function setupStripeCheckout() {
  const stripe = Stripe("pk_live_51SKOpp2Uggs4joMAO5XDxpwt6dbpwjpWxBD5UDm5nD0M4YIhy73B7hOm5kyz3EPxMJ2rLGzP3CmIdvNN0ZfPni8Q00Qk6tDkt6");

document.getElementById("checkout-form").addEventListener("submit", function (e) {
  e.preventDefault();

  fetch("/shop/create-checkout-session/", {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" }
  })
    .then(res => res.json())
    .then(data => {
      console.log("Stripe session ID:", data.id);
      if (data.id) {
        stripe.redirectToCheckout({ sessionId: data.id });
      } else {
        alert("Payment failed: " + data.error);
      }
    });
});

}

function updateCartCount(count) {
  const cartCount = document.getElementById("cart-count");
  if (cartCount) {
    cartCount.textContent = count;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  attachAddListeners();
  attachRemoveListeners();
  setupCheckoutModals();
  setupStripeCheckout();
});


