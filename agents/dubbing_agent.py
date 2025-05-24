"""Agent to create text to audio from a given dialogue."""

from pathlib import Path
from google.adk.agents import LlmAgent
from openai import OpenAI

from . import prompt
from config.config import DubbingArtistConfig

# Ensure the output folder exists
Path(DubbingArtistConfig.output_dir).mkdir(parents=True, exist_ok=True)

def generate_tts(prompt: str, file_name: str, instruction: str) -> dict:
    """
    Generates an audio based on a text prompt using TTS model.

    Args:
        prompt: Text to convert to speech.
        file_name: The name of the file to save the audio.
        instruction: Instruction for the TTS model. for example "Speak in a cheerful and positive tone."

    Returns:
        audio file path.
    """
    try:
        client = OpenAI()
        with client.audio.speech.with_streaming_response.create(
            model=DubbingArtistConfig.OPENAI_MODEL,
            voice=DubbingArtistConfig.VOICE,
            input=prompt,
            instructions=instruction,
        ) as response:
            response.stream_to_file(file_name)
        # it will create mp3 file as default

        return {"status": "success", "file": file_name}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
        

dubbing_agent = LlmAgent(
    model= DubbingArtistConfig.MODEL,
    name=DubbingArtistConfig.AGENT_NAME,
    description=DubbingArtistConfig.DESCRIPTION,
    instruction= prompt.DUBBING_PROMPT,
    tools=[generate_tts], # Include the AgentTool
    output_key="dubbing_file",  # Key to store the generated audio file
)

print(f"✅ Agent '{dubbing_agent.name}' created using model '{dubbing_agent.model}'.")