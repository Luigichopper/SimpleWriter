"""
Word Count Extension for Novel Writer
Tracks and displays word, character, and page counts for chapters and the entire book.
"""

def init_extension():
    """Initialize the extension."""
    return {
        "name": "Word Count",
        "version": "1.0.0",
        "description": "Tracks and displays word counts for chapters and the entire book",
        "author": "Novel Writer"
    }

def on_load():
    """Called when the extension is loaded."""
    print("Word Count extension loaded!")

def get_css():
    """Return the CSS for the word count UI."""
    return """
    .word-count-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: var(--card-bg);
        border-top: 1px solid var(--border-color);
        padding: 8px 15px;
        font-size: 12px;
        color: var(--text-color);
        display: flex;
        justify-content: space-between;
        z-index: 100;
    }
    
    .word-count-item {
        margin-right: 20px;
        display: inline-block;
    }
    
    .word-count-label {
        font-weight: bold;
        margin-right: 5px;
    }
    
    .word-count-value {
        font-family: monospace;
    }
    
    .word-count-toggle {
        cursor: pointer;
        margin-left: auto;
        display: flex;
        align-items: center;
    }
    
    .word-count-toggle:hover {
        color: var(--primary-color);
    }
    
    .word-count-settings {
        padding-left: 10px;
        cursor: pointer;
    }
    
    .word-count-settings:hover {
        color: var(--primary-color);
    }
    
    .word-count-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        display: none;
        align-items: center;
        justify-content: center;
    }
    
    .word-count-modal-content {
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 8px;
        width: 400px;
        max-width: 90%;
    }
    
    .word-count-modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 10px;
    }
    
    .word-count-modal-title {
        font-size: 18px;
        font-weight: bold;
    }
    
    .word-count-close {
        cursor: pointer;
        font-size: 20px;
    }
    
    .word-count-stats-container {
        margin-bottom: 20px;
    }
    
    .word-count-stat-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid var(--border-color);
    }
    
    .word-count-stat-heading {
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 5px;
        color: var(--primary-color);
    }
    
    .word-count-stat-name {
        font-weight: 500;
    }
    
    .word-count-stat-value {
        font-family: monospace;
    }
    
    .word-count-options {
        margin-top: 20px;
    }
    
    .word-count-form-group {
        margin-bottom: 10px;
    }
    
    .word-count-form-group label {
        display: block;
        margin-bottom: 5px;
    }
    
    .word-count-form-control {
        width: 100%;
        padding: 5px 10px;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    .word-count-btn {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 10px;
    }
    
    .word-count-btn:hover {
        background-color: var(--secondary-color);
    }
    
    .word-count-goals {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid var(--border-color);
    }
    
    .word-count-goals-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .word-count-goals-title {
        font-weight: bold;
    }
    
    .word-count-progress {
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 4px;
        margin-top: 5px;
        overflow: hidden;
    }
    
    .word-count-progress-bar {
        height: 100%;
        background-color: var(--primary-color);
        transition: width 0.3s ease;
    }
    
    .word-count-progress-text {
        font-size: 11px;
        text-align: right;
        margin-top: 2px;
    }
    
    .word-count-minimized {
        padding: 5px 10px;
        display: none;
    }
    """

