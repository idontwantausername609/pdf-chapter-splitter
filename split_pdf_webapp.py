import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os

st.title("Manual PDF Chapter Splitter")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
page_list = st.text_input("Enter chapter start pages (comma-separated, 1-based):", "26, 56, 86, 107, 132, 158, 192, 220, 254, 278, 305, 336")

if uploaded_file and page_list:
    chapter_starts = [int(x.strip()) for x in page_list.split(",") if x.strip().isdigit()]
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    chapter_starts = sorted(chapter_starts)
    chapter_starts.append(doc.page_count + 1)  # Sentinel for last chapter

    st.write("Splitting PDF...")
    for idx in range(len(chapter_starts) - 1):
        start = chapter_starts[idx] - 1
        end = chapter_starts[idx + 1] - 2
        chapter_num = idx + 1
        chapter_doc = fitz.open()
        chapter_doc.insert_pdf(doc, from_page=start, to_page=end)
        out_path = f"chapter_{chapter_num:02}_pages_{start+1}-{end+1}.pdf"
        chapter_doc.save(out_path)
        chapter_doc.close()
        with open(out_path, "rb") as f:
            st.download_button(f"Download {out_path}", f, file_name=out_path)
        os.remove(out_path)
    os.remove(tmp_path)
    st.success("Done!")

st.info("No files or data are uploaded to any server. All processing is local in your browser session.")
