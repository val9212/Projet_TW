document.addEventListener('DOMContentLoaded', function() {
    const alignCheckbox = document.getElementById('align');
    const significanceCheckbox = document.getElementById('significance');
    const alignParams = document.getElementById('align-params');
    const significanceParams = document.getElementById('significance-params');
    const form = document.getElementById('alignment-form');
    const loader = document.getElementById('loader');

    function toggleFields() {
        alignParams.style.display = alignCheckbox.checked ? 'block' : 'none';
        significanceParams.style.display = significanceCheckbox.checked ? 'block' : 'none';
    }

    alignCheckbox.addEventListener('change', toggleFields);
    significanceCheckbox.addEventListener('change', toggleFields);

    form.addEventListener('submit', function() {
        loader.style.display = 'block';
    });

    toggleFields();
});
