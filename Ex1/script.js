const popup = document.createElement('div');
popup.classList.add('image-popup');
document.body.appendChild(popup);

// Add click handlers to rows
const resource_rows = document.querySelectorAll('.resource-row');

resource_rows.forEach(function(row) {
    row.addEventListener('mousedown', function(e) {
        // Get URL from dataset
        const imageUrl = this.dataset.fullUrl;
        const type = this.dataset.type;

        // Create and show resource in popup
        if (type === 'IMAGE') {
            popup.innerHTML = `<img src="${imageUrl}" alt="Preview">`;
        } else if (type === 'VIDEO') {
            popup.innerHTML = `<video src="${imageUrl}" autoplay controls></video>`;
        }
        
        // Make popup visible to calculate its dimensions
        popup.style.display = 'block';
        
        // Calculate positions
        const popupHeight = popup.offsetHeight;
        const popupWidth = popup.offsetWidth;
        const windowHeight = window.innerHeight;
        const windowWidth = window.innerWidth;
        
        // Calculate left position
        let leftPos = e.pageX + 10;
        if (leftPos + popupWidth > windowWidth) {
            leftPos = windowWidth - popupWidth - 10;
        }
        
        // Calculate top position
        let topPos = e.pageY + 10;
        if (topPos + popupHeight > windowHeight) {
            topPos = e.pageY - popupHeight - 10; // Show above cursor if not enough space below
        }
        
        // Apply calculated positions
        popup.style.left = `${leftPos}px`;
        popup.style.top = `${topPos}px`;
    });

    // Hide popup when mouse is released
    row.addEventListener('mouseup', function() {
        popup.style.display = 'none';
    });

    // Also hide popup if mouse leaves the row while held down
    row.addEventListener('mouseleave', function() {
        popup.style.display = 'none';
    });
});

// Prevent text selection while dragging
resource_rows.forEach(row => {
    row.addEventListener('mousedown', e => e.preventDefault());
});