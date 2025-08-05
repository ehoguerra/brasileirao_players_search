// Main JavaScript for Brasileirão Players Search
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize components
    initializeSearch();
    initializeMobileOptimizations();
    initializeAccessibility();
    initializePerformance();
    
    console.log('🎯 Brasileirão Players Search - Website carregado');
});

// Search functionality
function initializeSearch() {
    const searchForm = document.getElementById('searchForm');
    const serieSelect = document.getElementById('serie');
    const clubSelect = document.getElementById('club');
    
    if (!searchForm) return;
    
    // Auto-loading clubs based on serie selection
    if (serieSelect && clubSelect) {
        serieSelect.addEventListener('change', function() {
            const selectedSerie = this.value;
            loadClubsForSerie(selectedSerie, clubSelect);
        });
    }
    
    // Form validation
    searchForm.addEventListener('submit', function(e) {
        if (!validateSearchForm()) {
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        showFormLoading(true);
    });
    
    // Auto-collapse filters on mobile after search
    if (window.innerWidth < 992) {
        searchForm.addEventListener('submit', function() {
            setTimeout(() => {
                const filtersCollapse = document.getElementById('searchFilters');
                if (filtersCollapse && filtersCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(filtersCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            }, 100);
        });
    }
}

// Load clubs for selected serie
function loadClubsForSerie(serie, clubSelect) {
    if (!clubSelect) return;
    
    // Show loading state
    clubSelect.innerHTML = '<option value="">Carregando...</option>';
    clubSelect.disabled = true;
    
    if (!serie) {
        // Reset to all clubs
        window.location.reload();
        return;
    }
    
    // Fetch clubs for the selected serie
    fetch(`/api/clubs/${encodeURIComponent(serie)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(clubs => {
            // Reset select
            clubSelect.innerHTML = '<option value="">Todos os clubes</option>';
            
            // Add clubs
            clubs.forEach(club => {
                const option = document.createElement('option');
                option.value = club;
                option.textContent = club;
                clubSelect.appendChild(option);
            });
            
            clubSelect.disabled = false;
        })
        .catch(error => {
            console.error('Erro ao carregar clubes:', error);
            clubSelect.innerHTML = '<option value="">Erro ao carregar</option>';
            
            // Show error toast
            showToast('Erro ao carregar clubes da série selecionada', 'error');
            
            setTimeout(() => {
                clubSelect.innerHTML = '<option value="">Todos os clubes</option>';
                clubSelect.disabled = false;
            }, 2000);
        });
}

// Form validation
function validateSearchForm() {
    const ageMin = document.getElementById('age_min');
    const ageMax = document.getElementById('age_max');
    
    if (ageMin && ageMax && ageMin.value && ageMax.value) {
        const minAge = parseInt(ageMin.value);
        const maxAge = parseInt(ageMax.value);
        
        if (minAge > maxAge) {
            showToast('Idade mínima não pode ser maior que a máxima', 'error');
            ageMin.focus();
            return false;
        }
        
        if (minAge < 16 || maxAge > 50) {
            showToast('Idade deve estar entre 16 e 50 anos', 'error');
            return false;
        }
    }
    
    return true;
}

// Show form loading state
function showFormLoading(isLoading) {
    const submitBtn = document.querySelector('#searchForm button[type="submit"]');
    if (!submitBtn) return;
    
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> <span class="d-none d-sm-inline">Buscando...</span>';
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-search"></i> <span class="d-none d-sm-inline">Buscar</span>';
    }
}

// Mobile optimizations
function initializeMobileOptimizations() {
    // Touch-friendly interactions
    addTouchFeedback();
    
    // Optimize scrolling performance
    optimizeScrolling();
    
    // Handle orientation changes
    handleOrientationChange();
    
    // Lazy loading for images (if any)
    initializeLazyLoading();
}

// Add touch feedback for better mobile UX
function addTouchFeedback() {
    const clickableElements = document.querySelectorAll('.btn, .card, .nav-link, .page-link');
    
    clickableElements.forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        element.addEventListener('touchend', function() {
            this.style.transform = '';
        });
        
        element.addEventListener('touchcancel', function() {
            this.style.transform = '';
        });
    });
}

// Optimize scrolling performance
function optimizeScrolling() {
    let ticking = false;
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(function() {
                // Handle scroll-based animations or effects here
                updateScrollProgress();
                ticking = false;
            });
            ticking = true;
        }
    });
}

// Update scroll progress indicator (if needed)
function updateScrollProgress() {
    const scrollTop = window.pageYOffset;
    const docHeight = document.body.offsetHeight - window.innerHeight;
    const scrollPercent = scrollTop / docHeight * 100;
    
    // Update progress bar if exists
    const progressBar = document.getElementById('scrollProgress');
    if (progressBar) {
        progressBar.style.width = scrollPercent + '%';
    }
}

// Handle orientation changes
function handleOrientationChange() {
    window.addEventListener('orientationchange', function() {
        // Delay to ensure viewport is updated
        setTimeout(() => {
            // Trigger any necessary layout updates
            window.dispatchEvent(new Event('resize'));
        }, 100);
    });
}

// Lazy loading for images
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('loading');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Accessibility improvements
function initializeAccessibility() {
    // Skip link functionality
    addSkipLinks();
    
    // Keyboard navigation
    improveKeyboardNavigation();
    
    // Screen reader announcements
    initializeAriaLive();
    
    // Focus management
    manageFocus();
}

// Add skip links for accessibility
function addSkipLinks() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Pular para o conteúdo principal';
    skipLink.className = 'sr-only sr-only-focusable btn btn-primary';
    skipLink.style.position = 'absolute';
    skipLink.style.top = '10px';
    skipLink.style.left = '10px';
    skipLink.style.zIndex = '9999';
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

// Improve keyboard navigation
function improveKeyboardNavigation() {
    // Add keyboard support for custom elements
    document.addEventListener('keydown', function(e) {
        // Handle Enter key on clickable elements
        if (e.key === 'Enter') {
            const target = e.target;
            if (target.classList.contains('clickable') || target.dataset.clickable) {
                target.click();
            }
        }
        
        // Handle Escape key to close modals/dropdowns
        if (e.key === 'Escape') {
            // Close any open Bootstrap modals
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
            });
            
            // Close any open dropdowns
            const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
            openDropdowns.forEach(dropdown => {
                const toggle = dropdown.previousElementSibling;
                if (toggle) {
                    const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
                    if (bsDropdown) bsDropdown.hide();
                }
            });
        }
    });
}

// Initialize ARIA live regions for announcements
function initializeAriaLive() {
    // Create live region for status messages
    const liveRegion = document.createElement('div');
    liveRegion.id = 'aria-live-status';
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    document.body.appendChild(liveRegion);
}

// Announce message to screen readers
function announceToScreenReader(message) {
    const liveRegion = document.getElementById('aria-live-status');
    if (liveRegion) {
        liveRegion.textContent = message;
    }
}

// Focus management
function manageFocus() {
    // Store last focused element before navigation
    let lastFocusedElement = null;
    
    document.addEventListener('focusin', function(e) {
        lastFocusedElement = e.target;
    });
    
    // Restore focus after page loads
    window.addEventListener('pageshow', function() {
        // Focus first interactive element if no hash
        if (!window.location.hash) {
            const firstInput = document.querySelector('input, select, textarea, button');
            if (firstInput) {
                firstInput.focus();
            }
        }
    });
}

// Performance optimizations
function initializePerformance() {
    // Debounce resize events
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(handleResize, 250);
    });
    
    // Preload critical resources
    preloadCriticalResources();
    
    // Initialize service worker (if needed)
    if ('serviceWorker' in navigator) {
        // Register service worker for offline functionality
        // navigator.serviceWorker.register('/sw.js');
    }
}

// Handle window resize
function handleResize() {
    // Update any size-dependent calculations
    updateResponsiveElements();
}

// Update responsive elements
function updateResponsiveElements() {
    // Update any elements that need recalculation on resize
    const cards = document.querySelectorAll('.player-card');
    cards.forEach(card => {
        // Ensure equal heights in grid
        card.style.height = 'auto';
    });
}

// Preload critical resources
function preloadCriticalResources() {
    // Preload critical CSS if not already loaded
    const criticalCSS = [
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css'
    ];
    
    criticalCSS.forEach(href => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'style';
        link.href = href;
        document.head.appendChild(link);
    });
}

// Toast notification system
function showToast(message, type = 'info', duration = 3000) {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="bi bi-${getToastIcon(type)} text-${getToastColor(type)} me-2"></i>
                <strong class="me-auto">Notificação</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        delay: duration
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
    
    // Announce to screen readers
    announceToScreenReader(message);
}

// Get toast icon based on type
function getToastIcon(type) {
    const icons = {
        'info': 'info-circle',
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'error': 'x-circle'
    };
    return icons[type] || icons.info;
}

// Get toast color based on type
function getToastColor(type) {
    const colors = {
        'info': 'primary',
        'success': 'success',
        'warning': 'warning',
        'error': 'danger'
    };
    return colors[type] || colors.info;
}

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for global access
window.Brasileirao = {
    showToast,
    announceToScreenReader,
    loadClubsForSerie
};
