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

## Components

- **Script Writer**: Generates engaging scripts based on user prompts
- **Image Producer**: Creates images for the video
- **Dubbing Artist**: Converts scripts to spoken audio
- **Music Composer**: Generates background music
- **Video Builder**: Assembles all components into a video

## Getting Started

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your API credentials:
   ```
   cp .env.example .env
   # Then edit .env to add your 
   GOOGLE_API_KEY=your_google_api_key
   OPENAI_API_KEY=your_openai_api_key
   BEATOVEN_API_KEY=your_beatoven_api_key (https://www.beatoven.ai/)
   ```
## Usage

### Command Line

```
# Generate a video with a prompt
python main.py --prompt "Generate inspiring quotes and explain it with a story" --output "my_video.mp4"


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.