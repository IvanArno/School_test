// Lightbox functionality
document.addEventListener('DOMContentLoaded', function() {
    const lightboxModal = document.getElementById('lightbox-modal');
    const lightboxImage = document.getElementById('lightbox-image');
    const closeBtn = lightboxModal.querySelector('span');
    
    // Add click listeners to all photo and poster images
    const images = document.querySelectorAll('.photo-image, .card img[src*="/media/"]');
    
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function(e) {
            if (e.target.closest('a')) return; // Don't open lightbox if clicking a link
            lightboxImage.src = this.src;
            lightboxModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });
    
    // Close lightbox
    closeBtn.addEventListener('click', closeLightbox);
    lightboxModal.addEventListener('click', function(e) {
        if (e.target === lightboxModal) {
            closeLightbox();
        }
    });
    
    function closeLightbox() {
        lightboxModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    });
});
