document
  .getElementById("signupForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("https://hof-r7pv.onrender.com/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();
      localStorage.setItem("username",data.user);
      localStorage.setItem("token",data.token);
      localStorage.setItem('email', data.email);

      // Redirect to profile page after successful signup
      window.location.href = "./profile.html"; // Assuming profile.html is your profile page
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("error").innerText =
        "Error occurred. Please try again.";
    }
  });
