#!/bin/bash
#
# Usage:
#   chmod +x setup_project.sh
#   ./setup_project.sh
#
# This script creates a baseline directory structure for a
# voice-and-text chatbot project, organized by data type and purpose.

# Exit immediately if any command fails
set -e

# Name of the top-level directory
PROJECT_NAME="grandma-chatbot"

# Create the main project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# --- data folder ---
mkdir -p data/text/{raw,cleaned,annotated}
mkdir -p data/audio/{raw,cleaned,transcripts}
mkdir -p data/metadata

# A short README for the data directory
cat << EOF > data/README.md
# Data Directory

- **text/**: Contains text-based data (e.g. messages).
  - **raw/**: Unprocessed or original text files.
  - **cleaned/**: Cleaned or preprocessed text files.
  - **annotated/**: Text files with tone/emotion or other annotations.
- **audio/**: Contains audio data (voicemail recordings, etc.).
  - **raw/**: Unprocessed/original audio files.
  - **cleaned/**: Noise-reduced or normalized audio files.
  - **transcripts/**: Text transcripts corresponding to audio files.
- **metadata/**: Supplementary files such as manifests or cross-references.
EOF

# --- notebooks folder ---
mkdir -p notebooks

# --- scripts folder ---
mkdir -p scripts/{data_preprocessing,training,inference,evaluation}

# --- models folder ---
mkdir -p models/{language_model,tts_model,stt_model}

# --- configs folder ---
mkdir -p configs

# --- docs folder ---
mkdir -p docs
cat << EOF > docs/guide.md
# Project Documentation

Use this folder for detailed guides, references, or how-to documents.
EOF

# --- top-level files ---
touch requirements.txt
touch LICENSE

cat << EOF > README.md
# $PROJECT_NAME

## Overview
This project aims to build a voice-and-text chatbot based on personal audio and text data from a loved one.

## Directory Structure

- **data/**: All raw and processed data
  - **text/**, **audio/**, **metadata/**
- **notebooks/**: Jupyter notebooks for exploration and prototyping
- **scripts/**: Python (or shell) scripts for data preprocessing, model training, inference, and evaluation
- **models/**: Stores checkpoints and config files for language models, TTS models, and STT models
- **configs/**: Configuration files (e.g., hyperparameters, environment settings)
- **docs/**: Documentation, tutorials, guides

## Getting Started

1. **Install Dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
2. **Data Preparation:**
   - Add your raw text messages and voicemail files to the relevant folders in \`data/\`.
   - Update or create transcripts in \`data/audio/transcripts/\` if needed.
3. **Model Training:**
   - Use scripts in \`scripts/training/\` to fine-tune your chatbot or TTS models.
4. **Inference / Running the Bot:**
   - Use scripts in \`scripts/inference/\` for text or voice-based interactions.

## Notes

- **Ethics & Privacy**: Since this project uses personal data, take care with how you store and share these files.
- **Future**: Expand or modify this structure as the project grows.

EOF

echo "Project structure for '$PROJECT_NAME' created successfully."