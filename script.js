// ============================================
// Remote for Roku TV – Aruk - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    initScrollAnimations();
    initNavScrollEffect();
    initStickyDownload();
    initFeatureTabs();
    initScreenshotSlider();
    initFAQAccordion();
    initSmoothScroll();
    trackDownloadLinks();
});


// ============================================
// Scroll-triggered Reveal Animations
// ============================================

function initScrollAnimations() {
    const revealEls = document.querySelectorAll('.reveal');
    if (!revealEls.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // animate once
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    });

    revealEls.forEach(el => observer.observe(el));
}


// ============================================
// Nav — backdrop blur + border on scroll
// ============================================

function initNavScrollEffect() {
    const header = document.getElementById('site-header');
    if (!header) return;

    const handler = () => {
        if (window.scrollY > 40) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handler, { passive: true });
    handler(); // run once on load
}


// ============================================
// Sticky Download Bar Logic (Mobile)
// ============================================

function initStickyDownload() {
    const stickyBar = document.getElementById('stickyDownload');
    const heroSection = document.querySelector('.hero');

    if (!stickyBar || !heroSection) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                stickyBar.classList.add('visible');
            } else {
                stickyBar.classList.remove('visible');
            }
        });
    }, { threshold: 0.1 });

    observer.observe(heroSection);
}


// ============================================
// Feature Tab Filter
// ============================================

function initFeatureTabs() {
    const tabs = document.querySelectorAll('.feature-tab');
    const cards = document.querySelectorAll('.feature-card[data-category]');
    if (!tabs.length) return;

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const filter = tab.dataset.filter;

            cards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.classList.remove('hidden');
                    // Re-trigger reveal if needed
                    if (!card.classList.contains('visible')) {
                        card.classList.add('visible');
                    }
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
}


// ============================================
// Screenshot Slider
// ============================================

function initScreenshotSlider() {
    const slider = document.getElementById('screenshotSlider');
    const prevBtn = document.getElementById('sliderPrev');
    const nextBtn = document.getElementById('sliderNext');

    if (!slider || !prevBtn || !nextBtn) return;

    const SCROLL_AMOUNT = 240; // px per click

    nextBtn.addEventListener('click', () => {
        slider.scrollBy({ left: SCROLL_AMOUNT, behavior: 'smooth' });
    });

    prevBtn.addEventListener('click', () => {
        slider.scrollBy({ left: -SCROLL_AMOUNT, behavior: 'smooth' });
    });

    // Touch/drag swipe support
    let isDragging = false;
    let startX = 0;
    let scrollStart = 0;

    slider.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.pageX - slider.offsetLeft;
        scrollStart = slider.scrollLeft;
        slider.style.cursor = 'grabbing';
    });
    slider.addEventListener('mouseleave', () => {
        isDragging = false;
        slider.style.cursor = '';
    });
    slider.addEventListener('mouseup', () => {
        isDragging = false;
        slider.style.cursor = '';
    });
    slider.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        slider.scrollLeft = scrollStart - (x - startX);
    });

    // Highlight the slide currently nearest the center of the viewport.
    const slides = slider.querySelectorAll('.screenshot-slide');
    if (slides.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                entry.target.classList.toggle('active', entry.intersectionRatio > 0.65);
            });
        }, {
            root: slider,
            threshold: [0.25, 0.5, 0.75],
            rootMargin: '0px'
        });

        slides.forEach(slide => observer.observe(slide));
    }
}


// ============================================
// FAQ Accordion
// ============================================

function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) return;

    faqItems.forEach(item => {
        const question = item.querySelector('h3');
        if (!question) return;

        question.addEventListener('click', () => {
            const isOpen = item.classList.contains('open');
            // Close all
            faqItems.forEach(i => i.classList.remove('open'));
            // Open clicked if it was closed
            if (!isOpen) {
                item.classList.add('open');
            }
        });
    });
}


// ============================================
// Smooth Scroll for Anchor Links
// ============================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const headerH = document.getElementById('site-header')?.offsetHeight || 70;
                const top = target.getBoundingClientRect().top + window.scrollY - headerH - 20;
                window.scrollTo({ top, behavior: 'smooth' });
                window.history.pushState(null, null, href);
            }
        });
    });
}


// ============================================
// Analytics — Download Click Tracking
// ============================================

function trackDownloadClick() {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'view_item', {
            items: [{
                id: 'app_download',
                name: 'Remote for Roku TV – Aruk Download',
                category: 'app',
                quantity: 1
            }]
        });
    }
}

function trackDownloadLinks() {
    document.querySelectorAll('a[href*="play.google.com"]').forEach(link => {
        link.addEventListener('click', trackDownloadClick);
    });

    // FAQ tracking
    document.querySelectorAll('.faq-item h3').forEach(item => {
        item.addEventListener('click', () => {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'view_item', {
                    items: [{ id: 'faq_view', name: 'FAQ Viewed', category: 'engagement' }]
                });
            }
        });
    });
}


// ============================================
// Performance — Lazy load data-src images
// ============================================

if ('loading' in HTMLImageElement.prototype) {
    document.querySelectorAll('img[data-src]').forEach(img => {
        img.src = img.dataset.src;
    });
}


// ============================================
// Error Handling
// ============================================

window.addEventListener('error', function (event) {
    console.error('An error occurred:', event.error);
});


// ============================================
// Console branding
// ============================================

console.log('%c📺 Remote for Roku TV – Aruk', 'font-size:16px; font-weight:800; color:#2563EB;');
console.log('%c  Free Roku remote for Android — smartremotelabs.github.io', 'font-size:12px; color:#888;');
