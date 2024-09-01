document.addEventListener('DOMContentLoaded', function () {
    const submitCvForm = document.getElementById('submitCvForm');
    const verifyCvForm = document.getElementById('verifyCvForm');
    const checkStatusForm = document.getElementById('checkStatusForm');

    if (submitCvForm) {
        submitCvForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const element = document.getElementById('element').value;

            const response = await fetch('/submit_cv', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, element })
            });

            const result = await response.json();
            document.getElementById('response').innerText = result.message + ' Transaction Hash: ' + result.tx_hash;
        });
    }

    if (verifyCvForm) {
        verifyCvForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const element = document.getElementById('element').value;
            const verified = document.getElementById('verified').value === 'true';

            const response = await fetch('/verify_cv', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, element, verified })
            });

            const result = await response.json();
            document.getElementById('response').innerText = result.message + ' Transaction Hash: ' + result.tx_hash;
        });
    }

    if (checkStatusForm) {
        checkStatusForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const element = document.getElementById('element').value;

            const response = await fetch('/check_status?name=' + encodeURIComponent(name) + '&element=' + encodeURIComponent(element));
            const result = await response.json();
            document.getElementById('response').innerText = 'Status: ' + (result.status ? 'Verified' : 'Not Verified');
        });
    }
});
