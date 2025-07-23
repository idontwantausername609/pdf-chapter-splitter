import fitz  # PyMuPDF
import os
import sys

def split_pdf_by_manual_pages(input_pdf_path, chapter_starts, output_dir="Chapters"):
    doc = fitz.open(input_pdf_path)
    os.makedirs(output_dir, exist_ok=True)
    chapter_starts = sorted(chapter_starts)
    chapter_starts.append(doc.page_count)  # Sentinel for last chapter
    for idx in range(len(chapter_starts) - 1):
        start = chapter_starts[idx] - 1  # Convert to 0-based index
        end = chapter_starts[idx + 1] - 2  # Inclusive end
        chapter_num = idx + 1
        chapter_doc = fitz.open()
        chapter_doc.insert_pdf(doc, from_page=start, to_page=end)
        filename = f"Chapter_{chapter_num:02}_pages_{start+1}-{end+1}.pdf"
        filepath = os.path.join(output_dir, filename)
        chapter_doc.save(filepath)
        chapter_doc.close()
        print(f"Saved: {filename} (Pages {start+1}-{end+1})")
    print("\nDone!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python split_pdf_manual.py <input_pdf>")
        sys.exit(1)
    input_pdf = sys.argv[1]
    # User-provided chapter start pages (1-based)
    chapter_starts = [26, 56, 86, 107, 132, 158, 192, 220, 254, 278, 305, 336]  # Stop at Notes section
    split_pdf_by_manual_pages(input_pdf, chapter_starts)

if __name__ == "__main__":
    main()
