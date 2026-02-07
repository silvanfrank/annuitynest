document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('annuity-form');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    const results = document.getElementById('results');
    const withdrawalAgeRow = document.getElementById('withdrawal-age-row');
    const withdrawalAgeInput = document.getElementById('withdrawal_age');
    const annuityTypeRadios = document.querySelectorAll('input[name="annuity_type"]');
    
    // Handle annuity type change to show/hide withdrawal age
    annuityTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'variable') {
                withdrawalAgeRow.style.display = 'grid';
                withdrawalAgeInput.required = true;
            } else {
                withdrawalAgeRow.style.display = 'none';
                withdrawalAgeInput.required = false;
                withdrawalAgeInput.value = '';
            }
        });
    });
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous results/errors
        errorMessage.style.display = 'none';
        results.style.display = 'none';
        results.innerHTML = '';
        
        // Get form data
        const formData = new FormData(form);
        const data = {
            name: formData.get('name') || '',
            email: formData.get('email'),
            current_age: parseInt(formData.get('current_age')) || 0,
            annuity_type: formData.get('annuity_type'),
            phone: formData.get('phone') || '',
            retirement_account: formData.get('retirement_account') || '',
            state: formData.get('state'),
            amount: parseFloat(formData.get('amount')) || 0
        };
        
        // Add withdrawal age if variable
        if (data.annuity_type === 'variable') {
            data.withdrawal_age = parseInt(formData.get('withdrawal_age')) || 0;
        }
        
        // Show loading
        loading.style.display = 'block';
        form.style.opacity = '0.5';
        
        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Calculation failed');
            }
            
            if (result.type === 'fixed') {
                displayFixedResults(result.results);
            } else if (result.type === 'variable') {
                displayVariableResults(result.result);
            }
            
        } catch (error) {
            errorMessage.textContent = error.message || 'An error occurred. Please try again.';
            errorMessage.style.display = 'block';
        } finally {
            loading.style.display = 'none';
            form.style.opacity = '1';
        }
    });
    
    function displayFixedResults(products) {
        if (!products || products.length === 0) {
            results.innerHTML = '<p class="disclaimer">No products found matching your criteria. Please try adjusting your investment amount.</p>';
            results.style.display = 'block';
            return;
        }
        
        let html = '<h2>Available Fixed Annuity Products</h2>';
        html += '<table class="results-table">';
        html += '<thead><tr>';
        html += '<th>Company</th>';
        html += '<th>Product</th>';
        html += '<th>Base Rate</th>';
        html += '<th>Term</th>';
        html += '<th>Min Investment</th>';
        html += '</tr></thead><tbody>';
        
        products.forEach(product => {
            html += '<tr>';
            html += `<td>${escapeHtml(product.company)}</td>`;
            html += `<td>${escapeHtml(product.product)}</td>`;
            html += `<td>${product.base_rate.toFixed(2)}%</td>`;
            html += `<td>${product.rate_term || 'N/A'} years</td>`;
            html += `<td>$${product.min_contribution.toLocaleString()}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        html += '<p class="disclaimer">Product availability varies by state. Contact us to confirm eligibility and get detailed quotes.</p>';
        
        results.innerHTML = html;
        results.style.display = 'block';
    }
    
    function displayVariableResults(result) {
        let html = '<div class="variable-result">';
        html += '<h3>Variable Annuity Projection</h3>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Investment Amount:</span>';
        html += `<span class="result-value">$${result.investment_amount.toLocaleString()}</span>`;
        html += '</div>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Current Age:</span>';
        html += `<span class="result-value">${result.current_age}</span>`;
        html += '</div>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Withdrawal Age:</span>';
        html += `<span class="result-value">${result.withdrawal_age}</span>`;
        html += '</div>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Deferral Period:</span>';
        html += `<span class="result-value">${result.deferral_period} years</span>`;
        html += '</div>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Withdrawal Rate:</span>';
        html += `<span class="result-value">${result.withdrawal_rate}%</span>`;
        html += '</div>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Annual Income:</span>';
        html += `<span class="result-value">$${result.annual_income.toLocaleString()}</span>`;
        html += '</div>';
        
        html += '<div class="result-item">';
        html += '<span class="result-label">Monthly Income:</span>';
        html += `<span class="result-value">$${result.monthly_income.toLocaleString()}</span>`;
        html += '</div>';
        
        html += '</div>';
        
        html += `<p class="disclaimer">${result.disclaimer}</p>`;
        
        results.innerHTML = html;
        results.style.display = 'block';
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Auto-resize iframe height for parent page
    function sendHeightToParent() {
        if (window.parent !== window) {
            const height = document.body.scrollHeight;
            window.parent.postMessage({
                type: 'resize',
                height: height
            }, '*');
        }
    }
    
    // Send height when results are displayed
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.target.id === 'results' && mutation.target.style.display === 'block') {
                setTimeout(sendHeightToParent, 100);
            }
        });
    });
    
    observer.observe(results, { attributes: true, attributeFilter: ['style'] });
    
    // Send initial height
    setTimeout(sendHeightToParent, 100);
});