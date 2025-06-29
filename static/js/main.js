// Main JavaScript file for Redmine Admin

document.addEventListener('DOMContentLoaded', function() {
    console.log('Redmine Admin Dashboard loaded');
    
    // Add any interactive functionality here
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            // Add click effects or navigation
            console.log('Card clicked:', this.querySelector('.card-title').textContent);
        });
    });
}); 