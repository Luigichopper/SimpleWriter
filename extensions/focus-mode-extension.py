"""
Focus Mode Extension for Novel Writer
Provides a distraction-free writing environment by hiding non-essential interface elements
and enabling fullscreen mode for complete immersion.
"""

def init_extension():
    """Initialize the extension."""
    return {
        "name": "Focus Mode",
        "version": "1.1.0",
        "description": "Toggle distraction-free writing mode with fullscreen",
        "author": "Novel Writer"
    }

def on_load():
    """Called when the extension is loaded."""
    print("Focus Mode extension loaded!")

def get_css():
    """Return the CSS for focus mode."""
    return """
    /* Focus mode styles */
    body.focus-mode .sidebar {
        display: none !important;
    }
    
    body.focus-mode .toolbar {
        opacity: 0.2;
        transition: opacity 0.3s;
    }
    
    body.focus-mode .toolbar:hover {
        opacity: 1;
    }
    
    body.focus-mode header {
        opacity: 0.2;
        transition: opacity 0.3s;
    }
    
    body.focus-mode header:hover {
        opacity: 1;
    }
    
    body.focus-mode .editor {
        margin: 0 auto;
    }
    
    body.focus-mode .content-editable {
        max-width: 650px;
        margin: 0 auto;
        padding: 40px;
    }
    
    /* Special styles for true fullscreen */
    body.focus-mode.fullscreen .editor-area {
        padding-top: 40px;
    }
    
    .focus-toggle {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--primary-color);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 100;
        transition: transform 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .focus-toggle:hover {
        transform: scale(1.1);
    }
    
    /* Notification when entering focus mode */
    .focus-notification {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 15px 25px;
        border-radius: 30px;
        font-size: 16px;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.5s;
        pointer-events: none;
    }
    
    .focus-notification.show {
        opacity: 1;
    }
    
    /* ESC hint tooltip */
    .esc-hint {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.5s, visibility 0.5s;
        visibility: hidden;
    }
    
    .esc-hint.show {
        opacity: 1;
        visibility: visible;
    }
    """

def get_js():
    """Return the JavaScript for focus mode toggle with fullscreen support."""
    return """
    // Add focus mode toggle button
    const focusToggle = document.createElement('div');
    focusToggle.className = 'focus-toggle';
    focusToggle.innerHTML = '<i class="fas fa-compress"></i>';
    focusToggle.title = 'Toggle Focus Mode';
    document.body.appendChild(focusToggle);
    
    // Create notification element
    const focusNotification = document.createElement('div');
    focusNotification.className = 'focus-notification';
    document.body.appendChild(focusNotification);
    
    // Create ESC hint
    const escHint = document.createElement('div');
    escHint.className = 'esc-hint';
    escHint.textContent = 'Press ESC to exit fullscreen';
    document.body.appendChild(escHint);
    
    // Fullscreen API check
    const fullscreenAvailable = 
        document.documentElement.requestFullscreen || 
        document.documentElement.webkitRequestFullscreen || 
        document.documentElement.mozRequestFullScreen || 
        document.documentElement.msRequestFullscreen;
    
    // Fullscreen functions with vendor prefixes
    function requestFullscreen(element) {
        if (element.requestFullscreen) {
            return element.requestFullscreen();
        } else if (element.webkitRequestFullscreen) {
            return element.webkitRequestFullscreen();
        } else if (element.mozRequestFullScreen) {
            return element.mozRequestFullScreen();
        } else if (element.msRequestFullscreen) {
            return element.msRequestFullscreen();
        }
        return Promise.reject('Fullscreen API not supported');
    }
    
    function exitFullscreen() {
        if (document.exitFullscreen) {
            return document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            return document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            return document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            return document.msExitFullscreen();
        }
        return Promise.reject('Fullscreen API not supported');
    }
    
    function isFullscreen() {
        return !!(
            document.fullscreenElement ||
            document.webkitFullscreenElement ||
            document.mozFullScreenElement ||
            document.msFullscreenElement
        );
    }
    
    // Show notification
    function showNotification(message, duration = 2000) {
        focusNotification.textContent = message;
        focusNotification.classList.add('show');
        
        setTimeout(() => {
            focusNotification.classList.remove('show');
        }, duration);
    }
    
    // Show ESC hint briefly
    function showEscHint() {
        escHint.classList.add('show');
        
        setTimeout(() => {
            escHint.classList.remove('show');
        }, 3000);
    }
    
    // Toggle focus mode
    function toggleFocusMode() {
        if (document.body.classList.contains('focus-mode')) {
            // Disable focus mode
            document.body.classList.remove('focus-mode');
            document.body.classList.remove('fullscreen');
            localStorage.setItem('focusMode', 'disabled');
            focusToggle.innerHTML = '<i class="fas fa-compress"></i>';
            focusToggle.title = 'Enter Focus Mode';
            
            // Exit fullscreen if we're in it
            if (isFullscreen()) {
                exitFullscreen().catch(error => {
                    console.warn('Error exiting fullscreen:', error);
                });
            }
            
            showNotification('Focus mode disabled');
        } else {
            // Enable focus mode
            document.body.classList.add('focus-mode');
            localStorage.setItem('focusMode', 'enabled');
            focusToggle.innerHTML = '<i class="fas fa-expand"></i>';
            focusToggle.title = 'Exit Focus Mode';
            
            // Try to enter fullscreen
            if (fullscreenAvailable) {
                requestFullscreen(document.documentElement)
                    .then(() => {
                        document.body.classList.add('fullscreen');
                        showNotification('Focus mode enabled - Fullscreen activated');
                        showEscHint();
                    })
                    .catch(error => {
                        console.warn('Error enabling fullscreen:', error);
                        showNotification('Focus mode enabled - Distractions hidden');
                    });
            } else {
                showNotification('Focus mode enabled - Distractions hidden');
            }
        }
    }
    
    // Check for saved focus mode preference
    if (localStorage.getItem('focusMode') === 'enabled') {
        document.body.classList.add('focus-mode');
        focusToggle.innerHTML = '<i class="fas fa-expand"></i>';
        focusToggle.title = 'Exit Focus Mode';
        
        // Don't automatically enter fullscreen on page load
        // as browsers typically block this without user interaction
    }
    
    // Add event listener to button
    focusToggle.addEventListener('click', toggleFocusMode);
    
    // Add keyboard shortcut (F11 or Alt+F)
    document.addEventListener('keydown', function(e) {
        // F11 or Alt+F
        if (e.key === 'F11' || (e.altKey && e.key === 'f')) {
            e.preventDefault(); // Prevent default browser behavior for F11
            toggleFocusMode();
        }
    });
    
    // Listen for fullscreen change events
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
    document.addEventListener('mozfullscreenchange', handleFullscreenChange);
    document.addEventListener('MSFullscreenChange', handleFullscreenChange);
    
    function handleFullscreenChange() {
        // If we exit fullscreen but focus mode is still on
        if (!isFullscreen() && document.body.classList.contains('fullscreen')) {
            document.body.classList.remove('fullscreen');
        }
    }
    """

def inject_editor(document):
    """Inject the focus mode CSS and JS into the editor."""
    # Only inject on the editor page, not on other pages
    if document.select('.editor-container'):
        # Add CSS
        style_tag = document.new_tag('style')
        style_tag.string = get_css()
        document.head.append(style_tag)

        # Add JS
        script_tag = document.new_tag('script')
        script_tag.string = get_js()
        document.body.append(script_tag)

    return document