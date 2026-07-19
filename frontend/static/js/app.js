async function login() {

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;

    const response = await fetch("api/auth/login/", {

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
        await fetch("/api/auth/verify-otp/", {

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

	const response = await fetch("/api/auth/dashboard/", {
		
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

<h3>🎉 Welcome ${data.user.name}</h3>

<h4>Email</h4>

<p>${data.user.email}</p>

<h4>Provider</h4>

<p>${data.user.auth_provider}</p>

`;
	
	console.log("Access Token:");
    console.log(sessionStorage.getItem("access"));
}

async function logout() {

    try {

        await fetch("/api/auth/logout/", {
            method: "POST",
            credentials: "include"
        });

    } finally {

        sessionStorage.clear();

        window.location = "/";
    }
}

    if (window.location.pathname === "/dashboard-page/") {

        loadDashboard();

    }