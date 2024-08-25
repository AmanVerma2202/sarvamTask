# sarvamTask
Flask-based web application that allows users to upload a PDF, annotate specific words with their corresponding Unicode values, and download the annotated PDF.

When using custom fonts or glyphs, there might be instances where characters don't correspond to standard Unicode values, making it hard to ensure text consistency and correctness. This issue can affect the readability and functionality of the text across different platforms and applications.

The code uses a custom mapping (custom_mapping) to convert characters to their corresponding Unicode values based on the font. This ensures that text information is correctly represented even with non-standard or custom fonts.



### Files
- **app.log:** Log file that records events during the app's runtime.
- **glyphMapping.py:** Contains custom glyph-to-Unicode mappings.
- **sarvam.py:** The main Flask application file.
- **index.html:** The front-end template for uploading PDFs.

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/username/sarvam.git
   cd sarvam
