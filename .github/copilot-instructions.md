<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This project is a Python script that splits a large PDF into multiple PDFs by chapter. Use libraries such as PyPDF2 or pdfplumber for PDF processing. The script should accept a PDF file as input and output separate PDF files for each chapter (e.g., 'chapter 1.pdf', 'chapter 2.pdf', etc.).

Use the following path as the "Test PDF": "C:\Users\viran\Downloads\PDF Splitter\Human Resource Management -- Sandra L Steen; Raymond A Noe; John R Hollenbeck; Barry A -- Fifth Canadian edition, Whitby, Ontario, 2019 -- McGraw Hill -- 978125965.pdf"


import fitz  # PyMuPDF
import os
import re
import sys

# Match chapter lines like "CHAPTER 1", "CHAPTER 1 – Title", etc.
chapter_pattern = re.compile(r"^\s*chapter\s+(\d{1,2})([\s:–—-].*)?$", re.IGNORECASE)

def find_chapters(doc, skip_first_n_pages=20):
    chapter_starts = []
    seen = set()

    for i in range(skip_first_n_pages, len(doc)):
        text = doc[i].get_text("text")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines:
            match = chapter_pattern.match(line)
            if match:
                chap_num = int(match.group(1))
                if chap_num not in seen:
                    chapter_starts.append((chap_num, i, line))
                    seen.add(chap_num)
                    print(f"Found Chapter {chap_num} on page {i+1}: {line}")
                break  # Only take the first match per page
    return chapter_starts

def split_by_chapter(input_pdf_path, output_dir="Chapters"):
    print(f"Opening PDF: {input_pdf_path}")
    doc = fitz.open(input_pdf_path)

    # Step 1: Find chapters
    print("\nDetecting chapters...")
    chapter_starts = find_chapters(doc)

    if not chapter_starts:
        print("No chapters detected.")
        return

    chapter_starts.append((None, len(doc), "End"))  # Sentinel for last chapter

    # Step 2: Output folder
    os.makedirs(output_dir, exist_ok=True)

    # Step 3: Split and save
    print("\nSaving chapter PDFs...")
    for idx in range(len(chapter_starts) - 1):
        chap_num, start_page, title_line = chapter_starts[idx]
        _, end_page, _ = chapter_starts[idx + 1]

        # Extract pages
        chapter_doc = fitz.open()
        chapter_doc.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)

        # Clean filename
        clean_title = re.sub(r'[^\w\s-]', '', title_line).strip().replace(" ", "_")
        filename = f"Chapter_{chap_num:02}_{clean_title}.pdf"
        filepath = os.path.join(output_dir, filename)

        chapter_doc.save(filepath)
        chapter_doc.close()
        print(f"Saved: {filename}")

    print("\nDone!")

def main():
    if len(sys.argv) != 2:
        print("Usage: python split_pdf_by_chapter.py <input_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    if not os.path.isfile(input_pdf):
        print(f"File not found: {input_pdf}")
        sys.exit(1)

    split_by_chapter(input_pdf)

if __name__ == "__main__":
    main()
