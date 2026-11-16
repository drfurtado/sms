#!/bin/bash

# Render the Quarto project
echo "Rendering the repository..."
quarto render

# Add all changes (including the rendered docs folder)
echo "Adding changes to Git..."
git add .

# Commit messages
# Use current date/time if no message is provided as an argument
msg="update: $(date +'%Y-%m-%d %H:%M:%S')"
if [ $# -eq 1 ]; then
  msg="$1"
fi

echo "Commiting with message: $msg"
git commit -m "$msg"

# Push to GitHub
echo "Pushing to GitHub..."
git push

# Preview locally
echo "Launching local preview..."
quarto preview
