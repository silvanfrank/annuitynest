document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('annuity-form');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    const results = document.getElementById('results');
    const container = document.querySelector('.container');
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
        // Expand container for table view
        container.classList.add('has-results');
        
        if (!products || products.length === 0) {
            results.innerHTML = '<p class="disclaimer">No products found matching your criteria. Please try adjusting your investment amount.</p>';
            results.style.display = 'block';
            return;
        }
        
        let html = '<h2>Available Fixed Annuity Products</h2>';
        html += '<table class="results-table">';
        html += '<thead><tr>';
        html += '<th>Sort</th>';
        html += '<th>Company</th>';
        html += '<th>Product</th>';
        html += '<th>Years</th>';
        html += '<th>Min Contribution</th>';
        html += '<th>Min Rate</th>';
        html += '<th>Base Rate</th>';
        html += '<th>Bonus Rate</th>';
        html += '<th>Yield to Surrender</th>';
        html += '<th>Surrender Period</th>';
        html += '<th>Future Value</th>';
        html += '</tr></thead><tbody>';
        
        products.forEach(product => {
            html += '<tr>';
            html += `<td>${product.sort || ''}</td>`;
            html += `<td>${escapeHtml(product.company)}</td>`;
            html += `<td>${escapeHtml(product.product)}</td>`;
            html += `<td>${product.years || 'N/A'}</td>`;
            html += `<td>$${product.min_contribution ? product.min_contribution.toLocaleString() : '0'}</td>`;
            html += `<td>${product.min_rate ? product.min_rate.toFixed(2) : '0.00'}%</td>`;
            html += `<td>${product.base_rate ? product.base_rate.toFixed(2) : '0.00'}%</td>`;
            html += `<td>${product.bonus_rate ? product.bonus_rate.toFixed(2) : '0.00'}%</td>`;
            html += `<td>${product.yield_to_surrender ? product.yield_to_surrender.toFixed(3) : '0.000'}%</td>`;
            html += `<td>${product.surrender_period || 'N/A'} years</td>`;
            html += `<td>$${product.future_value ? product.future_value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '0.00'}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        html += `<p class="disclaimer">Showing all ${products.length} products. Product availability varies by state. Contact us to confirm eligibility and get detailed quotes.</p>`;
        
        results.innerHTML = html;
        results.style.display = 'block';
    }
    
    function displayVariableResults(result) {
        // Expand container for table view
        container.classList.add('has-results');
        
        if (!result || !result.products || result.products.length === 0) {
            results.innerHTML = '<p class="disclaimer">No variable annuity products found. Please try adjusting your criteria.</p>';
            results.style.display = 'block';
            return;
        }
        
        let html = '';
        html += '<h3>Available Variable Annuity Products</h3>';
        html += '<table class="results-table">';
        html += '<thead><tr>';
        html += '<th>Annuity Type</th>';
        html += '<th>Carrier</th>';
        html += '<th>Rider Name</th>';
        html += '<th>Annual Lifetime Income Amount</th>';
        html += '</tr></thead><tbody>';
        
        result.products.forEach(product => {
            html += '<tr>';
            html += `<td>${escapeHtml(product.annuity_type)}</td>`;
            html += `<td>${escapeHtml(product.carrier)}</td>`;
            html += `<td>${escapeHtml(product.rider_name)}</td>`;
            html += `<td>$${product.annual_lifetime_income ? product.annual_lifetime_income.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) : '0.00'}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        html += `<p class="disclaimer">Showing all ${result.count} variable annuity products. Displaying columns B (Annuity Type), C (Carrier), E (Rider Name), and S (Annual Lifetime Income Amount) as specified in the Excel file.</p>`;
        
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