def get_js():
    """Return the JavaScript for word count functionality."""
    return """
    // Create word count panel
    const wordCountPanel = document.createElement('div');
    wordCountPanel.className = 'word-count-panel';
    wordCountPanel.innerHTML = `
        <div class="word-count-stats">
            <span class="word-count-item">
                <span class="word-count-label">Words:</span>
                <span class="word-count-value" id="wordCountValue">0</span>
            </span>
            <span class="word-count-item">
                <span class="word-count-label">Characters:</span>
                <span class="word-count-value" id="charCountValue">0</span>
            </span>
            <span class="word-count-item">
                <span class="word-count-label">Pages:</span>
                <span class="word-count-value" id="pageCountValue">0</span>
            </span>
        </div>
        <div class="word-count-minimized" id="wordCountMinimized">
            <span class="word-count-value" id="wordCountMinValue">0</span> words
        </div>
        <div class="word-count-toggle" id="wordCountToggle">
            <i class="fas fa-chevron-down"></i>
        </div>
        <div class="word-count-settings" id="wordCountSettings">
            <i class="fas fa-chart-bar"></i>
        </div>
    `;
    document.body.appendChild(wordCountPanel);
    
    // Create word count modal
    const wordCountModal = document.createElement('div');
    wordCountModal.className = 'word-count-modal';
    wordCountModal.id = 'wordCountModal';
    wordCountModal.innerHTML = `
        <div class="word-count-modal-content">
            <div class="word-count-modal-header">
                <div class="word-count-modal-title">Word Count Statistics</div>
                <span class="word-count-close">&times;</span>
            </div>
            <div class="word-count-stats-container" id="wordCountStatsContainer">
                <div class="word-count-stat-heading">Current Chapter</div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Words:</span>
                    <span class="word-count-stat-value" id="chapterWordCount">0</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Characters:</span>
                    <span class="word-count-stat-value" id="chapterCharCount">0</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Pages (est.):</span>
                    <span class="word-count-stat-value" id="chapterPageCount">0</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Reading Time:</span>
                    <span class="word-count-stat-value" id="chapterReadingTime">0 min</span>
                </div>
                
                <div class="word-count-stat-heading">Entire Book</div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Words:</span>
                    <span class="word-count-stat-value" id="bookWordCount">0</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Characters:</span>
                    <span class="word-count-stat-value" id="bookCharCount">0</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Pages (est.):</span>
                    <span class="word-count-stat-value" id="bookPageCount">0</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Reading Time:</span>
                    <span class="word-count-stat-value" id="bookReadingTime">0 min</span>
                </div>
                <div class="word-count-stat-row">
                    <span class="word-count-stat-name">Chapters:</span>
                    <span class="word-count-stat-value" id="bookChapterCount">0</span>
                </div>
            </div>
            
            <div class="word-count-goals">
                <div class="word-count-goals-header">
                    <div class="word-count-goals-title">Writing Goals</div>
                </div>
                <div class="word-count-form-group">
                    <label for="wordCountGoal">Word Count Goal</label>
                    <input type="number" id="wordCountGoal" class="word-count-form-control" placeholder="e.g., 50000">
                </div>
                <div id="wordCountGoalProgress" style="display: none;">
                    <div class="word-count-progress">
                        <div class="word-count-progress-bar" id="wordCountProgressBar" style="width: 0%;"></div>
                    </div>
                    <div class="word-count-progress-text">
                        <span id="wordCountProgressText">0 / 0 words (0%)</span>
                    </div>
                </div>
                <button class="word-count-btn" id="saveWordCountGoal">Save Goal</button>
            </div>
        </div>
    `;
    document.body.appendChild(wordCountModal);
    
    // Variables for word count tracking
    let isPanelMinimized = false;
    let wordsPerPage = 250; // Standard estimate
    let wordCountGoal = 0;
    
    // Load saved preferences
    function loadWordCountPreferences() {
        const savedGoal = localStorage.getItem('wordCountGoal');
        if (savedGoal) {
            wordCountGoal = parseInt(savedGoal, 10);
            document.getElementById('wordCountGoal').value = wordCountGoal;
            updateGoalProgress();
        }
        
        const isPanelMinimizedSaved = localStorage.getItem('wordCountPanelMinimized');
        if (isPanelMinimizedSaved === 'true') {
            minimizePanel();
        }
    }
    
    // Calculate word count from text
    function countWords(text) {
        if (!text || text.trim() === '') return 0;
        // First clean up HTML tags
        const cleanText = text.replace(/<[^>]*>/g, ' ');
        // Then count words
        return cleanText.trim().split(/\\s+/).filter(word => word.length > 0).length;
    }
    
    // Calculate character count
    function countCharacters(text) {
        if (!text || text.trim() === '') return 0;
        // First clean up HTML tags
        const cleanText = text.replace(/<[^>]*>/g, ' ');
        // Then count characters (excluding whitespace)
        return cleanText.replace(/\\s+/g, '').length;
    }
    
    // Calculate reading time in minutes
    function calculateReadingTime(wordCount) {
        const wordsPerMinute = 200; // Average reading speed
        return Math.max(1, Math.round(wordCount / wordsPerMinute));
    }
    
    // Update word counts for current chapter
    function updateWordCount() {
        if (!editorElement) return;
        
        // Get content for the current chapter
        const content = editorElement.innerHTML || '';
        
        // Calculate counts
        const wordCount = countWords(content);
        const charCount = countCharacters(content);
        const pageCount = Math.max(1, Math.round(wordCount / wordsPerPage * 10) / 10);
        
        // Update display
        document.getElementById('wordCountValue').textContent = wordCount.toLocaleString();
        document.getElementById('charCountValue').textContent = charCount.toLocaleString();
        document.getElementById('pageCountValue').textContent = pageCount.toFixed(1);
        document.getElementById('wordCountMinValue').textContent = wordCount.toLocaleString();
        
        // Update modal stats for current chapter
        document.getElementById('chapterWordCount').textContent = wordCount.toLocaleString();
        document.getElementById('chapterCharCount').textContent = charCount.toLocaleString();
        document.getElementById('chapterPageCount').textContent = pageCount.toFixed(1);
        document.getElementById('chapterReadingTime').textContent = calculateReadingTime(wordCount) + ' min';
        
        // Update book stats
        updateBookStats();
    }
    
    // Update stats for the entire book
    function updateBookStats() {
        if (!book || !book.chapters) return;
        
        // Save current chapter content to book
        if (currentChapterId) {
            saveCurrentChapter();
        }
        
        // Calculate book totals
        let totalWords = 0;
        let totalChars = 0;
        let chaptersWithContent = 0;
        
        for (const chapter of book.chapters) {
            const content = chapter.content || '';
            const chapterWords = countWords(content);
            const chapterChars = countCharacters(content);
            
            totalWords += chapterWords;
            totalChars += chapterChars;
            
            if (chapterWords > 0) {
                chaptersWithContent++;
            }
        }
        
        const totalPages = Math.max(1, Math.round(totalWords / wordsPerPage * 10) / 10);
        const readingTime = calculateReadingTime(totalWords);
        
        // Update modal stats for book
        document.getElementById('bookWordCount').textContent = totalWords.toLocaleString();
        document.getElementById('bookCharCount').textContent = totalChars.toLocaleString();
        document.getElementById('bookPageCount').textContent = totalPages.toFixed(1);
        document.getElementById('bookReadingTime').textContent = readingTime + ' min';
        document.getElementById('bookChapterCount').textContent = book.chapters.length.toString() + 
            (chaptersWithContent < book.chapters.length ? ` (${chaptersWithContent} with content)` : '');
        
        // Update goal progress
        updateGoalProgress(totalWords);
    }
    
    // Update goal progress display
    function updateGoalProgress(totalWords = null) {
        if (!wordCountGoal) {
            document.getElementById('wordCountGoalProgress').style.display = 'none';
            return;
        }
        
        if (totalWords === null) {
            // Calculate book totals if not provided
            if (!book || !book.chapters) return;
            
            totalWords = 0;
            for (const chapter of book.chapters) {
                const content = chapter.content || '';
                totalWords += countWords(content);
            }
        }
        
        // Calculate percentage
        const percentage = Math.min(100, Math.round((totalWords / wordCountGoal) * 100));
        
        // Update progress display
        document.getElementById('wordCountGoalProgress').style.display = 'block';
        document.getElementById('wordCountProgressBar').style.width = percentage + '%';
        document.getElementById('wordCountProgressText').textContent = 
            `${totalWords.toLocaleString()} / ${wordCountGoal.toLocaleString()} words (${percentage}%)`;
    }
    
    // Toggle panel between minimized and expanded states
    function togglePanel() {
        if (isPanelMinimized) {
            // Expand
            document.querySelector('.word-count-stats').style.display = 'block';
            document.getElementById('wordCountMinimized').style.display = 'none';
            document.getElementById('wordCountToggle').innerHTML = '<i class="fas fa-chevron-down"></i>';
            isPanelMinimized = false;
        } else {
            // Minimize
            minimizePanel();
        }
        localStorage.setItem('wordCountPanelMinimized', isPanelMinimized);
    }
    
    function minimizePanel() {
        document.querySelector('.word-count-stats').style.display = 'none';
        document.getElementById('wordCountMinimized').style.display = 'block';
        document.getElementById('wordCountToggle').innerHTML = '<i class="fas fa-chevron-up"></i>';
        isPanelMinimized = true;
    }
    
    // Event Listeners
    
    // Toggle panel
    document.getElementById('wordCountToggle').addEventListener('click', togglePanel);
    
    // Open stats modal
    document.getElementById('wordCountSettings').addEventListener('click', function() {
        updateBookStats();
        document.getElementById('wordCountModal').style.display = 'flex';
    });
    
    // Close modal
    document.querySelector('.word-count-close').addEventListener('click', function() {
        document.getElementById('wordCountModal').style.display = 'none';
    });
    
    // Close modal when clicking outside
    document.getElementById('wordCountModal').addEventListener('click', function(event) {
        if (event.target === this) {
            this.style.display = 'none';
        }
    });
    
    // Save word count goal
    document.getElementById('saveWordCountGoal').addEventListener('click', function() {
        const goalInput = document.getElementById('wordCountGoal');
        const goal = parseInt(goalInput.value, 10);
        
        if (!isNaN(goal) && goal > 0) {
            wordCountGoal = goal;
            localStorage.setItem('wordCountGoal', goal);
            updateGoalProgress();
        } else {
            wordCountGoal = 0;
            localStorage.removeItem('wordCountGoal');
            document.getElementById('wordCountGoalProgress').style.display = 'none';
        }
    });
    
    // Update word count when text changes in the editor
    if (editorElement) {
        editorElement.addEventListener('input', updateWordCount);
        
        // Initial word count
        updateWordCount();
    }
    
    // Update counts when switching chapters
    const originalLoadChapter = window.loadChapter;
    if (typeof originalLoadChapter === 'function') {
        window.loadChapter = function(chapterId) {
            // Call the original function
            originalLoadChapter(chapterId);
            
            // Update word count after a short delay to let the content load
            setTimeout(updateWordCount, 100);
        };
    }
    
    // Load preferences
    loadWordCountPreferences();
    
    // Initial update
    updateWordCount();
    """

def inject_editor(document):
    """Inject the word count CSS and JS into the editor."""
    # Add CSS
    style_tag = document.new_tag('style')
    style_tag.string = get_css()
    document.head.append(style_tag)

    # Add JS
    script_tag = document.new_tag('script')
    script_tag.string = get_js()
    document.body.append(script_tag)

    return document