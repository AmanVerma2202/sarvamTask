# sarvamTask
Flask-based web application that allows users to upload a PDF, annotate specific words with their corresponding Unicode values, and download the annotated PDF.

When using custom fonts or glyphs, there might be instances where characters don't correspond to standard Unicode values, making it hard to ensure text consistency and correctness. This issue can affect the readability and functionality of the text across different platforms and applications.

The code uses a custom mapping (custom_mapping) to convert characters to their corresponding Unicode values based on the font. This ensures that text information is correctly represented even with non-standard or custom fonts.



### Files
- **Static/**: Contains the generated annotated PDF file.
- **templates/**: Contains the HTML template for the web interface.
- **app.log**: Stores logs related to the application's execution.
- **glyphMapping.py**: Contains custom mappings of glyphs to Unicode characters.
- **sarvam.py**: Main application file that handles PDF processing, annotation, and the Flask web app.


## How to Run Locally

Clone the repository:

   ```bash
   git clone https://github.com/AmanVerma2202/sarvamTask.git
   cd sarvamTask
   pip install -r requirements.txt
   python sarvam.py
 ```

## Demo

Insert gif or link to demo



## Tech Stack

 **Python,Html,Flask,Fitz(PyMuPdf)**

## Approach
The project solves the problem of annotating PDFs with detailed information about each word's glyph by:

**Extracting Text**: The text is extracted from the PDF using the PyMuPDF library (fitz). The text is parsed into blocks, lines, and spans to analyze individual words.<br/>
**Mapping Glyphs**: Each Character(glyph) in the PDF is mapped to its corresponding Unicode character  using custom mappings defined in glyphMapping.py.<br/>
**Annotating**: The application calculates the position and dimensions of each word, then adds annotations with details like font name, font size, color, position, and Unicode values. These annotations are placed on the PDF with small lines pointing to the corresponding text or character, ensuring no overlap between annotations.






**Web Interface**: The Flask web app provides a simple interface for users to upload a PDF, process it, and download the annotated version.


## Logging
The application generates logs for debugging and tracking purposes. Logs are stored in app.log.

## Contributing
Feel free to submit issues, fork the repository, and send pull requests if you want to contribute.
