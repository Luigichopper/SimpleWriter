# Novel Writer - A Flask-based Writing Application

A sleek, modern, lightweight web application for writers to create, organize, and export novels. Built with Flask, this application offers a distraction-free writing environment with just the right amount of features to enhance your writing process.

![image](https://github.com/user-attachments/assets/e4e0e385-6726-43cb-b39f-640e8fd8c7f0)


## Key Features

### Book Management
- **Multiple Projects**: Create and manage multiple books in a single interface
- **Easy Navigation**: Quickly switch between your writing projects
- **Automatic Saving**: Your work is saved automatically every 30 seconds

### Chapter Organization
- **Flexible Structure**: Create, delete, rename, and reorder chapters
- **Quick Access**: Navigate between chapters with a single click
- **Content Preservation**: All formatting is maintained across sessions

### Rich Text Editor
- **Basic Formatting**: Bold, italic, and underlined text
- **List Support**: Create bullet points and numbered lists
- **Block Quotes**: Format sections as block quotes
- **Clean Formatting**: One-click removal of all text formatting

### Export Options
- **JSON Format**: Export your entire book structure for backup
- **Plain Text**: Export clean, formatted text that works anywhere
- **HTML**: Export beautifully formatted HTML with proper spacing

### Customization
- **Book Settings**: Customize font size and line spacing for each book
- **UI Preferences**: Adjust the interface to your liking
- **Theme Options**: Choose between light and dark themes (via extensions)

### Extension System
- **Modular Design**: Add new features through Python-based extensions
- **Built-in Extensions**: Dark mode, focus timer, and more
- **Custom Extensions**: Create your own extensions to enhance functionality

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository:**
```bash
git clone https://github.com/yourusername/novel-writer.git
cd novel-writer
```

2. **Create and activate a virtual environment (recommended):**
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python main.py
```

5. **Access the application:**
Open your web browser and navigate to: `http://127.0.0.1:5000`

## Usage Guide

### Creating Your First Book
1. From the home screen, click the "New Book" button
2. Enter a title for your book
3. Click "Create Book" to be taken to the editor

### Managing Chapters
- **View a chapter**: Click on any chapter in the sidebar
- **Add a chapter**: Click the "Add Chapter" button at the bottom of the sidebar
- **Rename a chapter**: Click the pencil icon next to the chapter name
- **Delete a chapter**: Click the trash icon next to the chapter name

### Formatting Your Text
Use the toolbar above the editor for formatting:
- **B**: Bold text
- **I**: Italic text
- **U**: Underline text
- **•**: Bullet points
- **1.**: Numbered lists
- **"**: Block quotes
- **T**: Reset text formatting

### Saving Your Work
- Your work is saved automatically every 30 seconds
- Click the "Save" button in the top bar to save manually

### Exporting Your Book
1. Click the "Export" dropdown in the top menu
2. Choose your preferred format:
   - **JSON**: For backup and importing back into the application
   - **Text**: Plain text format with Markdown-style headings
   - **HTML**: Formatted HTML with proper spacing and styles

### Customizing Book Settings
1. Click the "Settings" gear icon in the top menu
2. Adjust font size and line spacing
3. Click "Save Settings" to apply changes

### Using Extensions
The application comes with two built-in extensions:

#### Dark Mode
- Automatically applies a dark theme to reduce eye strain
- Toggle between light and dark mode with a floating button

#### Focus Timer
- Pomodoro-style timer to help maintain writing focus
- Set 5, 15, or 25 minute focus sessions
- Get a notification when your session is complete

## Creating Your Own Extensions

Extensions are Python files that enhance the functionality of the application. Here's how to create a basic extension:

### Basic Extension Structure

```python
def init_extension():
    """Return extension metadata."""
    return {
        "name": "My Extension",
        "version": "1.0.0",
        "description": "Description of what your extension does",
        "author": "Your Name"
    }

def on_load():
    """Called when the extension is loaded."""
    print("My extension loaded!")

def get_css():
    """Return CSS to be injected into the editor."""
    return """
    /* Your CSS here */
    """

def get_js():
    """Return JavaScript to be injected into the editor."""
    return """
    // Your JavaScript here
    """

def inject_editor(document):
    """
    Modify the editor HTML.
    document: BeautifulSoup document representing the editor
    return: Modified BeautifulSoup document
    """
    # Add CSS
    style_tag = document.new_tag('style')
    style_tag.string = get_css()
    document.head.append(style_tag)
    
    # Add JavaScript
    script_tag = document.new_tag('script')
    script_tag.string = get_js()
    document.body.append(script_tag)
    
    return document
```

### Installing Your Extension
1. Save your extension file with a `.py` extension
2. Place it in the `extensions` folder of the application
3. Restart the application (or upload through the Extensions tab)
4. Activate your extension in the Extensions tab

## Project Structure

```
novel-writer/
│
├── main.py                # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This documentation file
│
├── books/                # Directory for storing books
│   └── *.json            # Book data files
│
├── extensions/           # Extension modules
│   ├── dark_mode.py      # Dark mode extension
│   └── focus_timer.py    # Focus timer extension
│
├── templates/            # HTML templates
│   ├── index.html        # Home page template
│   └── edit.html         # Editor template
│
└── static/               # Static assets (if needed)
    ├── css/              # CSS files
    └── js/               # JavaScript files
```

## Troubleshooting

### Common Issues

#### "Template Not Found" Error
- Make sure your `templates` directory exists at the root of the project
- Check that `index.html` and `edit.html` are in the templates directory

#### Extensions Not Working
- Ensure you have `beautifulsoup4` installed: `pip install beautifulsoup4`
- Check that your extension has an `inject_editor` function
- Restart the application after adding or modifying extensions

#### Chapter Creation Issues
- If creating a chapter doesn't immediately display, don't worry - it's being saved
- Click the "Save" button or refresh the page to see your new chapter

## Future Enhancements

- **Word Count**: Track your writing progress with word and character counts
- **Search**: Find text within your book
- **Images**: Support for adding images to your book
- **Offline Mode**: Work without an internet connection
- **Collaboration**: Share and collaborate on books with other users

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Flask, a lightweight Python web framework
- Uses modern web technologies for a responsive UI
- Inspired by distraction-free writing applications

---

*Happy Writing!*
