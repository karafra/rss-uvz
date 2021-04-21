let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1dnotcnNzLmF1dGgiLCJzdWIiOiJtdG90aDU3NUBnbWFpbC5jb20iLCJpYXQiOjE2MTkwMzcyNjEuNjgzOTgzMywiZXhwIjoxNjE5MDM3NTYxLjY4Mzk4MzMsImxvZ2dlZEluQXMiOiJtdG90aDU3NUBnbWFpbC5jb20ifQ.GZqWHe2tVDC6AVeSHPR2Z4SL5dklSyehsbnbShZRR4I";

const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}


const fixUpToken = () => {
    get
}


const addUser = () => {
    const name = document.getElementById("nameField").value;
    const email = document.getElementById("emailField").value;
    if (!name || !email) {
        console.error("Missing required field (username or name)")
    }
    fetch(`${window.location.origin}/api/database/insertEmail/`, {
        headers: {
            "content-type": "application/json; charset=UTF-8 "
        },
        body: JSON.stringify({
            token: token,
            email: email,
            nameOfUser: name
        }),
        method: "PUT"
    }).then(res =>
        res.json().then(
            res => console.log(res)
        )
    );
}