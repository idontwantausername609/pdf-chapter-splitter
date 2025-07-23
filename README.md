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

A simple Streamlit web app to split a PDF into chapters using a manual list of start pages. No server upload—everything runs locally in your browser session.

## How to Use

1. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app:
   ```sh
   streamlit run split_pdf_webapp.py
   ```
3. Open the app in your browser, upload your PDF, and enter the chapter start pages (comma-separated, 1-based as seen in your PDF viewer).
4. Download each split chapter as a PDF.

## Requirements
- Python 3.8+
- streamlit
- pymupdf

## How it works
- No files are uploaded to any server. All processing is local.
- Works on Windows, Mac, and Linux.

## Example
- Enter: `26, 56, 86, 107, 132, 158, 192, 220, 254, 278, 305, 336`
- Each chapter will be available for download after splitting.

---

Feel free to fork, modify, or deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) for easy sharing!
