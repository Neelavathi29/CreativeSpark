document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            sidebar.classList.toggle('active');
        });
    }

    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    const sidebarLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    sidebarLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('active');
            }
        });
    });

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(reg) {
                console.log('Service Worker registered');
            })
            .catch(function(err) {
                console.log('Service Worker registration failed:', err);
            });
    }

    const pageTransition = document.getElementById('pageTransition');
    if (pageTransition) {
        document.querySelectorAll('a:not([target="_blank"]):not([href^="#"]):not([href^="javascript"]):not([href^="mailto"])').forEach(function(link) {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href && !href.startsWith('#') && !href.startsWith('javascript') && !href.startsWith('mailto') && this.hostname === window.location.hostname) {
                    e.preventDefault();
                    pageTransition.classList.add('active');
                    setTimeout(function() {
                        window.location.href = href;
                    }, 400);
                }
            });
        });
        window.addEventListener('pageshow', function() {
            pageTransition.classList.remove('active');
        });
    }

    var confettiCanvas = document.getElementById('confettiCanvas');
    if (confettiCanvas && typeof canvasConfetti !== 'undefined') {
        var rect = confettiCanvas.getBoundingClientRect();
        var x = rect.left + rect.width / 2;
        var y = rect.top + rect.height / 2;
        canvasConfetti({
            particleCount: 100,
            spread: 70,
            origin: {
                x: x / window.innerWidth,
                y: y / window.innerHeight
            }
        });
    }
});