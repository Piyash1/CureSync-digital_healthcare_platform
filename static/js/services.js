function filterDoctors() {
    const filter = document.getElementById('specialization').value;
    const cards = document.querySelectorAll('.service-card');
    cards.forEach(card => {
        const specialization = card.getAttribute('data-specialization');
        card.style.display = filter === 'all' || specialization === filter ? 'block' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    filterDoctors();
});