# grandma-chatbot

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
   ```bash
   pip install -r requirements.txt
   ```
2. **Data Preparation:**
   - Add your raw text messages and voicemail files to the relevant folders in `data/`.
   - Update or create transcripts in `data/audio/transcripts/` if needed.
3. **Model Training:**
   - Use scripts in `scripts/training/` to fine-tune your chatbot or TTS models.
4. **Inference / Running the Bot:**
   - Use scripts in `scripts/inference/` for text or voice-based interactions.

## Notes

- **Ethics & Privacy**: Since this project uses personal data, take care with how you store and share these files.
- **Future**: Expand or modify this structure as the project grows.

