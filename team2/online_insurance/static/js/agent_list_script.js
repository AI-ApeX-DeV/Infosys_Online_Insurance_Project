// static/js/scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const filterSelect = document.getElementById('status-filter');
    const agentCards = document.querySelectorAll('.agent-card');

    filterSelect.addEventListener('change', () => {
        const filterValue = filterSelect.value;
        agentCards.forEach(card => {
            const status = card.getAttribute('data-status');
            if (filterValue === 'all' || filterValue === status) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
