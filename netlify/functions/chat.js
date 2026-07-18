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

        // --- THE FIX: Bulletproof System Prompt Injection ---
        // Google rejects the standalone "systemInstruction" field. We intercept and inject it directly.
        if (body.systemInstruction) {
            const sysPrompt = body.systemInstruction.parts[0].text;
            if (body.contents && body.contents.length > 0) {
                const originalText = body.contents[0].parts[0].text;
                // Stitch the rulebook seamlessly into the first message
                body.contents[0].parts[0].text = `[System Directive: ${sysPrompt}]\n\nUser Message: ${originalText}`;
            }
            // Delete the field that trips the breaker
            delete body.systemInstruction; 
        }

        // Connecting to the highly stable gemini-1.5-flash model
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
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
