// Upload and comparison handling for Variant Alert!

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    const comparisonTypeSelect = document.getElementById('comparison_type');
    const outputFormatGroup = document.getElementById('output-format-group');
    const outputFormatSelect = document.getElementById('output_format');
    const vcfWarning = document.getElementById('vcf-warning');

    // Show/hide output format based on comparison type
    comparisonTypeSelect.addEventListener('change', function() {
        if (this.value === 'compare-variant') {
            outputFormatGroup.style.display = 'block';
        } else {
            outputFormatGroup.style.display = 'none';
        }
    });

    // Show warning for VCF output format
    outputFormatSelect.addEventListener('change', function() {
        if (this.value === 'vcf') {
            vcfWarning.style.display = 'block';
        } else {
            vcfWarning.style.display = 'none';
        }
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate files
        const sourceFile = document.getElementById('source_vcf').files[0];
        const targetFile = document.getElementById('target_vcf').files[0];

        if (!sourceFile || !targetFile) {
            showAlert('Please select both source and target VCF files', 'error');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        btnText.textContent = 'Processing...';
        btnSpinner.style.display = 'inline-block';
        resultsSection.style.display = 'none';

        // Prepare form data
        const formData = new FormData(uploadForm);

        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showResults(data);
                showAlert('Comparison completed successfully!', 'success');
            } else {
                showAlert(data.error || 'An error occurred during comparison', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('Network error: ' + error.message, 'error');
        } finally {
            // Reset button state
            submitBtn.disabled = false;
            btnText.textContent = 'Start Comparison';
            btnSpinner.style.display = 'none';
        }
    });

    function showResults(data) {
        resultsSection.style.display = 'block';
        
        let html = `
            <div class="alert alert-success">
                <strong>✓ Comparison completed successfully!</strong><br>
                Genome reference: ${data.genome_reference || 'N/A'}<br>
                Session ID: ${data.session_id}
            </div>
        `;

        if (data.result_files && data.result_files.length > 0) {
            html += `
                <h4>Download Results:</h4>
                <ul class="results-list">
            `;

            data.result_files.forEach(file => {
                html += `
                    <li class="result-item">
                        <span><strong>📄 ${file.name}</strong></span>
                        <a href="${file.url}" class="download-link" download>⬇ Download</a>
                    </li>
                `;
            });

            html += '</ul>';
        } else {
            html += '<p>No result files were generated.</p>';
        }

        resultsContent.innerHTML = html;

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `<strong>${type === 'success' ? '✓' : '✗'}</strong> ${message}`;

        // Insert at the top of the form
        uploadForm.parentElement.insertBefore(alertDiv, uploadForm);

        // Remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
});
