async function login() {

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    const response = await fetch("/api/login/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email,
            password: password
        })

    });

    const data = await response.json();

    if (response.ok) {

        sessionStorage.setItem(
            "email",
            email
        );

        window.location = "/otp-page/";

    } else {
         
		 alert(data.detail || JSON.stringify(data));
		 
    }

}

async function verifyOtp() {

    const email =
        sessionStorage.getItem("email");

    const otp =
        document.getElementById("otp").value;

    const response =
        await fetch("/api/verify-otp/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                email: email,
                otp: otp

            })

        });

    const data = await response.json();

    if (response.ok) {

        sessionStorage.setItem(
            "access",
            data.tokens.access
        );

        sessionStorage.setItem(
            "refresh",
            data.tokens.refresh
        );

        sessionStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );

        window.location = "/dashboard-page/";
    } else {

        alert(JSON.stringify(data));
    }

}

async function loadDashboard() {

	const response = await fetch("/api/dashboard/", {
		
        method: "GET",
		
        credentials: "same-origin"
    });

    const data = await response.json();

    if (!response.ok) {

        alert("Session expired.");

        sessionStorage.clear();

        window.location = "/";

        return;

    }

    document.getElementById("userInfo").innerHTML = `

    <h3>Welcome ${data.user.name}</h3>

    <p><strong>Email:</strong> ${data.user.email}</p>

    <p><strong>Username:</strong> ${data.user.username}</p>

    <p><strong>Provider:</strong> ${data.user.auth_provider}</p>

    `;
	
	console.log("Access Token:");
    console.log(sessionStorage.getItem("access"));
}

async function logout() {

    await fetch("/api/logout/", {
        method: "POST"
    });

    sessionStorage.clear();

    window.location = "/";
}

    if (window.location.pathname === "/dashboard-page/") {

        loadDashboard();

    }