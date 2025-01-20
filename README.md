Title - AI-Driven Admission Assistance Chatbot for Streamlined University Enrollment

Part 1 - Web Scraping and Parsing Pipeline

This project enables efficient web scraping, parsing, and data consolidation. Below are the details of each component and its functionality.

## Dependencies
-`bs4`
-`os`
-`playwright`

 1. Parsing URLs - `Get_urls.py`
- Input: `id_name_urls.csv`  
- Output: `urls.csv`  
- Description:  
  Extracts and consolidates all URLs from the input CSV into a single output CSV file.  


 2. Web Scraping - `Web_Scraper.py`
- Input: URL (e.g., `https://www.aero.iitb.ac.in/`)  
- Output: Directory (e.g., `www.aero.iitb.ac.in`)  
- Description:  
  Scrapes the entire website from the provided URL and creates a directory structure. Downloads all files (HTML, images, CSS, etc.) and saves them in the respective subdirectories.

Code Summary:
- Saves the website files by maintaining directory structure.
- Avoids redundant visits using a `visited_urls` set.
- Downloads resources (images, scripts, CSS) into the corresponding directories.

To Execute:
```bash
python Web_Scraper.py
```

---

3. Getting HTML Pages - `Get_Dept_html.py`
- Input: Directory created by `Web_Scraper.py` (e.g., `www.aero.iitb.ac.in/home`)  
- Output: Parsed text files in a new directory (e.g., `aero/`)  
- Description:  
  Parses HTML files in the scraped directory to extract:
  - Paragraphs
  - Tables
  - Ordered lists  

Converts the extracted content into text files stored in the output directory.

To Execute:
```bash
python Get_Dept_html.py
```

---

## 4. Merging Files - `Merging_files.py`
- Input: Directory with parsed text files (e.g., `aero/`)  
- Output: Single merged text file (e.g., `aero.txt`)  
- Description:  
  Combines all text files into a single output file for easier data access and analysis.

To Execute:
```bash
python Merging_files.py
```

---

## Example Workflow:
1. Parse URLs: Extract URLs from `id_name_urls.csv` using `Get_urls.py`.  
2. Web Scraping: Scrape the website using `Web_Scraper.py`.  
3. HTML Parsing: Process HTML files and extract structured content using `Get_Dept_html.py`.  
4. Merge Files: Consolidate extracted content into a single file using `Merging_files.py`.  

---

## Note:
- For demo purpose some intermediate files are uploaded not all are uploaded. 
- All the text files generated are to be converted to pdf.

-------------------------------------------------------------------------------------------------------------------------------

Part 2 - Retrieval-Based Question-Answering System

This project implements a retrieval-based question-answering (QA) system using PDF documents as input data.

---

## Overview

The system leverages the following components:

1. PDF Loading: Reads and processes PDF documents.
2. Text Splitting: Splits documents into smaller chunks for efficient retrieval.
3. Embeddings: Converts text chunks into numerical vectors using a Sentence Transformer model.
4. Retriever: Retrieves relevant text chunks for a given query based on similarity.
5. LLM Integration: Simulates response generation based on retrieved context.

---

## Features

- Processes multiple PDF files from a directory.
- Splits documents into manageable chunks with overlap for better context.
- Embeds documents and queries using a pre-trained Sentence Transformer model.
- Implements an in-memory vector store for fast similarity-based retrieval.
- Provides a chatbot interface for interactive question answering.

---

## Dependencies

- `os`
- `langchain_community.document_loaders`
- `langchain_text_splitters`
- `langchain_core.vectorstores`
- `sentence_transformers`
- `numpy`

Install these dependencies using pip:
```bash
pip install langchain sentence-transformers numpy 
```

---

## Files

- PDF Loader: Loads and processes PDF files from a specified directory.
- Text Splitter: Breaks documents into chunks of 1000 characters with 200-character overlap.
- Embedding Model: Converts text into vector representations using a Sentence Transformer model (`Alibaba-NLP/gte-large-en-v1.5`).
- Retriever: Finds the most relevant chunks for a given query using cosine similarity.
- Chatbot: Provides a CLI for question answering.

---

## Usage

1. Set the Directory Path: Specify the directory containing your PDF files:
    ```python
    directory_path = "/path/to/pdf/files"
    ```

2. Process the PDFs:
    ```python
    documents = process_pdf_directory(directory_path)
    ```

3. Prepare the Retriever:
    ```python
    retriever = prepare_retriever(documents)
    ```

4. Run the Chatbot:
    ```python
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("Exiting. Goodbye!")
            break

        response = chatbot(query, retriever)
        print("Answer:", response)
    ```
---

## Sample Workflow
1. Process PDFs: Extract content from all PDF files in the directory.
2. Index Documents: Split and embed documents for efficient retrieval.
3. Interact: Enter queries to retrieve relevant context and generate answers.

---

## Example Query

Input:
"What is the procedure for applying to the program?"

Output:
"Simulated response to 'What is the procedure for applying to the program?' using context: [Relevant context]..."

---

## Notes

- The system uses a simulated response generator. Replace this with an actual LLM integration for production use.
- Ensure the PDF files contain readable text; scanned images may not be processed effectively.
- Connect to T4 GPU.

---
## References

Langchain tutorial - https://youtu.be/yF9kGESAi3M?si=Qot3YoLKZjh6f0wx

Playwright - https://github.com/microsoft/playwright-python

Pre-trained model used – https://huggingface.co/Alibaba-NLP/gte-large-en-v1.5

Sample Data - https://www.iitb.ac.in/
