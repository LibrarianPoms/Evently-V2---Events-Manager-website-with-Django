// Evently Animation and Interactive Elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initAnimations();
    
    // Initialize scroll effects
    initScrollEffects();
    
    // Initialize interactive elements
    initInteractiveElements();
    
    // Initialize epic animations
    initEpicAnimations();
    
    // Initialize 3D card effects
    init3DCardEffects();
    
    // Initialize particle background
    initParticleBackground();
    
    // Auto-close alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Initialize animations for elements
function initAnimations() {
    // Add animation classes to elements
    const fadeElements = document.querySelectorAll('.fade-in-element');
    fadeElements.forEach(el => {
        el.classList.add('fade-in');
    });
    
    const slideUpElements = document.querySelectorAll('.slide-up-element');
    slideUpElements.forEach(el => {
        el.classList.add('slide-up');
    });
    
    const slideRightElements = document.querySelectorAll('.slide-right-element');
    slideRightElements.forEach(el => {
        el.classList.add('slide-in-right');
    });
    
    // Staggered animations for card elements
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Create animated background shapes
    createBackgroundShapes();
}

// Create animated background shapes
function createBackgroundShapes() {
    const bgAnimation = document.querySelector('.bg-animation');
    if (!bgAnimation) return;
    
    // Clear existing shapes
    const existingShapes = bgAnimation.querySelectorAll('.shape');
    existingShapes.forEach(shape => shape.remove());
    
    // Create new shapes
    for (let i = 0; i < 3; i++) {
        const shape = document.createElement('div');
        shape.classList.add('shape');
        bgAnimation.appendChild(shape);
    }
}

// Initialize scroll effects
function initScrollEffects() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Reveal elements on scroll
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    
    const revealOnScroll = function() {
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.classList.add('revealed');
            }
        });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    // Initial check
    revealOnScroll();
}

// Initialize interactive elements
function initInteractiveElements() {
    // Card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });
    
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('btn-hover');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('btn-hover');
        });
    });
    
    // Countdown timers for events
    initCountdownTimers();
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize countdown timers for events
function initCountdownTimers() {
    const countdownElements = document.querySelectorAll('.countdown-timer');
    
    countdownElements.forEach(element => {
        const targetDate = new Date(element.getAttribute('data-target-date')).getTime();
        
        // Update the countdown every second
        const countdownInterval = setInterval(function() {
            // Get current date and time
            const now = new Date().getTime();
            
            // Calculate the time remaining
            const distance = targetDate - now;
            
            // Time calculations for days, hours, minutes and seconds
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // Display the result
            element.innerHTML = `
                <div class="countdown-item">
                    <span class="countdown-value">${days}</span>
                    <span class="countdown-label">Days</span>
                </div>
                <div class="countdown-item">
                    <span class="countdown-value">${hours}</span>
                    <span class="countdown-label">Hours</span>
                </div>
                <div class="countdown-item">
                    <span class="countdown-value">${minutes}</span>
                    <span class="countdown-label">Minutes</span>
                </div>
                <div class="countdown-item">
                    <span class="countdown-value">${seconds}</span>
                    <span class="countdown-label">Seconds</span>
                </div>
            `;
            
            // If the countdown is finished, display expired message
            if (distance < 0) {
                clearInterval(countdownInterval);
                element.innerHTML = "Event has started!";
            }
        }, 1000);
    });
}

// Parallax effect for background elements
window.addEventListener('scroll', function() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    parallaxElements.forEach(element => {
        const scrollPosition = window.pageYOffset;
        const speed = element.getAttribute('data-parallax-speed') || 0.5;
        
        element.style.transform = `translateY(${scrollPosition * speed}px)`;
    });
});

// Add typing effect to headings
function addTypingEffect(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function typeWriter() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }
    
    typeWriter();
}

// Initialize typing effects
const typingElements = document.querySelectorAll('.typing-effect');
typingElements.forEach(element => {
    const text = element.getAttribute('data-text');
    const speed = parseInt(element.getAttribute('data-speed')) || 100;
    addTypingEffect(element, text, speed);
});

// Epic Animations Section
// ======================

// Initialize epic animations
function initEpicAnimations() {
    // Add pulse effect to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-success');
    buttons.forEach(button => {
        button.classList.add('pulse-effect');
    });
    
    // Add floating animation to featured event card
    const featuredEvent = document.querySelector('.card.shadow-sm');
    if (featuredEvent) {
        featuredEvent.classList.add('floating-animation');
    }
    
    // Add glowing effect to headings
    const headings = document.querySelectorAll('h1, h2');
    headings.forEach(heading => {
        heading.classList.add('glow-effect');
    });
    
    // Add confetti effect to success messages
    const successMessages = document.querySelectorAll('.alert-success');
    if (successMessages.length > 0) {
        createConfetti();
    }
}

// Create confetti effect
function createConfetti() {
    const confettiContainer = document.createElement('div');
    confettiContainer.classList.add('confetti-container');
    document.body.appendChild(confettiContainer);
    
    // Create confetti pieces
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement('div');
        confetti.classList.add('confetti');
        
        // Random colors
        const colors = ['#f94144', '#f3722c', '#f8961e', '#f9c74f', '#90be6d', '#43aa8b', '#577590'];
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        // Random position and animation duration
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
        confetti.style.opacity = Math.random();
        confetti.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';
        
        confettiContainer.appendChild(confetti);
    }
    
    // Remove confetti after animation
    setTimeout(() => {
        confettiContainer.remove();
    }, 5000);
}

// Initialize 3D card effects
function init3DCardEffects() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            // Get card dimensions and position
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate rotation based on mouse position - more subtle
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 30; // Reduced rotation amount
            const rotateY = (centerX - x) / 30; // Reduced rotation amount
            
            // Apply 3D rotation - more subtle
            card.style.transform = `perspective(2000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            
            // Add highlight effect
            const shine = card.querySelector('.card-shine') || document.createElement('div');
            if (!card.querySelector('.card-shine')) {
                shine.classList.add('card-shine');
                card.appendChild(shine);
            }
            
            // Position the shine effect
            shine.style.backgroundImage = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 80%)`;
        });
        
        // Reset card on mouse leave
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            const shine = card.querySelector('.card-shine');
            if (shine) shine.remove();
        });
    });
}

// Initialize particle background
function initParticleBackground() {
    const mainContainer = document.querySelector('.container');
    if (!mainContainer) return;
    
    // Create particle container
    const particleContainer = document.createElement('div');
    particleContainer.classList.add('particle-background');
    mainContainer.parentNode.insertBefore(particleContainer, mainContainer);
    
    // Create particles - reduced number for subtlety
    for (let i = 0; i < 20; i++) {
        createParticle(particleContainer);
    }
}

// Create a single particle
function createParticle(container) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    // Random size
    const size = Math.random() * 10 + 5;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    
    // Random position
    particle.style.left = Math.random() * 100 + 'vw';
    particle.style.top = Math.random() * 100 + 'vh';
    
    // Random color
    const hue = Math.random() * 360;
    particle.style.backgroundColor = `hsla(${hue}, 70%, 60%, 0.3)`;
    
    // Random animation - slower for subtlety
    particle.style.animationDuration = (Math.random() * 25 + 15) + 's';
    particle.style.animationDelay = (Math.random() * 10) + 's';
    
    container.appendChild(particle);
}
