let currentUserId = null; // va fi setat după register

document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (res.ok) {
    const data = await res.json();
    localStorage.setItem("userID", data.userID);
    // redirecționează către shop cu userID în query string
    window.location.href = `/after_register/${data.userID}`;
  } else {
    alert("Error registering user");
  }
});
