#!/bin/bash

# Define input and output filenames
input_file="yt-dlp_simpleGUI.py"
output_file="yt-dlp_simpleGUI_Win.py"

# Create a temporary file to hold the modified content
temp_file=$(mktemp)

# Add the specified lines to the temporary file
{
    echo "# Windows version, only things that change here are using yt-dlp.exe instead of ./yt-dlp,"
    echo "# and leaving some parts commented since they are only for Linux."
    echo "# I am using a script for converting this, please check the code for any errors from this conversion."
    echo ""
    # Use sed to replace only './yt-dlp' and ignore others like '/yt-dlp'
    sed 's|\./yt-dlp|yt-dlp.exe|g' "$input_file"
} > "$temp_file"

# Move the temporary file to the output file
mv "$temp_file" "$output_file"

echo "Replacement complete. The new file is saved as '$output_file'."

