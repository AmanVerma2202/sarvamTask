import os
import fitz
import random
import logging
from flask import Flask, render_template, request, send_file
from glyphMapping import custom_mapping  # Import the custom mappings

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='app.log',  # Log file name
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

def map_glyph_to_unicode(glyph, font_name):
    if font_name in custom_mapping:
        return custom_mapping[font_name].get(glyph, glyph)
    return glyph

def count_total_words(pdf_path):
    doc = fitz.open(pdf_path)
    total_words = 0
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_dict = page.get_text("dict")
        for block in text_dict.get("blocks", []):
            if 'lines' in block:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "")
                        words = text.split()
                        total_words += len(words)
    return total_words

def extract_and_annotate_words(pdf_path, output_pdf_path, annotate_ratio=0.05, min_annotations=10):
    logging.info(f"Starting annotation process for {pdf_path}")
    doc = fitz.open(pdf_path)
    total_words = count_total_words(pdf_path)
    words_to_annotate = max(int(total_words * annotate_ratio), min_annotations)
    words_annotated = 0
    previous_annotations = []  # List to store positions of previous annotations

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_dict = page.get_text("dict")
        for block in text_dict.get("blocks", []):
            if 'lines' in block:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        font_name = span.get("font", "Unknown Font")
                        font_size = span.get("size", "Unknown Size")
                        color = span.get("color", "Unknown Color")
                        color_hex = "#{:06x}".format(color)
                        bbox = span.get("bbox", [0, 0, 0, 0])
                        text = span.get("text", "")
                        words = text.split()
                        total_width = bbox[2] - bbox[0]

                        start_x = bbox[0]
                        start_y = bbox[1]  # y-coordinate is constant for a line
                        for word in words:
                            word_width = total_width * (len(word) / len(text))  # Estimate word width
                            if random.random() <= annotate_ratio and words_annotated < words_to_annotate:
                                mapped_word = ''.join(map_glyph_to_unicode(char, font_name) for char in word)
                                x = start_x + word_width / 2  # Midpoint of the word in x-axis
                                y = start_y  # y-coordinate remains constant

                                # Unicode and other details
                                unicode_values = []
                                for char in word:
                                    mapped_char = map_glyph_to_unicode(char, font_name)
                                    if len(mapped_char) == 1:
                                        unicode_values.append(f"U+{ord(mapped_char):04X}")
                                    else:
                                        unicode_values.append(f"U+{ord(mapped_char[0]):04X}")  # Handle multi-char cases

                                annotation_text = (
                                    f"Word: {mapped_word}\n"
                                    f"Font: {font_name}\n"
                                    f"Font Size: {font_size}\n"
                                    f"Color: {color_hex}\n"
                                    f"Position: x={x}px, y={y}px\n"
                                    f"Unicode: {', '.join(unicode_values)}"
                                )

                                # Annotation box (adjust y-position to avoid overlap)
                                text_lines = annotation_text.split('\n')
                                line_height = 7  # Approximate line height for font size 6
                                annot_height = len(text_lines) * line_height + 10
                                annot_y0 = start_y - 5
                                annot_y1 = start_y + annot_height

                                # Check for overlaps with previous annotations
                                while any(prev_annot[0] < annot_y1 and prev_annot[1] > annot_y0 for prev_annot in previous_annotations):
                                    annot_y0 += annot_height + 5  # Move the annotation box down
                                    annot_y1 += annot_height + 5

                                annot_rect = fitz.Rect(
                                    start_x + word_width + 5,
                                    annot_y0,
                                    start_x + word_width + 200,
                                    annot_y1
                                )

                                # Record the position of this annotation
                                previous_annotations.append((annot_y0, annot_y1))

                                # Draw an arrow (line) from the word to the annotation box
                                arrow_start = (start_x + word_width, start_y + (bbox[3] - bbox[1]) / 2)
                                arrow_end = (annot_rect.x0, (annot_rect.y0 + annot_rect.y1) / 2)
                                page.draw_line(arrow_start, arrow_end, color=(0, 0, 1), width=1)

                                # Add annotation
                                page.add_freetext_annot(
                                    annot_rect,
                                    annotation_text,
                                    fontsize=6,
                                    rotate=0,
                                    fill_color=(1, 1, 1),  # Background color for better visibility
                                    border_color=(0, 0, 0),  # Border color
                                    text_color=(0, 0, 0)  # Text color
                                )
                                words_annotated += 1
                            start_x += word_width + 1  # Move start_x to the next word position
        logging.info(f"Annotated page {page_num + 1}/{len(doc)}")
    doc.save(output_pdf_path)
    logging.info(f"Annotated PDF saved as {output_pdf_path}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf_file']
        if file and file.filename.endswith('.pdf'):
            input_path = os.path.join('static', file.filename)
            output_path = os.path.join('static', 'annotatedoutput.pdf')
            file.save(input_path)
            extract_and_annotate_words(input_path, output_path)
            return render_template('index.html', annotated_pdf='annotatedoutput.pdf')
    return render_template('index.html')

@app.route('/download')
def download():
    return send_file(os.path.join('static', 'annotatedoutput.pdf'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
