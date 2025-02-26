"""
Focus Timer Extension for Novel Writer
Adds a Pomodoro-style focus timer to the editor.
"""

def init_extension():
    """Initialize the extension."""
    return {
        "name": "Focus Timer",
        "version": "1.0.0",
        "description": "Adds a Pomodoro-style focus timer to the editor",
        "author": "Novel Writer"
    }

def on_load():
    """Called when the extension is loaded."""
    print("Focus Timer extension loaded!")

def get_css():
    """Return the CSS for the focus timer."""
    return """
    .focus-timer {
        position: fixed;
        top: 70px;
        right: 20px;
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 100;
        width: 200px;
        text-align: center;
    }
    
    .timer-display {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .timer-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    
    .timer-button {
        padding: 5px 10px;
        border: none;
        border-radius: 4px;
        background-color: var(--primary-color);
        color: white;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .timer-button:hover {
        background-color: var(--secondary-color);
    }
    
    .timer-mode {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    
    .timer-mode-button {
        padding: 3px 8px;
        border: 1px solid var(--primary-color);
        border-radius: 4px;
        background-color: transparent;
        color: var(--primary-color);
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
    }
    
    .timer-mode-button.active {
        background-color: var(--primary-color);
        color: white;
    }
    
    .timer-minimize {
        position: absolute;
        top: 5px;
        right: 10px;
        background: none;
        border: none;
        color: var(--text-color);
        cursor: pointer;
        font-size: 12px;
    }
    
    .timer-toggle {
        position: fixed;
        top: 70px;
        right: 20px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--primary-color);
        color: white;
        display: none;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 100;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    """

def get_js():
    """Return the JavaScript for the focus timer."""
    return """
    // Create the focus timer element
    const focusTimer = document.createElement('div');
    focusTimer.className = 'focus-timer';
    focusTimer.innerHTML = `
        <button class="timer-minimize"><i class="fas fa-minus"></i></button>
        <h3>Focus Timer</h3>
        <div class="timer-mode">
            <button class="timer-mode-button active" data-minutes="25">25m</button>
            <button class="timer-mode-button" data-minutes="15">15m</button>
            <button class="timer-mode-button" data-minutes="5">5m</button>
        </div>
        <div class="timer-display">25:00</div>
        <div class="timer-buttons">
            <button class="timer-button" id="startTimer">Start</button>
            <button class="timer-button" id="resetTimer">Reset</button>
        </div>
    `;
    document.body.appendChild(focusTimer);
    
    // Create toggle button (initially hidden)
    const timerToggle = document.createElement('div');
    timerToggle.className = 'timer-toggle';
    timerToggle.innerHTML = '<i class="fas fa-clock"></i>';
    timerToggle.style.display = 'none';
    document.body.appendChild(timerToggle);
    
    // Timer variables
    let timerInterval;
    let timerRunning = false;
    let timerMinutes = 25;
    let timerSeconds = 0;
    let timerDisplay = focusTimer.querySelector('.timer-display');
    
    // Update timer display
    function updateTimerDisplay() {
        const displayMinutes = timerMinutes.toString().padStart(2, '0');
        const displaySeconds = timerSeconds.toString().padStart(2, '0');
        timerDisplay.textContent = `${displayMinutes}:${displaySeconds}`;
    }
    
    // Start timer
    function startTimer() {
        if (timerRunning) {
            // Pause timer
            clearInterval(timerInterval);
            timerRunning = false;
            document.getElementById('startTimer').textContent = 'Resume';
        } else {
            // Start or resume timer
            timerRunning = true;
            document.getElementById('startTimer').textContent = 'Pause';
            
            timerInterval = setInterval(() => {
                // Count down
                if (timerSeconds > 0) {
                    timerSeconds--;
                } else if (timerMinutes > 0) {
                    timerMinutes--;
                    timerSeconds = 59;
                } else {
                    // Timer complete
                    clearInterval(timerInterval);
                    timerRunning = false;
                    document.getElementById('startTimer').textContent = 'Start';
                    
                    // Play notification sound
                    const audio = new Audio('https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3');
                    audio.play();
                    
                    // Show notification
                    if (Notification.permission === 'granted') {
                        new Notification('Timer Complete', {
                            body: 'Your focus session has ended.',
                            icon: 'https://cdn-icons-png.flaticon.com/512/4305/4305692.png'
                        });
                    }
                }
                
                updateTimerDisplay();
            }, 1000);
        }
    }
    
    // Reset timer
    function resetTimer() {
        clearInterval(timerInterval);
        timerRunning = false;
        document.getElementById('startTimer').textContent = 'Start';
        
        // Get the active mode
        const activeMode = focusTimer.querySelector('.timer-mode-button.active');
        timerMinutes = parseInt(activeMode.getAttribute('data-minutes'));
        timerSeconds = 0;
        
        updateTimerDisplay();
    }
    
    // Event listeners
    document.getElementById('startTimer').addEventListener('click', startTimer);
    document.getElementById('resetTimer').addEventListener('click', resetTimer);
    
    // Mode selection
    focusTimer.querySelectorAll('.timer-mode-button').forEach(button => {
        button.addEventListener('click', function() {
            // Update active state
            focusTimer.querySelectorAll('.timer-mode-button').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Update timer
            timerMinutes = parseInt(this.getAttribute('data-minutes'));
            timerSeconds = 0;
            updateTimerDisplay();
            
            // If timer is running, reset it
            if (timerRunning) {
                resetTimer();
            }
        });
    });
    
    // Minimize/maximize timer
    focusTimer.querySelector('.timer-minimize').addEventListener('click', function() {
        focusTimer.style.display = 'none';
        timerToggle.style.display = 'flex';
    });
    
    timerToggle.addEventListener('click', function() {
        focusTimer.style.display = 'block';
        timerToggle.style.display = 'none';
    });
    
    // Request notification permission
    if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
        Notification.requestPermission();
    }
    """

def inject_editor(document):
    """Inject the focus timer CSS and JS into the editor."""
    # Add CSS
    style_tag = document.new_tag('style')
    style_tag.string = get_css()
    document.head.append(style_tag)
    
    # Add JS
    script_tag = document.new_tag('script')
    script_tag.string = get_js()
    document.body.append(script_tag)
    
    return document
