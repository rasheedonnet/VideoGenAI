"""Configuration for the VideoGenerator."""

import os
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Configuration for agents."""
    # Use Google models by default, TODO:fall back to open source
    use_google_models: bool = True   
    # Google Vertex AI config
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    beatoven_api_key: str = os.getenv("BEATOVEN_API_KEY", "")  
    beatoven_v1_api_url: str = os.getenv("BEATOVEN_V1_API_URL", "https://api.beatoven.ai/v1")

    # Output paths
    output_dir: str = "output"
    
@dataclass
class DirectorConfig(AgentConfig):
    """Configuration for the Director agent."""
    AGENT_NAME: str = "director_agent"
    DESCRIPTION: str = "Root agent to generate a video from a user prompt. This agent coordinates the entire video generation process by calling other agents in sequence."
    MODEL: str = "gemini-2.5-pro-preview-03-25"

@dataclass
class ScriptWriterConfig(AgentConfig):
    """Configuration for the ScriptWriter agent."""
    AGENT_NAME: str = "script_writer_agent"
    DESCRIPTION: str = "Script Writer Agent to generate a script for a video. This agent is responsible for generating a script based on the user prompt."
    MODEL: str = "gemini-2.5-pro-preview-03-25"

# @dataclass
class ImageProducerConfig(AgentConfig):
    """Configuration for the ImageProducer agent."""
    AGENT_NAME: str = "image_producer_agent"
    DESCRIPTION: str = "Image Producer Agent to generate images for a given script. This agent is responsible for generating images based on the provided script."
    MODEL: str = "gemini-2.5-pro-preview-03-25"
    OPENAI_MODEL: str = "gpt-image-1"
    IMAGE_SIZE: str = "1024x1536" # Choose a supported size (1024x1024 (square) 1536x1024 (landscape) 1024x1536 (portrait) auto (default))
    IMAGE_QUALITY: str = "low"  # Choose a supported quality (low, medium, high)
    IMAGE_COUNT: int = 1  # Number of images to generate
    IMAGE_FORMAT: str = "b64_json"  # Format of the image data returned by the API

@dataclass
class DubbingArtistConfig(AgentConfig):
    """Configuration for the DubbingArtist agent."""
    AGENT_NAME: str = "dubbing_agent"
    DESCRIPTION: str = "Image Producer Agent to generate images for a given script. This agent is responsible for generating images based on the provided script."
    MODEL: str = "gemini-2.5-pro-preview-03-25"
    OPENAI_MODEL: str = "gpt-4o-mini-tts"
    VOICE: str = "coral"

@dataclass
class BackgroundScoreConfig(AgentConfig):
    """Configuration for the MusicComposer agent."""
    AGENT_NAME: str = "bgscore_agent"
    DESCRIPTION: str = "Background score producer Agent to generate background music for given script. This agent is responsible for generating background music based on the provided script."
    MODEL: str = "gemini-2.5-pro-preview-03-25"

@dataclass
class VideoBuilderConfig(AgentConfig):
    """Configuration for the VideoBuilder agent."""
    AGENT_NAME: str = "video_builder_agent"
    DESCRIPTION: str = "Agent which uses previously generated images and audio to create a video. This agent is responsible for generating a video based on the provided instruction."
    MODEL: str = "gemini-2.5-pro-preview-03-25"

# @dataclass
# class SocialMediaPublisherConfig(AgentConfig):
#     """Configuration for the SocialMediaPublisher agent."""
#     gemini_model: str = "gemini-1.5-flash"
#     deepseek_model: str = "deepseek-ai/deepseek-v2"
    
#     # Social media credentials (should be set in .env)
#     instagram_token: str = os.getenv("INSTAGRAM_TOKEN", "")
#     facebook_token: str = os.getenv("FACEBOOK_TOKEN", "")
#     youtube_token: str = os.getenv("YOUTUBE_TOKEN", "")
#     tiktok_token: str = os.getenv("TIKTOK_TOKEN", "")