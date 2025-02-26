from bs4 import BeautifulSoup

def init_extension():
    return {
        "name": "Word Count Tracker",
        "version": "1.0.0",
        "description": "Tracks word count, characters, and chapter length.",
        "author": "Luigichopper"
    }

def on_load():
    print("Word Count Tracker extension loaded!")

def get_word_count(text):
    words = text.split()
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    return len(words), characters, characters_no_spaces

def inject_editor(document):
    script_tag = document.new_tag('script')
    script_tag.string = """
    document.addEventListener("DOMContentLoaded", function() {
        function updateWordCount() {
            var content = document.querySelector(".editor").innerText;
            var wordCount = content.split(/\\s+/).filter(function(word) {
                return word.length > 0;
            }).length;
            var charCount = content.length;
            var charCountNoSpaces = content.replace(/\\s+/g, '').length;
            document.getElementById("wordCount").innerText = "Words: " + wordCount;
            document.getElementById("charCount").innerText = "Characters: " + charCount;
            document.getElementById("charCountNoSpaces").innerText = "Characters (no spaces): " + charCountNoSpaces;
        }

        var editor = document.querySelector(".editor");
        editor.addEventListener("input", updateWordCount);
        updateWordCount();
    });
    """
    document.body.append(script_tag)

    word_count_div = document.new_tag('div', id="wordCount")
    char_count_div = document.new_tag('div', id="charCount")
    char_count_no_spaces_div = document.new_tag('div', id="charCountNoSpaces")
    document.body.append(word_count_div)
    document.body.append(char_count_div)
    document.body.append(char_count_no_spaces_div)

    return document
