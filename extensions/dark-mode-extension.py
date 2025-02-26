"""
Dark Mode Extension for Novel Writer
Adds a dark mode toggle to the editor.
"""

def init_extension():
    """Initialize the extension."""
    return {
        "name": "Dark Mode",
        "version": "1.0.0",
        "description": "Adds a dark mode toggle to the editor",
        "author": "Novel Writer"
    }

def on_load():
    """Called when the extension is loaded."""
    print("Dark Mode extension loaded!")

def get_css():
    """Return the CSS for dark mode."""
    return """
    body.dark-mode {
        --bg-color: #1a1a1a;
        --text-color: #e0e0e0;
        --card-bg: #2a2a2a;
        --border-color: #444;
    }
    
    .dark-mode-toggle {
        position: fixed;
        bottom: 20px;
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
    }
    
    .dark-mode-toggle:hover {
        transform: scale(1.1);
    }
    """

def get_js():
    """Return the JavaScript for dark mode toggle."""
    return """
    // Add dark mode toggle button
    const darkModeToggle = document.createElement('div');
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    document.body.appendChild(darkModeToggle);
    
    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Add event listener
    darkModeToggle.addEventListener('click', function() {
        if (document.body.classList.contains('dark-mode')) {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
            this.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
            this.innerHTML = '<i class="fas fa-sun"></i>';
        }
    });
    """

def inject_editor(document):
    """Inject the dark mode CSS and JS into the editor."""
    # Add CSS
    style_tag = document.new_tag('style')
    style_tag.string = get_css()
    document.head.append(style_tag)
    
    # Add JS
    script_tag = document.new_tag('script')
    script_tag.string = get_js()
    document.body.append(script_tag)
    
    return document
