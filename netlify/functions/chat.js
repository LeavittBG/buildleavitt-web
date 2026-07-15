

exports.handler = async function(event, context) {
    // 1. Ensure it's a POST request
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    try {
        // 2. Parse the incoming message from the frontend
        const body = JSON.parse(event.body);
        
        // 3. Grab the API key securely from the Netlify Vault
        const API_KEY = process.env.GEMINI_API_KEY;

        if (!API_KEY) {
            console.error("API Key is missing from Environment Variables");
            return { statusCode: 500, body: "Server configuration error." };
        }

        // 4. Send the request to Google Gemini
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        // 5. Check if Google rejected it (e.g., a 401 Unauthorized error)
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Google API Error: ${response.status} - ${errorText}`);
            return { statusCode: response.status, body: `Google API Error: ${response.status}` };
        }

        // 6. Return Google's response back to the frontend chat window
        const data = await response.json();
        return {
            statusCode: 200,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        };

    } catch (error) {
        console.error("Serverless Function Error:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: "Internal Server Error" })
        };
    }
};
