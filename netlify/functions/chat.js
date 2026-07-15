exports.handler = async function(event, context) {
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    try {
        const body = JSON.parse(event.body);
        const API_KEY = process.env.GEMINI_API_KEY;

        if (!API_KEY) {
            console.error("API Key is missing from Environment Variables");
            return { statusCode: 500, body: JSON.stringify({ error: "Server configuration error." }) };
        }

        const headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, OPTION"
        };
        
        if (event.httpMethod === "OPTIONS") {
             return { statusCode: 200, headers, body: "OK" };
        }

        // Connecting to the highly stable gemini-1.5-flash model
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Google API Error: ${response.status} - ${errorText}`);
            return { 
                statusCode: response.status, 
                headers,
                body: JSON.stringify({ error: `Google API Error: ${response.status}` })
            };
        }

        const data = await response.json();
        return {
            statusCode: 200,
            headers: { 
                ...headers,
                "Content-Type": "application/json" 
            },
            body: JSON.stringify(data)
        };

    } catch (error) {
        console.error("Serverless Function Error:", error);
        return {
            statusCode: 500,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ error: "Internal Server Error", details: error.message })
        };
    }
};
