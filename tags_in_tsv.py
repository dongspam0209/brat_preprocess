import pandas as pd

# Load the TSV file
file_path = 'FallRisk_En_No1.tsv'

# Reading the TSV file
with open(file_path, 'r', encoding='utf-8') as file:
    tsv_data = file.readlines()

# Collecting unique tags from the TSV file
tags = set()

# Parsing the lines for tags (assuming they are the columns after the 3rd one in tag info lines)
for line in tsv_data:
    if not line.startswith('#') and line.strip():  # Ignoring comments and empty lines
        columns = line.strip().split('\t')
        # Tags start from the 4th column onwards (index 3), ignoring first three columns (token location, token, etc.)
        tags.update([tag for tag in columns[3:] if tag != '_'])  # Ignore placeholder '_'

# Print the unique tags
# for tag in sorted(tags):
#     print(tag)


# Removing numbers and square brackets from tags
import re

# Function to clean the tags by removing [numbers]
def clean_tag(tag):
    return re.sub(r'\[\d+\]', '', tag)

# Assuming we already have the list of tags from previous code
# Here I'll simulate it by loading the result from the uploaded file
file_path = 'result.txt'

# Read the file and clean the tags
with open(file_path, 'r') as file:
    raw_tags = file.readlines()

# Clean each tag
cleaned_tags = {clean_tag(tag.strip()) for tag in raw_tags if tag.strip()}

# Display the cleaned and unique tags
print(cleaned_tags)
