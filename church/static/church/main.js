document.addEventListener("DOMContentLoaded", function () {

    // Animate summary card numbers counting up
    const counters = document.querySelectorAll('.card h2');
    counters.forEach(counter => {
        let count = 0;
        const target = parseInt(counter.innerText);
        const speed = 20; // ms per increment
        const increment = Math.ceil(target / 50);

        const updateCount = () => {
            count += increment;
            if (count > target) count = target;
            counter.innerText = count;
            if (count < target) {
                setTimeout(updateCount, speed);
            }
        };
        updateCount();
    });

    // Table row hover highlight (extra effect)
    const tables = document.querySelectorAll('table tbody tr');
    tables.forEach(row => {
        row.addEventListener('mouseenter', () => row.style.backgroundColor = '#eafaf1');
        row.addEventListener('mouseleave', () => row.style.backgroundColor = '');
    });

    // Responsive navbar toggle (if you add a menu button)
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if(navToggle && navMenu){
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
});
