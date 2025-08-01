# PDF Splitter by Chapter

This Python script splits a large PDF into multiple PDFs by chapter. Each output file is named after the detected chapter (e.g., 'Chapter 1.pdf', 'Chapter 2.pdf', etc.).

## Requirements
- Python 3.7+
- PyPDF2

## Installation
Install the required package:

```
pip install PyPDF2
```

## Usage

Place your PDF in the same directory as the script, then run:

```
python split_pdf_by_chapter.py <your_pdf_file.pdf>
```

The script will create separate PDF files for each chapter in the same directory.

## Notes
- Chapters are detected by searching for the word 'Chapter' followed by a number (case-insensitive) on each page.
- If no chapters are found, the script will notify you.

---

# Manual PDF Chapter Splitter (Web App)

**Try it instantly in your browser:**
👉 [pdf-split.streamlit.app](https://pdf-split.streamlit.app/)

A simple Streamlit web app to split a PDF into chapters using a manual list of start pages. No install needed—just use the link above!

## How to Use

1. Go to [pdf-split.streamlit.app](https://pdf-split.streamlit.app/)
2. Upload your PDF.
3. Enter the chapter start pages (comma-separated, 1-based as seen in your PDF viewer).
4. Download each split chapter as a PDF.

## Example
- Enter: `26, 56, 86, 107, 132, 158, 192, 220, 254, 278, 305, 336`
- Each chapter will be available for download after splitting.

---

### For Developers
If you want to run or modify the app locally:

1. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app:
   ```sh
   streamlit run split_pdf_webapp.py
   ```

---

Feel free to fork, modify, or deploy your own version!
