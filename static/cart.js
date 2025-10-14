document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get("userID") || localStorage.getItem("userID");

  if (!userId) {
    alert("User not logged in!");
    return;
  }

  document.getElementById("shopLink").href = `/shop?userID=${userId}`;

  async function loadCart() {
    const res = await fetch(`/api/cart/${userId}`);
    const data = await res.json();

    const items = data.items || [];
    const total = data.total || 0;

    const container = document.getElementById("cart");
    container.innerHTML = "";

    items.forEach(item => {
      const div = document.createElement("div");
      div.innerHTML = `
        <strong>${item.productName}</strong> x ${item.quantity} = ${item.price * item.quantity} RON
        <button onclick="addToCart(${item.prodID})">+</button>
        <button onclick="decreaseFromCart(${item.prodID})">-</button>
      `;
      container.appendChild(div);
    });

    document.getElementById("total").textContent = `Total: ${total} RON`;
  }

  async function addToCart(prodID) {
    const res = await fetch(`/api/cart/${userId}/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prodID: prodID, quantity: 1 })
    });

    const data = await res.json();
    if (res.ok) {
      loadCart();
    } else {
      alert(data.message || "Error adding product");
    }
  }

  async function decreaseFromCart(prodID) {
    const res = await fetch(`/api/cart/${userId}/decrease`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prodID: prodID })
    });

    const data = await res.json();
    if (res.ok) {
      loadCart();
    } else {
      alert(data.message || "Error updating product");
    }
  }

  document.getElementById("checkoutBtn").addEventListener("click", async () => {
    const res = await fetch(`/api/cart/${userId}/checkout`, { method: "POST" });
    const data = await res.json();

    if (res.ok) {
      loadCart();
      alert(`Checkout successful! Total: ${data.total} RON`);
    } else {
      alert(data.message || "Checkout failed!");
    }
  });

  window.addToCart = addToCart;
  window.decreaseFromCart = decreaseFromCart;

  loadCart();
});
