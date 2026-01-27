// Navigation
const navbar = document.querySelector('.navbar');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

// Add scroll effect to navbar
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    // Update active nav link based on scroll position
    updateActiveNavLink();
});

// Mobile menu toggle
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Update active nav link based on scroll position
function updateActiveNavLink() {
    let current = '';
    const sections = document.querySelectorAll('section[id]');
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;
        if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// Carousel
class Carousel {
    constructor() {
        this.slides = document.querySelectorAll('.carousel-slide');
        this.indicators = document.querySelectorAll('.indicator');
        this.prevBtn = document.querySelector('.prev-btn');
        this.nextBtn = document.querySelector('.next-btn');
        this.currentSlide = 0;
        this.slideInterval = null;
        this.slideDuration = 5000; // 5 seconds
        
        this.init();
    }
    
    init() {
        // Show first slide
        this.showSlide(this.currentSlide);
        
        // Start auto slide
        this.startAutoSlide();
        
        // Event listeners for buttons
        this.prevBtn.addEventListener('click', () => {
            this.stopAutoSlide();
            this.prevSlide();
            this.startAutoSlide();
        });
        
        this.nextBtn.addEventListener('click', () => {
            this.stopAutoSlide();
            this.nextSlide();
            this.startAutoSlide();
        });
        
        // Event listeners for indicators
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                this.stopAutoSlide();
                this.goToSlide(index);
                this.startAutoSlide();
            });
        });
        
        // Pause auto slide on hover
        const carousel = document.querySelector('.carousel');
        carousel.addEventListener('mouseenter', () => this.stopAutoSlide());
        carousel.addEventListener('mouseleave', () => this.startAutoSlide());
    }
    
    showSlide(index) {
        // Hide all slides
        this.slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // Remove active class from all indicators
        this.indicators.forEach(indicator => indicator.classList.remove('active'));
        
        // Show current slide
        this.slides[index].classList.add('active');
        
        // Add active class to current indicator
        this.indicators[index].classList.add('active');
        
        this.currentSlide = index;
    }
    
    nextSlide() {
        let nextIndex = this.currentSlide + 1;
        if (nextIndex >= this.slides.length) {
            nextIndex = 0;
        }
        this.showSlide(nextIndex);
    }
    
    prevSlide() {
        let prevIndex = this.currentSlide - 1;
        if (prevIndex < 0) {
            prevIndex = this.slides.length - 1;
        }
        this.showSlide(prevIndex);
    }
    
    goToSlide(index) {
        this.showSlide(index);
    }
    
    startAutoSlide() {
        this.slideInterval = setInterval(() => {
            this.nextSlide();
        }, this.slideDuration);
    }
    
    stopAutoSlide() {
        if (this.slideInterval) {
            clearInterval(this.slideInterval);
            this.slideInterval = null;
        }
    }
}

// Testimonial Slider
class TestimonialSlider {
    constructor() {
        this.testimonials = document.querySelectorAll('.testimonial');
        this.currentTestimonial = 0;
        this.interval = null;
        
        this.init();
    }
    
    init() {
        // Show first testimonial
        this.showTestimonial(this.currentTestimonial);
        
        // Auto cycle testimonials
        this.startAutoCycle();
        
        // Pause on hover
        const slider = document.querySelector('.testimonial-slider');
        slider.addEventListener('mouseenter', () => this.stopAutoCycle());
        slider.addEventListener('mouseleave', () => this.startAutoCycle());
    }
    
    showTestimonial(index) {
        // Hide all testimonials
        this.testimonials.forEach(testimonial => {
            testimonial.classList.remove('active');
        });
        
        // Show current testimonial
        this.testimonials[index].classList.add('active');
        this.currentTestimonial = index;
    }
    
    nextTestimonial() {
        let nextIndex = this.currentTestimonial + 1;
        if (nextIndex >= this.testimonials.length) {
            nextIndex = 0;
        }
        this.showTestimonial(nextIndex);
    }
    
    startAutoCycle() {
        this.interval = setInterval(() => {
            this.nextTestimonial();
        }, 6000); // Change every 6 seconds
    }
    
    stopAutoCycle() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize carousel
    const carousel = new Carousel();
    
    // Initialize testimonial slider
    const testimonialSlider = new TestimonialSlider();
    
    // Booking form submission
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const roomType = this.querySelector('select').value;
            const nights = this.querySelector('input[type="number"]').value;
            
            // Calculate price based on room type
            let pricePerNight = 0;
            switch(roomType) {
                case 'deluxe':
                    pricePerNight = 29900;
                    break;
                case 'executive':
                    pricePerNight = 49900;
                    break;
                case 'presidential':
                    pricePerNight = 89900;
                    break;
            }
            
            const totalPrice = pricePerNight * nights;
            
            // Show booking confirmation
            alert(`Booking Confirmed!\n\nRoom Type: ${roomType}\nNumber of Nights: ${nights}\nTotal Price: KSh ${totalPrice.toLocaleString()}\n\nWe will contact you shortly at the phone number provided.`);
            
            // Reset form
            this.reset();
        });
    }
    
    // Add animation to elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 1s ease forwards';
            }
        });
    }, observerOptions);
    
    // Observe feature cards, room cards, and food cards
    document.querySelectorAll('.feature-card, .room-card, .food-card').forEach(card => {
        observer.observe(card);
    });
    
    // Add MPesa icon styling
    const style = document.createElement('style');
    style.textContent = `
        .fa-mpesa:before {
            content: "M-PESA";
            font-family: Arial, sans-serif;
            font-weight: bold;
            font-size: 1.8rem;
        }
    `;
    document.head.appendChild(style);
    
    // Initialize active nav link
    updateActiveNavLink();
});