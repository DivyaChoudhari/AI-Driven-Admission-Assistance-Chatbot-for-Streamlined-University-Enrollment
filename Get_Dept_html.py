#Input - Directory created by Web_Scraper.py
#Output - department directory

import os
from bs4 import BeautifulSoup

# Input directory with all files
input_dir = 'www.aero.iitb.ac.in/home'

# Output directory named aero
output_dir = '/home/divya/Project/aero'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Print all files in the input directory for debugging
print(f"Files in input directory: {os.listdir(input_dir)}")

# Iterating through all files and generating automatically mapped output text files
for filename in os.listdir(input_dir):
    # Construct full input file path
    file_path = os.path.join(input_dir, filename)

    # Only processing files and skipping index.html
    if os.path.isfile(file_path):
        if filename == 'index.html':
            print(f"Skipping file: {filename}")  # Debugging line
            continue

        print(f"Processing file: {filename}")  # Debugging line

        # Generate the output file name by replacing the original extension with .txt
        output_file_name = f"{os.path.splitext(filename)[0]}.txt"
        output_file_path = os.path.join(output_dir, output_file_name)

        # Open the file and read its contents
        with open(file_path, 'r') as file:
            content = file.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Extracting paragraphs 
        paragraphs = soup.find_all('p')
        paragraph_texts = '\n'.join(p.get_text(strip=True) for p in paragraphs)

        # Extracting tables
        table_texts = []
        tables = soup.find_all('table')
        for table in tables:
            # Start a new table section in the output
            table_texts.append("\nTable:\n")
            rows = table.find_all('tr')
            for row in rows:
                # Extracting data from each cell in the row
                cells = row.find_all(['td', 'th'])  # Include both data and header cells
                cell_texts = [cell.get_text(strip=True) for cell in cells]  # Strip whitespace
                table_texts.append('\t'.join(cell_texts))  # Join cells with tabs for better readability
            table_texts.append("\n")  # Add a newline after each table

        # Extracting ordered lists
        list_texts = []
        ordered_lists = soup.find_all('ol')

        for ol in ordered_lists:
            list_texts.append("\nOrdered List:\n")
            items = ol.find_all('li')
            for index, item in enumerate(items, start=1):
                list_texts.append(f"{index}. {item.get_text(strip=True)}")  # Numbering for ordered lists

        # Combine all texts to write to the output file
        output_content = (
            paragraph_texts + "\n\n" +  # Paragraphs
            "\n".join(table_texts) + "\n\n" +  # Tables
            "\n".join(list_texts)  # Ordered Lists
        )

        # Write the combined content to the output text file
        with open(output_file_path, 'w') as output_file:
            output_file.write(output_content)
            print(f"Saved output to: {output_file_path}")  # Debugging line

