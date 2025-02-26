"""
PDF Export Extension for Novel Writer
Creates professionally typeset PDF exports with multiple style and page size options.
"""

def init_extension():
    """Initialize the extension."""
    return {
        "name": "PDF Export",
        "version": "1.0.0",
        "description": "Export books as professionally typeset PDFs with multiple styles and page sizes",
        "author": "Novel Writer"
    }

def on_load():
    """Called when the extension is loaded."""
    print("PDF Export extension loaded!")

def get_css():
    """Return the CSS for the PDF export UI."""
    return """
    .pdf-export-button {
        margin-left: 5px;
    }
    
    .pdf-export-modal {
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
    
    .pdf-export-modal-content {
        background-color: var(--card-bg);
        padding: 25px;
        border-radius: 8px;
        width: 500px;
        max-width: 90%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .pdf-export-modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 10px;
    }
    
    .pdf-export-modal-title {
        font-size: 18px;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    .pdf-export-form-group {
        margin-bottom: 15px;
    }
    
    .pdf-export-form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: 500;
    }
    
    .pdf-export-form-control {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-size: 14px;
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    .pdf-export-row {
        display: flex;
        gap: 15px;
        margin-bottom: 15px;
    }
    
    .pdf-export-col {
        flex: 1;
    }
    
    .pdf-settings-info {
        margin-top: 15px;
        font-size: 12px;
        color: #666;
        font-style: italic;
    }
    
    .pdf-export-submit {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.3s;
        margin-top: 10px;
    }
    
    .pdf-export-submit:hover {
        background-color: var(--secondary-color);
    }
    
    .pdf-export-loading {
        display: none;
        text-align: center;
        margin-top: 15px;
    }
    
    .pdf-export-loading-spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
        margin-bottom: 10px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    """

