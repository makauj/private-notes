//create a script that calls the remoteok api and saves the data in a json file using javascript
const https = require('https');
const fs = require('fs');

const url = 'https://remoteok.com/api';

function callApi(url) {
    https.get(url, (resp) => {
        let data = '';

        // A chunk of data has been received.
        resp.on('data', (chunk) => {
            data += chunk;
        });
        
        // The whole response has been received. Print out the result.
        resp.on('end', () => {
            try {
                const parsed = JSON.parse(data);
                const formattedData = JSON.stringify(parsed, null, 2);
                fs.writeFile("../data/raw_jobs_json.json", formattedData, (err) => {
                    if (err) throw err;
                    console.log('Data has been saved!');
                });
            } catch (e) {
                console.error("JSON parse error:", err.message);
                console.error("Raw response:", data.slice(0, 500));
            }
        });

    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });
}

// Call the function
callApi(url);
