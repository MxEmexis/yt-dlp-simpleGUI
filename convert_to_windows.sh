#!/bin/bash

# Define input and output filenames
input_file="yt-dlp_simpleGUI.py"
output_file="yt-dlp_simpleGUI_Win.py"

# Use sed to replace './yt-dlp' with 'yt-dlp.exe' and save the result to the new file
sed 's|./yt-dlp|yt-dlp.exe|g' "$input_file" > "$output_file"

echo "Replacement complete. The new file is saved as '$output_file'."

