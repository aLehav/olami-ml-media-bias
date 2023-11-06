import csv
import os
import sys

def split_csv_by_article(input_csv, output_folder):
    # Increase the maximum CSV field size limit
    max_int = sys.maxsize
    while True:
        # decrease the max_int value by factor 10 
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int/10)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # using DictReader to handle columns by name
        
        for article in reader:
            # Use the article title as the unique identifier, replacing any characters not suitable for filenames
            safe_title = ''.join(c if c.isalnum() else '_' for c in article['title'])
            output_filename = f"{output_folder}/article_{safe_title}.csv"
            
            with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                writer.writeheader()  # Write the headers to the new file
                writer.writerow(article)  # Write the article row to the new file
