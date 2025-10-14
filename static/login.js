document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try{
            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({username, password})
            });

            const data = await response.json();

            if(response.ok){
                localStorage.setItem("userID", data.userID);
                window.location.href = `/shop?userID=${data.userID}`;
            }else{
                alert(data.message || "Login failed");
            }
        }catch (err){
            console.error("Error: ", err);
            alert("Something went wrong. Try again later");
        }
    });
});