def get_js():
    """Return the JavaScript for PDF export functionality."""
    return """
    // Add PDF export button to the export dropdown
    const exportDropdown = document.querySelector('.dropdown-content');
    if (exportDropdown) {
        const pdfExportLink = document.createElement('a');
        pdfExportLink.href = '#';
        pdfExportLink.className = 'dropdown-item pdf-export-button';
        pdfExportLink.textContent = 'Export as PDF';
        exportDropdown.appendChild(pdfExportLink);
        
        // Add event listener to the PDF export button
        pdfExportLink.addEventListener('click', function(e) {
            e.preventDefault();
            openPdfExportModal();
        });
    }
    
    // Create PDF export modal
    const pdfExportModal = document.createElement('div');
    pdfExportModal.className = 'pdf-export-modal';
    pdfExportModal.id = 'pdfExportModal';
    pdfExportModal.innerHTML = `
        <div class="pdf-export-modal-content">
            <div class="pdf-export-modal-header">
                <div class="pdf-export-modal-title">Export Book as PDF</div>
                <span class="close">&times;</span>
            </div>
            <form id="pdfExportForm">
                <div class="pdf-export-row">
                    <div class="pdf-export-col">
                        <div class="pdf-export-form-group">
                            <label for="pdfExportStyle">Style</label>
                            <select id="pdfExportStyle" class="pdf-export-form-control">
                                <option value="modern">Modern</option>
                                <option value="classic">Classic</option>
                                <option value="manuscript">Manuscript</option>
                                <option value="minimal">Minimal</option>
                            </select>
                        </div>
                    </div>
                    <div class="pdf-export-col">
                        <div class="pdf-export-form-group">
                            <label for="pdfExportSize">Page Size</label>
                            <select id="pdfExportSize" class="pdf-export-form-control">
                                <option value="letter">Letter (8.5\" x 11\")</option>
                                <option value="a4">A4 (210mm x 297mm)</option>
                                <option value="a5">A5 (148mm x 210mm)</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="pdf-export-form-group">
                    <label for="pdfExportMargin">Margins</label>
                    <select id="pdfExportMargin" class="pdf-export-form-control">
                        <option value="normal">Normal (1 inch)</option>
                        <option value="narrow">Narrow (0.5 inch)</option>
                        <option value="wide">Wide (1.25 inch)</option>
                    </select>
                </div>
                
                <div class="pdf-export-form-group">
                    <label for="pdfExportFontSize">Font Size</label>
                    <select id="pdfExportFontSize" class="pdf-export-form-control">
                        <option value="10">10pt</option>
                        <option value="11" selected>11pt</option>
                        <option value="12">12pt</option>
                    </select>
                </div>
                
                <div class="pdf-export-form-group">
                    <label for="pdfExportAuthor">Author Name</label>
                    <input type="text" id="pdfExportAuthor" class="pdf-export-form-control" placeholder="Your name">
                </div>
                
                <div class="pdf-export-form-group">
                    <label>
                        <input type="checkbox" id="pdfExportTOC" checked>
                        Include Table of Contents
                    </label>
                </div>
                
                <div class="pdf-settings-info">
                    PDF generation requires ReportLab to be installed. If you encounter errors, run: pip install reportlab
                </div>
                
                <div class="pdf-export-loading" id="pdfExportLoading">
                    <div class="pdf-export-loading-spinner"></div>
                    <p>Generating PDF, please wait...</p>
                </div>
                
                <button type="submit" class="pdf-export-submit">Generate PDF</button>
            </form>
        </div>
    `;
    document.body.appendChild(pdfExportModal);
    
    // Close modal when clicking the X
    pdfExportModal.querySelector('.close').addEventListener('click', function() {
        pdfExportModal.style.display = 'none';
    });
    
    // Close modal when clicking outside
    pdfExportModal.addEventListener('click', function(event) {
        if (event.target === pdfExportModal) {
            pdfExportModal.style.display = 'none';
        }
    });
    
    // Handle form submission
    document.getElementById('pdfExportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading spinner
        document.getElementById('pdfExportLoading').style.display = 'block';
        
        // Collect form data
        const formData = {
            bookId: book.id,
            style: document.getElementById('pdfExportStyle').value,
            pageSize: document.getElementById('pdfExportSize').value,
            margins: document.getElementById('pdfExportMargin').value,
            fontSize: document.getElementById('pdfExportFontSize').value,
            author: document.getElementById('pdfExportAuthor').value,
            includeTOC: document.getElementById('pdfExportTOC').checked
        };
        
        // Save current chapter
        saveCurrentChapter();
        
        // Send request to generate PDF
        fetch(`/api/extensions/pdf-export/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'PDF generation failed');
                });
            }
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${book.title.replace(/\\s+/g, '_')}.pdf`;
            document.body.appendChild(a);
            a.click();
            
            // Clean up
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            document.getElementById('pdfExportLoading').style.display = 'none';
            pdfExportModal.style.display = 'none';
        })
        .catch(error => {
            console.error('Error generating PDF:', error);
            alert('Error: ' + error.message);
            document.getElementById('pdfExportLoading').style.display = 'none';
        });
    });
    
    // Function to open PDF export modal
    function openPdfExportModal() {
        pdfExportModal.style.display = 'flex';
        
        // Set default author to stored value if available
        const storedAuthor = localStorage.getItem('pdfExportAuthor');
        if (storedAuthor) {
            document.getElementById('pdfExportAuthor').value = storedAuthor;
        }
    }
    """

def inject_editor(document):
    """Inject the PDF export CSS and JS into the editor."""
    # Add CSS
    style_tag = document.new_tag('style')
    style_tag.string = get_css()
    document.head.append(style_tag)

    # Add JS
    script_tag = document.new_tag('script')
    script_tag.string = get_js()
    document.body.append(script_tag)

    return document

