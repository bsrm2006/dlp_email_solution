document.addEventListener('DOMContentLoaded', function() {
    // Email scanning form submission
    const scanForm = document.getElementById('email-scan-form');
    if (scanForm) {
        scanForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(scanForm);
            
            fetch('/scan_email', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('scan-result');
                
                if (data.status === 'PASS') {
                    resultDiv.innerHTML = `
                        <div class="alert alert-success">
                            <strong>Email Safe:</strong> No DLP violations detected.
                        </div>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>DLP Violation Detected!</strong>
                            <p>Violations: ${JSON.stringify(data.content_violations)}</p>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Exception management
    const exceptionForm = document.getElementById('exception-form');
    if (exceptionForm) {
        exceptionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(exceptionForm);
            
            fetch('/exceptions', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/';
                } else {
                    throw new Error('Exception addition failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});