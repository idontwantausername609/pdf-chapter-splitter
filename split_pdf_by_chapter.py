import os
import re
import fitz  # PyMuPDF
import sys
# Add these imports for OCR
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

# More robust pattern: matches '[CHAPTER |', 'CHAPTER 1', etc.
chapter_heading_pattern = re.compile(r"^[\[\(\{\s]*chapter\s*[|:–—-]*\s*(\d{1,2})", re.IGNORECASE)

def find_chapters(doc, skip_first_n_pages=0):
    chapter_starts = []
    seen = set()
    last_found_page = -5
    for i in range(skip_first_n_pages, len(doc)):
        text = doc[i].get_text("text")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for idx, line in enumerate(lines):
            match = chapter_heading_pattern.match(line)
            if match:
                if match.lastindex and match.lastindex >= 2 and match.group(2) and match.group(2).strip():
                    title = match.group(2).strip()
                else:
                    title = lines[idx + 1] if idx + 1 < len(lines) else "Untitled"
                chap_num = int(match.group(1))
                if chap_num not in seen and (i - last_found_page >= 5):
                    chapter_starts.append((chap_num, i, title))
                    seen.add(chap_num)
                    last_found_page = i
                    print(f"✅ Found Chapter {chap_num} on page {i+1}: {title}")
                break
    chapter_starts.sort(key=lambda x: x[1])
    return chapter_starts

def debug_by_chapter(input_pdf_path):
    print(f"\n📂 Opening PDF: {input_pdf_path}")
    doc = fitz.open(input_pdf_path)

    print("\n🔎 Detecting chapters...")
    chapter_starts = find_chapters(doc)

    if not chapter_starts:
        print("❌ No chapters detected.")
        return

    chapter_starts.append((None, len(doc), "EOF"))  # end marker

    print("\n📄 Chapter PDF page ranges (1-based):")
    for idx in range(len(chapter_starts) - 1):
        chap_num, start_page, title = chapter_starts[idx]
        _, next_start_page, _ = chapter_starts[idx + 1]
        end_page = next_start_page - 1
        if end_page < start_page:
            print(f"⚠️  Skipping Chapter {chap_num}: invalid range {start_page + 1} to {end_page + 1}")
            continue
        print(f"  Chapter {chap_num}: PDF pages {start_page + 1} - {end_page + 1} | Title: {title}")
    print("\n🎉 Done!")

def audit_chapter_headings(input_pdf_path, skip_first_n_pages=20, output_txt="chapter_audit_output.txt"):
    print(f"\n📂 Opening PDF: {input_pdf_path}")
    doc = fitz.open(input_pdf_path)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(f"PDF: {input_pdf_path}\n\n")
        f.write("Auditing all lines matching the chapter pattern...\n")
        for i in range(skip_first_n_pages, len(doc)):
            text = doc[i].get_text("text")
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            for idx, line in enumerate(lines):
                match = chapter_heading_pattern.match(line)
                if match:
                    f.write(f"\n=== PDF page {i+1} ===\n")
                    f.write(f"Matched line: '{line}' (line {idx+1} on page)\n")
                    f.write("First 10 lines of this page:\n")
                    for l in lines[:10]:
                        f.write(f"  {l}\n")
        f.write("\nAudit complete. Review this file to tune your chapter detection.\n")
    print(f"\nAudit output saved to {output_txt}")

def ocr_page(input_pdf_path, page_num=26, dpi=300, output_img="ocr_page26.png"):
    print(f"\nRendering page {page_num} as image and running OCR...")
    if pytesseract is None or Image is None:
        print("pytesseract and Pillow are required for OCR. Please install them with: pip install pytesseract pillow")
        return
    doc = fitz.open(input_pdf_path)
    if page_num < 1 or page_num > len(doc):
        print(f"Page {page_num} is out of range.")
        return
    page = doc[page_num - 1]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_path = output_img
    pix.save(img_path)
    print(f"Saved page image to {img_path}")
    img = Image.open(img_path)
    ocr_text = pytesseract.image_to_string(img)
    print("\n--- OCR result ---\n")
    print(ocr_text)
    print("\n--- End OCR result ---\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python split_pdf_by_chapter.py <input_pdf>")
        sys.exit(1)
    input_pdf = sys.argv[1]
    if not os.path.isfile(input_pdf):
        print(f"File not found: {input_pdf}")
        sys.exit(1)
    # Only run OCR on page 26
    ocr_page(input_pdf, page_num=26)
    # audit_chapter_headings(input_pdf)
    # debug_by_chapter(input_pdf)

if __name__ == "__main__":
    main()