def generate_pdf(book_data, options):
    """
    Generate a PDF from book data and options.
    Uses ReportLab to create a formatted PDF.
    """
    try:
        # Import required packages - will fail if not installed
        from reportlab.lib.pagesizes import letter, A4, A5
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.platypus.tableofcontents import TableOfContents
        import tempfile
        from bs4 import BeautifulSoup

        # Define page sizes
        page_sizes = {
            'letter': letter,
            'a4': A4,
            'a5': A5
        }

        # Define margins
        margins = {
            'normal': 1*inch,
            'narrow': 0.5*inch,
            'wide': 1.25*inch
        }

        # Get options with defaults
        page_size = page_sizes.get(options.get('pageSize', 'letter'), letter)
        margin = margins.get(options.get('margins', 'normal'), 1*inch)
        font_size = float(options.get('fontSize', 11))
        style_name = options.get('style', 'modern')

        # Create a temporary file for the PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        filename = temp_file.name
        temp_file.close()

        # Create the document
        doc = SimpleDocTemplate(
            filename,
            pagesize=page_size,
            leftMargin=margin,
            rightMargin=margin,
            topMargin=margin,
            bottomMargin=margin,
            title=book_data.get('title', 'Untitled'),
            author=options.get('author', '')
        )

        # Define styles
        styles = getSampleStyleSheet()

        # Style definitions based on selected style
        if style_name == 'modern':
            title_font = 'Helvetica-Bold'
            body_font = 'Helvetica'
            alignment = TA_JUSTIFY
        elif style_name == 'classic':
            title_font = 'Times-Bold'
            body_font = 'Times-Roman'
            alignment = TA_JUSTIFY
        elif style_name == 'manuscript':
            title_font = 'Courier-Bold'
            body_font = 'Courier'
            alignment = TA_LEFT
        elif style_name == 'minimal':
            title_font = 'Helvetica-Bold'
            body_font = 'Helvetica'
            alignment = TA_LEFT
        else:
            # Default to modern
            title_font = 'Helvetica-Bold'
            body_font = 'Helvetica'
            alignment = TA_JUSTIFY

        # Create styles
        title_style = ParagraphStyle(
            'Title',
            fontName=title_font,
            fontSize=font_size*2,
            alignment=TA_CENTER,
            spaceAfter=30
        )

        heading_style = ParagraphStyle(
            'Heading1',
            fontName=title_font,
            fontSize=font_size*1.5,
            alignment=TA_CENTER,
            spaceAfter=20
        )

        normal_style = ParagraphStyle(
            'Normal',
            fontName=body_font,
            fontSize=font_size,
            alignment=alignment,
            firstLineIndent=0.25*inch,
            spaceAfter=10
        )

        # Create document elements
        elements = []

        # Add title
        elements.append(Paragraph(book_data.get('title', 'Untitled'), title_style))

        # Add author if provided
        if options.get('author'):
            author_style = ParagraphStyle(
                'Author',
                fontName=body_font,
                fontSize=font_size*1.2,
                alignment=TA_CENTER,
                spaceAfter=30
            )
            elements.append(Paragraph(f"By {options.get('author')}", author_style))

        # Add table of contents if requested
        if options.get('includeTOC', True):
            elements.append(PageBreak())
            elements.append(Paragraph("Table of Contents", heading_style))
            toc = TableOfContents()
            toc.levelStyles = [
                ParagraphStyle(
                    name='TOCHeading1',
                    fontName=body_font,
                    fontSize=font_size,
                    leftIndent=20,
                    firstLineIndent=-20
                )
            ]
            elements.append(toc)

        # Process chapters
        for chapter in sorted(book_data.get('chapters', []), key=lambda x: x.get('order', 0)):
            # Add page break before chapter
            elements.append(PageBreak())

            # Add chapter heading
            elements.append(Paragraph(chapter.get('title', 'Chapter'), heading_style))

            # Process chapter content
            content = chapter.get('content', '')
            if content:
                # Parse HTML content
                soup = BeautifulSoup(content, 'html.parser')

                # Just get text paragraphs for simplicity
                paragraphs = soup.get_text().split('\n\n')

                for paragraph in paragraphs:
                    if paragraph.strip():
                        elements.append(Paragraph(paragraph.strip(), normal_style))

        # Build the document
        doc.build(elements)

        return filename
    except ImportError as e:
        # Handle missing dependencies
        print(f"Missing dependency: {str(e)}")
        raise ImportError(f"Required package not installed: {str(e)}. Please run 'pip install reportlab beautifulsoup4'.")
    except Exception as e:
        # Handle other errors
        print(f"Error generating PDF: {str(e)}")
        raise Exception(f"Error generating PDF: {str(e)}")