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
        return responseJson;
    }
    console.debug("Tokens refresed ...")
}


const removeEmailFromDOM = (el) => {
    var element = el;
    el.previousElementSibling.parentNode.remove();
    element.remove();
}

const getMailFromElement = (element) => {
    const emailText = element.previousElementSibling.innerHTML;
    return emailText.match(/\((.*?)\)/)[1]
}

const removeEmail = async(element) => {
    const email = getMailFromElement(element);
    const responseRaw = await fetch(`${window.location.origin}/api/database/deleteEmail/`, {
        headers: {
            "content-type": "application/json; charset=UTF-8 "
        },
        body: JSON.stringify({
            email: email
        }),
        method: "DELETE"
    });
    const responseJson = await responseRaw.json();
    if (responseJson.Error && responseJson.Error.includes("Token")) {
        console.log(responseJson)
        console.debug("Error validating token, trying to refresh this token ...");
        await refreshToken();
        return removeEmail(element);
    }
    removeEmailFromDOM(element);
    console.debug("Email removed");
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
    if (responseJson.Error) {
        console.debug(responseJson.Error);
        const refreshTokenResponse = await refreshToken();
        if (refreshTokenResponse) {
            console.error("Refresh token expired");
            return;
        }
        return await addUser();
    }
    document.getElementById("email-list").insertAdjacentHTML("beforeend",
        `
        <li class="email-address">
            <p>${name} (${email})</p>
            <a onclick="removeEmail(this)">
                <i class="far fa-trash-alt"></i>
            </a>
        </li>
    `);
    console.debug("Email added");
}