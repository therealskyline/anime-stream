document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navbarNav = document.querySelector('.navbar-nav');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navbarNav.classList.toggle('show');
        });
    }
    
    // Search functionality
    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.querySelector('#searchInput').value.trim();
            if (query) {
                window.location.href = `/search?query=${encodeURIComponent(query)}`;
            }
        });
    }
    
    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-button');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Si le bouton a un attribut href, utiliser celui-ci
            if (this.getAttribute('href') && !this.getAttribute('href').startsWith('#')) {
                return; // L'action par défaut du navigateur prendra le relais
            }
            
            // Sinon, utiliser l'attribut data-genre
            const genre = this.dataset.genre;
            if (genre) {
                window.location.href = `/search?genre=${encodeURIComponent(genre)}`;
            }
            
            // Pour les liens d'ancre internes
            if (this.getAttribute('href') && this.getAttribute('href').startsWith('#')) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    // Ajouter une classe active au bouton cliqué
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Scroll avec animation
                    targetElement.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Seasons tabs
    const seasonTabs = document.querySelectorAll('.season-tab');
    const seasonContents = document.querySelectorAll('.season-content');
    
    if (seasonTabs.length > 0) {
        seasonTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const seasonId = this.dataset.season;
                
                // Remove active class from all tabs and hide all content
                seasonTabs.forEach(t => t.classList.remove('active'));
                seasonContents.forEach(c => c.style.display = 'none');
                
                // Add active class to clicked tab and show corresponding content
                this.classList.add('active');
                document.querySelector(`.season-content[data-season="${seasonId}"]`).style.display = 'block';
            });
        });
        
        // Activate the first tab by default
        seasonTabs[0].click();
    }
    
    // Contrôles personnalisés du lecteur vidéo
    const videoPlayer = document.getElementById('custom-video-player');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    
    if (videoPlayer && fullscreenBtn) {
        // Lecture/Pause en cliquant sur la vidéo
        videoPlayer.addEventListener('click', function() {
            if (videoPlayer.paused) {
                videoPlayer.play();
            } else {
                videoPlayer.pause();
            }
        });
        
        // Bouton plein écran
        fullscreenBtn.addEventListener('click', function() {
            if (!document.fullscreenElement) {
                if (videoPlayer.requestFullscreen) {
                    videoPlayer.requestFullscreen();
                } else if (videoPlayer.webkitRequestFullscreen) {
                    videoPlayer.webkitRequestFullscreen();
                } else if (videoPlayer.msRequestFullscreen) {
                    videoPlayer.msRequestFullscreen();
                }
                
                // Changer l'icône
                fullscreenBtn.querySelector('i').classList.remove('fa-expand');
                fullscreenBtn.querySelector('i').classList.add('fa-compress');
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                
                // Changer l'icône
                fullscreenBtn.querySelector('i').classList.remove('fa-compress');
                fullscreenBtn.querySelector('i').classList.add('fa-expand');
            }
        });
        
        // Quand la vidéo se termine, suggérer l'épisode suivant
        videoPlayer.addEventListener('ended', function() {
            const nextEpisodeLink = document.querySelector('.next-episode');
            if (nextEpisodeLink) {
                setTimeout(() => {
                    window.location.href = nextEpisodeLink.href;
                }, 2000);
            }
        });
        
        // Gérer le changement d'état du plein écran
        document.addEventListener('fullscreenchange', updateFullscreenButton);
        document.addEventListener('webkitfullscreenchange', updateFullscreenButton);
        document.addEventListener('mozfullscreenchange', updateFullscreenButton);
        document.addEventListener('MSFullscreenChange', updateFullscreenButton);
        
        function updateFullscreenButton() {
            if (document.fullscreenElement) {
                fullscreenBtn.querySelector('i').classList.remove('fa-expand');
                fullscreenBtn.querySelector('i').classList.add('fa-compress');
            } else {
                fullscreenBtn.querySelector('i').classList.remove('fa-compress');
                fullscreenBtn.querySelector('i').classList.add('fa-expand');
            }
        }
    }
    
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Animation on scroll
    if ('IntersectionObserver' in window) {
        const fadeElements = document.querySelectorAll('.fade-in');
        const fadeObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        fadeElements.forEach(element => {
            fadeObserver.observe(element);
        });
    }
});
