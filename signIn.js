document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('https://hof-r7pv.onrender.com/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
     
      if (response.ok) {
        const data = await response.json();
        const token = data.token;

        // Store token in localStorage
        localStorage.setItem('token', data.token);
        localStorage.setItem('username', data.user);
        localStorage.setItem('email', data.email);

        // Redirect to profile page after successful login
        window.location.href = '/profile.html'; // Assuming profile.html is your profile page
      } else {
        // Handle failed login (e.g., display error message)
        console.error('Login failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
      document.getElementById('error').innerText = 'Error occurred. Please try again.';
    }
  });