// Main JavaScript for Gmail Draft Assistant

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Activate the correct tab based on the current URL
    activateNavTab();

    // Add event listener for column input validation
    const columnInputs = document.querySelectorAll('input[maxlength="1"]');
    if (columnInputs) {
        columnInputs.forEach(input => {
            input.addEventListener('input', function() {
                // Convert to uppercase
                this.value = this.value.toUpperCase();
                
                // Ensure it's a valid column letter (A-Z)
                if (this.value && !/^[A-Z]$/.test(this.value)) {
                    this.value = this.value.replace(/[^A-Z]/g, '');
                }
            });
        });
    }

    // Add an event listener to the file input to display the filename
    const fileInput = document.getElementById('csvFile');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name || 'No file selected';
            const fileLabel = this.nextElementSibling;
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
        });
    }
});

// Function to activate the correct navigation tab based on the current URL
function activateNavTab() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        // Remove 'active' class from all links
        link.classList.remove('active');
        
        // Check if the link href matches the current path
        const linkPath = new URL(link.href, window.location.origin).pathname;
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    // Create a temporary textarea element
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'absolute';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    
    // Select and copy the text
    textarea.select();
    let success = false;
    try {
        success = document.execCommand('copy');
    } catch (err) {
        console.error('Failed to copy text:', err);
    }
    
    // Remove the temporary element
    document.body.removeChild(textarea);
    
    return success;
}

// Confirm before leaving the page if there are unsaved changes
window.addEventListener('beforeunload', function(e) {
    // Check if there's a form with the 'data-confirm-leave' attribute
    const form = document.querySelector('form[data-confirm-leave="true"]');
    if (form && form.dataset.hasChanges === 'true') {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Helper function to format a date as MM/DD/YYYY
function formatDate(date) {
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
}

// Helper function to debounce function calls
function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
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
