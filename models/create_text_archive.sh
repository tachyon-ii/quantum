#!/bin/bash

# create_text_archive.sh - Creates a text archive of project files
# Usage: ./create_text_archive.sh [directory] [output_file]

# Set defaults
SOURCE_DIR="${1:-.}"
OUTPUT_FILE="${2:-project_archive.txt}"

# Create/clear the output file
> "$OUTPUT_FILE"

# Function to add a file to the archive
add_file() {
    local file="$1"
    local relative_path="${file#$SOURCE_DIR/}"
    
    echo "=================================================================================" >> "$OUTPUT_FILE"
    echo "FILE: $relative_path" >> "$OUTPUT_FILE"
    echo "=================================================================================" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
}

# Header for the archive
echo "PROJECT ARCHIVE - Created: $(date)" >> "$OUTPUT_FILE"
echo "Source Directory: $SOURCE_DIR" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Find and process all text files (customize the pattern as needed)
# This example includes common code and documentation files
find "$SOURCE_DIR" -type f \( \
    -name "*.c" -o \
    -name "*.h" -o \
    -name "*.md" -o \
    -name "*.txt" -o \
    -name "*.py" -o \
    -name "*.sh" -o \
    -name "*.json" -o \
    -name "*.yaml" -o \
    -name "*.yml" -o \
    -name "Makefile" -o \
    -name "README*" \
    \) ! -path "*/\.*" ! -path "*/node_modules/*" ! -path "*/venv/*" ! -path "*/__pycache__/*" | sort | while read -r file; do
    
    echo "Adding: ${file#$SOURCE_DIR/}"
    add_file "$file"
done

echo "Archive created: $OUTPUT_FILE"
echo "Total size: $(du -h "$OUTPUT_FILE" | cut -f1)"
echo "Files included: $(grep -c "^FILE: " "$OUTPUT_FILE")"
