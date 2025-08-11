function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`.tab[onclick="showTab('${tabId}')"]`).classList.add('active');
}

// ✅ Login Handler
function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('login-email').value.trim().toLowerCase();
    const password = document.getElementById('login-password').value.trim();

    const storedUser = JSON.parse(localStorage.getItem(email));

    if (!email || !password) {
        alert('Please fill in all fields.');
        return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email.');
        return;
    }

    if (storedUser && storedUser.password === password) {
        alert('Login successful!');
    } else {
        alert('Invalid email or password. Please try again.');
    }
}

// ✅ Sign Up Handler with Password Strength Check
function handleSignup(event) {
    event.preventDefault();

    const name = document.getElementById('signup-name').value.trim();
    const email = document.getElementById('signup-email').value.trim().toLowerCase();
    const password = document.getElementById('signup-password').value;
    const age = document.getElementById('signup-age').value;
    const gender = document.getElementById('signup-gender').value;
    const mobile = document.getElementById('signup-mobile').value.replace(/\s/g, '');

    if (!name || !email || !password || !age || !gender || !mobile) {
        alert('Please fill in all fields.');
        return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email.');
        return;
    }

    if (!/^(\+8801[3-9]\d{8}|01[3-9]\d{8})$/.test(mobile)) {
        alert('Please enter a valid Bangladeshi mobile number (e.g., +8801XXXXXXXXX or 01XXXXXXXXX).');
        return;
    }

    // ✅ Password must include uppercase, lowercase, number, special character, min 8 chars
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    if (!passwordPattern.test(password)) {
        alert('Password must be at least 8 characters and include uppercase, lowercase, number, and special character.');
        return;
    }

    // ✅ Store user in localStorage (demo only – not secure for production)
    const userData = {
        name,
        email,
        password,
        age,
        gender,
        mobile
    };

    localStorage.setItem(email, JSON.stringify(userData));
    alert('Sign up successful! Now you can log in.');
    showTab('login');
}

document.addEventListener('DOMContentLoaded', () => {
    showTab('login');
    console.log("Auth Page Loaded - Ready for Login/Signup");
});
