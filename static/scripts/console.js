const refreshToken = async() => {
    const responseRaw = await fetch(`${window.location.origin}/api/auth/refreshToken/`, {
        headers: {
            "content-type": "application/json; charset=UTF-8 "
        },
        body: JSON.stringify({}),
        method: "POST"
    });
    const responseJson = await responseRaw.json();
    if (responseJson.isValid === false) {
        console.error(`Error validating token: ${responseJson.error}`)
    }
}


const addUser = async() => {
    const name = document.getElementById("nameField").value;
    const email = document.getElementById("emailField").value;
    if (!name || !email) {
        console.error("Missing required field (username or name)");
    }
    // Make request to FE, to add user
    const responseRaw = await fetch(`${window.location.origin}/api/database/insertEmail/`, {
        headers: {
            "content-type": "application/json; charset=UTF-8 "
        },
        body: JSON.stringify({
            email: email,
            nameOfUser: name
        }),
        method: "PUT"
    });
    const responseJson = await responseRaw.json();
    if (!responseJson.email) {
        console.debug("Error validating token, trying to refresh this token ...");
        refreshToken();
        return addUser();
    }
    console.debug("Email added");
}