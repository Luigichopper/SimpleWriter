from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import json
import os
import uuid
from datetime import datetime
import importlib.util
import sys
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

# Create the Flask application
app = Flask(__name__,
            template_folder='templates',  # Explicitly set template folder
            static_folder='static')  # Explicitly set static folder

app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'extensions'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max-limit for extensions

# Ensure required directories exist
required_dirs = ['extensions', 'books', 'templates', 'static']
for directory in required_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


# Store active extensions - persisted to JSON
def get_active_extensions():
    if os.path.exists('active_extensions.json'):
        try:
            with open('active_extensions.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_active_extensions(active_ext):
    with open('active_extensions.json', 'w') as f:
        json.dump(active_ext, f)


# Initialize active extensions
active_extensions = get_active_extensions()


# Initialize extensions
def load_extensions():
    extensions = {}
    if os.path.exists('extensions'):
        for filename in os.listdir('extensions'):
            if filename.endswith('.py'):
                try:
                    module_name = filename[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join('extensions', filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'init_extension'):
                        extensions[module_name] = module
                except Exception as e:
                    print(f"Failed to load extension {filename}: {e}")
    return extensions


# Apply extensions to HTML
def apply_extensions(html):
    try:
        # Only proceed if we have BeautifulSoup and active extensions
        if active_extensions:
            soup = BeautifulSoup(html, 'html.parser')

            # Get all loaded extensions
            extensions = load_extensions()

            for ext_name, is_active in active_extensions.items():
                if is_active and ext_name in extensions:
                    ext_module = extensions[ext_name]
                    if hasattr(ext_module, 'inject_editor'):
                        try:
                            soup = ext_module.inject_editor(soup)
                        except Exception as e:
                            print(f"Error applying extension {ext_name}: {e}")

            return str(soup)
    except Exception as e:
        print(f"Error in apply_extensions: {e}")

    # Return original if any errors or no extensions
    return html


# Get available books
def get_books():
    books = []
    if os.path.exists('books'):
        for filename in os.listdir('books'):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join('books', filename), 'r') as f:
                        book = json.load(f)
                        books.append({
                            'id': book.get('id', filename[:-5]),
                            'title': book.get('title', 'Untitled'),
                            'last_modified': book.get('last_modified', '')
                        })
                except Exception as e:
                    print(f"Error loading book {filename}: {e}")
    return books


# Create a new book
def create_book(title):
    book_id = str(uuid.uuid4())
    book = {
        'id': book_id,
        'title': title,
        'chapters': [
            {
                'id': str(uuid.uuid4()),
                'title': 'Chapter 1',
                'content': '',
                'order': 0
            }
        ],
        'settings': {
            'font_size': 16,
            'line_spacing': 1.5,
            'theme': 'light'
        },
        'planning': {
            'notes': [],
            'characters': [],
            'timeline': []
        },
        'last_modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(os.path.join('books', f"{book_id}.json"), 'w') as f:
        json.dump(book, f, indent=4)

    return book_id


# Get a book by ID
def get_book(book_id):
    try:
        with open(os.path.join('books', f"{book_id}.json"), 'r') as f:
            book = json.load(f)

            # Ensure planning structure exists for backward compatibility
            if 'planning' not in book:
                book['planning'] = {
                    'notes': [],
                    'characters': [],
                    'timeline': []
                }

            return book
    except:
        return None


# Save a book
def save_book(book):
    book['last_modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(os.path.join('books', f"{book['id']}.json"), 'w') as f:
        json.dump(book, f, indent=4)


# Routes
@app.route('/')
def index():
    books = get_books()
    extensions = load_extensions()
    return render_template('index.html', books=books, extensions=extensions, active_extensions=active_extensions)


@app.route('/book/new', methods=['POST'])
def new_book():
    title = request.form.get('title', 'Untitled Book')
    book_id = create_book(title)
    return redirect(url_for('edit_book', book_id=book_id))


@app.route('/book/<book_id>')
def edit_book(book_id):
    book = get_book(book_id)
    if not book:
        return redirect(url_for('index'))

    extensions = load_extensions()
    html = render_template('edit.html', book=book, extensions=extensions, active_extensions=active_extensions)

    # Apply extensions to the HTML
    modified_html = apply_extensions(html)

    return modified_html


@app.route('/book/<book_id>/planning')
def book_planning(book_id):
    book = get_book(book_id)
    if not book:
        return redirect(url_for('index'))

    extensions = load_extensions()
    html = render_template('planning.html', book=book, extensions=extensions, active_extensions=active_extensions)

    # Apply extensions to the HTML
    modified_html = apply_extensions(html)

    return modified_html


@app.route('/api/book/<book_id>', methods=['GET'])
def api_get_book(book_id):
    book = get_book(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book)


@app.route('/api/book/<book_id>', methods=['POST'])
def api_save_book(book_id):
    try:
        book = request.json
        if not book:
            return jsonify({'error': 'Invalid book data'}), 400

        save_book(book)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving book: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/book/<book_id>/chapter/new', methods=['POST'])
def api_new_chapter(book_id):
    try:
        book = get_book(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Get chapter data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400

        title = data.get('title', f"Chapter {len(book['chapters']) + 1}")

        chapter = {
            'id': str(uuid.uuid4()),
            'title': title,
            'content': '',
            'order': len(book['chapters'])
        }

        book['chapters'].append(chapter)
        save_book(book)

        return jsonify(chapter)
    except Exception as e:
        print(f"Error creating chapter: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/book/<book_id>/chapter/<chapter_id>', methods=['DELETE'])
def api_delete_chapter(book_id, chapter_id):
    try:
        book = get_book(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        book['chapters'] = [c for c in book['chapters'] if c['id'] != chapter_id]
        # Reorder chapters
        for i, chapter in enumerate(book['chapters']):
            chapter['order'] = i

        save_book(book)

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting chapter: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/book/<book_id>/export/<format>')
def export_book(book_id, format):
    book = get_book(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    filename = f"{book['title'].replace(' ', '_')}.{format}"
    temp_filename = f"temp_{filename}"

    try:
        if format == 'json':
            with open(temp_filename, 'w', encoding='utf-8') as f:
                json.dump(book, f, indent=4)
            return send_file(temp_filename, as_attachment=True, download_name=filename)

        elif format == 'txt':
            with open(temp_filename, 'w', encoding='utf-8') as f:
                f.write(f"# {book['title']}\n\n")
                for chapter in sorted(book['chapters'], key=lambda x: x['order']):
                    f.write(f"## {chapter['title']}\n\n")
                    # Strip HTML tags for plain text
                    content = BeautifulSoup(chapter['content'], 'html.parser').get_text()
                    f.write(f"{content}\n\n")
            return send_file(temp_filename, as_attachment=True, download_name=filename)

        elif format == 'html':
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{book['title']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: {book['settings'].get('line_spacing', 1.5)};
            font-size: {book['settings'].get('font_size', 16)}px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 40px;
        }}
        h2 {{
            margin-top: 30px;
            margin-bottom: 20px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }}
        .chapter-content {{
            white-space: pre-wrap;
            margin-bottom: 30px;
        }}
        p {{
            margin-bottom: 1em;
        }}
        ul, ol {{
            margin-left: 20px;
            margin-bottom: 1em;
        }}
        blockquote {{
            border-left: 3px solid #ccc;
            margin-left: 20px;
            padding-left: 15px;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>{book['title']}</h1>
"""

            for chapter in sorted(book['chapters'], key=lambda x: x['order']):
                html += f"    <h2>{chapter['title']}</h2>\n"
                html += f'    <div class="chapter-content">{chapter["content"]}</div>\n\n'

            html += """</body>
</html>"""

            with open(temp_filename, 'w', encoding='utf-8') as f:
                f.write(html)
            return send_file(temp_filename, as_attachment=True, download_name=filename)

        return jsonify({'error': 'Invalid format'}), 400

    except Exception as e:
        print(f"Error exporting book: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temp file
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass


@app.route('/api/extensions/upload', methods=['POST'])
def upload_extension():
    if 'extension' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['extension']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.py'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True, 'filename': filename})

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/api/extensions/activate', methods=['POST'])
def activate_extension():
    try:
        extension_name = request.json.get('name')
        active = request.json.get('active', False)

        # Update active extensions
        global active_extensions
        active_extensions[extension_name] = active

        # Save active extensions to a file
        save_active_extensions(active_extensions)

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error activating extension: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask application...")
    # Pre-load the extensions at startup
    load_extensions()

    # Install BeautifulSoup if not installed
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("BeautifulSoup is not installed. Installing now...")
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        print("BeautifulSoup installed successfully.")
        from bs4 import BeautifulSoup

    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'

    app.run(debug=debug_mode)