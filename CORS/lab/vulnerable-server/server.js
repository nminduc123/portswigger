const express = require("express");
const session = require("express-session");
const mysql = require("mysql2/promise");
require("dotenv").config();

const app = express();

const PORT = process.env.PORT || 3000;

// ========================================
// MySQL
// ========================================

const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    connectionLimit: 10
});

// ========================================
// Middleware
// ========================================

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(
    session({
        secret: "cors-null-origin-lab-secret",

        resave: false,

        saveUninitialized: false,

        cookie: {
            httpOnly: true,

            // Giữ lax để localhost:3000 và localhost:4000
            // vẫn có thể dùng session trong lab.
            sameSite: "lax",

            secure: false
        }
    })
);

// ========================================
// VULNERABLE CORS
// ========================================

const allowedOrigins = [
    "http://localhost:4000",

    // CỐ TÌNH SAI
    "null"
];

app.use((req, res, next) => {

    const origin = req.headers.origin;

    console.log(
        `[CORS] ${req.method} ${req.path} | Origin=${origin}`
    );

    if (allowedOrigins.includes(origin)) {

        res.setHeader(
            "Access-Control-Allow-Origin",
            origin
        );

        res.setHeader(
            "Access-Control-Allow-Credentials",
            "true"
        );
    }

    next();
});

// ========================================
// Home
// ========================================

app.get("/", (req, res) => {

    res.send(`
<!DOCTYPE html>

<html>

<head>
    <title>CORS Lab</title>
</head>

<body>

<h1>Vulnerable CORS Lab</h1>

${
    req.session.userId
        ? `
            <p>You are logged in.</p>

            <a href="/account">
                View account
            </a>

            <br><br>

            <a href="/logout">
                Logout
            </a>
          `
        : `
            <a href="/login">
                Login
            </a>
          `
}

</body>

</html>
    `);
});

// ========================================
// Login page
// ========================================

app.get("/login", (req, res) => {

    res.send(`
<!DOCTYPE html>

<html>

<head>
    <title>Login</title>
</head>

<body>

<h1>Login</h1>

<form method="POST" action="/login">

    <label>
        Username:
    </label>

    <input
        type="text"
        name="username"
        required
    >

    <br><br>

    <label>
        Password:
    </label>

    <input
        type="password"
        name="password"
        required
    >

    <br><br>

    <button type="submit">
        Login
    </button>

</form>

</body>

</html>
    `);
});

// ========================================
// Login
// ========================================

app.post("/login", async (req, res) => {

    const {
        username,
        password
    } = req.body;

    try {

        const [rows] = await db.execute(
            `
            SELECT
                id,
                username
            FROM users
            WHERE username = ?
              AND password = ?
            `,
            [
                username,
                password
            ]
        );

        if (rows.length === 0) {

            return res.status(401).send(`
                <h1>Login failed</h1>

                <p>
                    Invalid username or password.
                </p>

                <a href="/login">
                    Back
                </a>
            `);
        }

        const user = rows[0];

        req.session.userId = user.id;

        console.log(
            `[LOGIN] ${user.username} logged in`
        );

        res.redirect("/account");

    } catch (error) {

        console.error(error);

        res.status(500).send(
            "Database error"
        );
    }
});

// ========================================
// Account page
// ========================================

app.get("/account", async (req, res) => {

    if (!req.session.userId) {

        return res.redirect("/login");
    }

    try {

        const [rows] = await db.execute(
            `
            SELECT
                username,
                email,
                api_key
            FROM users
            WHERE id = ?
            `,
            [
                req.session.userId
            ]
        );

        if (rows.length === 0) {

            return res.status(404).send(
                "User not found"
            );
        }

        const user = rows[0];

        res.send(`
<!DOCTYPE html>

<html>

<head>
    <title>Account</title>
</head>

<body>

<h1>My Account</h1>

<p>
    Username:
    <strong>${user.username}</strong>
</p>

<p>
    Email:
    <strong>${user.email}</strong>
</p>

<p>
    API Key:
    <strong>${user.api_key}</strong>
</p>

<hr>

<a href="/api/accountDetails">
    Account API
</a>

<br><br>

<a href="/logout">
    Logout
</a>

</body>

</html>
        `);

    } catch (error) {

        console.error(error);

        res.status(500).send(
            "Database error"
        );
    }
});

// ========================================
// ACCOUNT API
//
// Đây là endpoint chứa dữ liệu nhạy cảm
// mà attacker muốn đọc.
// ========================================

app.get("/api/accountDetails", async (req, res) => {

    console.log(
        `[API] /api/accountDetails`
    );

    console.log(
        `[API] session userId = ${req.session.userId}`
    );

    if (!req.session.userId) {

        return res.status(401).json({
            error: "Not authenticated"
        });
    }

    try {

        const [rows] = await db.execute(
            `
            SELECT
                username,
                email,
                api_key
            FROM users
            WHERE id = ?
            `,
            [
                req.session.userId
            ]
        );

        if (rows.length === 0) {

            return res.status(404).json({
                error: "User not found"
            });
        }

        const user = rows[0];

        res.json({
            username: user.username,
            email: user.email,
            apiKey: user.api_key
        });

    } catch (error) {

        console.error(error);

        res.status(500).json({
            error: "Database error"
        });
    }
});

// ========================================
// Logout
// ========================================

app.get("/logout", (req, res) => {

    req.session.destroy(() => {

        res.redirect("/login");
    });
});

// ========================================
// Start
// ========================================

async function start() {

    try {

        const connection =
            await db.getConnection();

        console.log(
            "[+] MySQL connected"
        );

        connection.release();

        app.listen(PORT, () => {

            console.log(
                `[+] Vulnerable server:`
            );

            console.log(
                `    http://localhost:${PORT}`
            );

            console.log(
                `[+] CORS whitelist:`
            );

            console.log(
                `    http://localhost:4000`
            );

            console.log(
                `    null  <-- VULNERABLE`
            );
        });

    } catch (error) {

        console.error(
            "[-] MySQL connection failed"
        );

        console.error(
            error.message
        );
    }
}

start();