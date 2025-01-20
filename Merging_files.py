#Input - Department directory created by Get_Dept_html.py
#Output - Merged text file

import os

# Specify the directory where your text files are stored
directory = './aero'

# Specify the name of the output file
output_file = 'merged_aero.txt'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Check if the file has a .txt extension
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            # Open and read the content of each text file
            with open(file_path, 'r') as infile:
                # Write the content to the output file
                outfile.write(infile.read())
                outfile.write("\n")  # Add a newline between files

print(f"All files have been merged into {output_file}")

