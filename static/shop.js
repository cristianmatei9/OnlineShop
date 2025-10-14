document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get("userID") || localStorage.getItem("userID");

  if (!userId) {
    alert("User not logged in!");
    return;
  }

  document.getElementById("cartLink").href = `/cart?userID=${userId}`;

  async function loadProducts() {
    const res = await fetch("/api/products");
    const products = await res.json();

    const container = document.getElementById("products");
    container.innerHTML = "";

    products.forEach(p => {
      const div = document.createElement("div");
      div.innerHTML = `
        <strong>${p.name}</strong> - ${p.price} RON
        <button onclick="addToCart(${p.id})">Add to Cart</button>
      `;
      container.appendChild(div);
    });
  }

  async function addToCart(prodID) {
    if (!userId) {
      alert("User not logged in!");
      return;
    }

    const res = await fetch(`/api/cart/${userId}/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prodID: prodID, quantity: 1 })
    });

    const data = await res.json();
    if (res.ok) {
      alert("Product added to cart!");
    } else {
      alert(data.message || "Error adding product to cart");
    }
  }

  window.addToCart = addToCart;
  loadProducts();
});
