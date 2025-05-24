# VideoGenerator

An AI-powered system for automatically generating short video content for social media platforms (Instagram, Facebook, YouTube, TikTok).

## Overview

VideoGenerator leverages various AI models to handle different aspects of video creation, from scriptwriting to final publication. The system uses Google's Agent Development Kit (ADK) to orchestrate the different AI agents.

## Features

- Script generation from user prompts
- Image generation for visuals 
- Audio/voice generation for narration
- Background music composition
- Video producer
- Social media publication

## Components

- **Script Writer**: Generates engaging scripts based on user prompts
- **Image Producer**: Creates images for the video
- **Dubbing Artist**: Converts scripts to spoken audio
- **Music Composer**: Generates background music
- **Video Builder**: Assembles all components into a video
- **Social Media Publisher**: Publishes videos to platforms

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API credentials:
   ```
   cp .env.example .env
   # Then edit .env to add your Google Cloud and social media credentials
   ```
## Usage

### Command Line

```
# Generate a video with a prompt
python main.py --prompt "Generate inspiring quotes and explain it with a story" --output "my_video.mp4"

# Launch the UI
python main.py --ui
```

### UI

For a more interactive experience, use the Streamlit UI by running:

```
streamlit run ui/app.py
```

### Testing

Run the tests to ensure everything is working correctly:

```
pytest tests/
```

## Configuration

The system is configured to use Google's AI models by default, with fallbacks to open-source alternatives.

- Google Models: Gemini Flash, Imagen 3, Chirp 3, Lyria 3, Veo 2
- Open Source Alternatives: DeepSeek, Stable Diffusion, OpenAI Whisper, Stable Audio Open, Wan

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.