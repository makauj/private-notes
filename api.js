//create a script that calls the remoteok api and saves the data in a json file using javascript
const https = require('https');
const fs = require('fs');

const url = 'https://remoteok.io/api';

function callApi(url) {
    https.get(url, (resp) => {
        let data = '';

        // A chunk of data has been received.
        resp.on('data', (chunk) => {
            data += chunk;
        });

        // The whole response has been received. Print out the result.
        resp.on('end', () => {
            fs.writeFile("data/raw_jobs_js.json", data, (err) => {
                if (err) throw err;
                console.log('Data has been saved!');
            });
        });

    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });
}

// Call the function
callApi(url);
