document.addEventListener('DOMContentLoaded', () => {
    // Mobile Navigation
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            const spans = navToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
    
    // Typing Animation
    const typingElement = document.querySelector('.typing');
    if (typingElement) {
        const text = typingElement.getAttribute('data-text');
        let i = 0;
        typingElement.textContent = '';
        
        const typeWriter = () => {
            if (i < text.length) {
                typingElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
    
    // Copy to Clipboard
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const text = btn.getAttribute('data-clipboard');
            try {
                await navigator.clipboard.writeText(text);
                const originalText = btn.textContent;
                btn.textContent = 'Copié !';
                btn.classList.add('copied');
                
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    });
    
    // Usage Tabs
    const tabs = document.querySelectorAll('.usage-tab');
    const panels = document.querySelectorAll('.usage-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.getAttribute('data-tab');
            
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Animate feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Animate install methods
    const installMethods = document.querySelectorAll('.install-method');
    installMethods.forEach((method, index) => {
        method.style.opacity = '0';
        method.style.transform = 'translateY(20px)';
        method.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(method);
    });
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const navHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Navbar background on scroll
    let lastScroll = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.8)';
        }
        
        lastScroll = currentScroll;
    });
    
    // Terminal interactive effect
    const terminal = document.querySelector('.terminal');
    if (terminal) {
        terminal.addEventListener('mousemove', (e) => {
            const rect = terminal.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            if (window.innerWidth > 768) {
                terminal.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            }
        });
        
        terminal.addEventListener('mouseleave', () => {
            if (window.innerWidth > 768) {
                terminal.style.transform = 'perspective(1000px) rotateY(-5deg) rotateX(5deg)';
            }
        });
    }
});