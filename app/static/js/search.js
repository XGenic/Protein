document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    const typeSelect = document.querySelector('select[name="type"]');
    const sortSelect = document.querySelector('select[name="sort"]');
    let searchTimeout;

    // Function to update results
    function updateResults() {
        const search = searchInput.value;
        const type = typeSelect.value;
        const sort = sortSelect.value;

        // Show loading indicator
        document.querySelector('.products').classList.add('loading');

        fetch(`/api/search?search=${encodeURIComponent(search)}&type=${type}&sort=${sort}`)
            .then(response => response.json())
            .then(products => {
                const tbody = document.querySelector('tbody');
                tbody.innerHTML = '';

                products.forEach(product => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${product.product_type.charAt(0).toUpperCase() + product.product_type.slice(1)}</td>
                            <td>${product.name}</td>
                            <td>${product.brand}</td>
                            <td>$${product.price.toFixed(2)}</td>
                            <td>${product.protein_per_serving}g</td>
                            <td>${product.servings}</td>
                            <td>$${product.price_per_protein.toFixed(3)}/g</td>
                        </tr>
                    `;
                });

                // Remove loading indicator
                document.querySelector('.products').classList.remove('loading');
            });
    }

    // Add event listeners
    searchInput.addEventListener('input', function() {
        // Clear the existing timeout
        clearTimeout(searchTimeout);
        
        // Set a new timeout to prevent too many requests
        searchTimeout = setTimeout(updateResults, 300);
    });

    typeSelect.addEventListener('change', updateResults);
    sortSelect.addEventListener('change', updateResults);
}); 