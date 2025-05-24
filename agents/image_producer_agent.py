"""Agent to create images from a given input."""

from pathlib import Path

from google.adk.agents import LlmAgent
from openai import OpenAI
import base64

from . import prompt
from config.config import ImageProducerConfig

# Ensure the output folder exists
Path(ImageProducerConfig.output_dir).mkdir(parents=True, exist_ok=True)

def generate_image(prompt: str, file_name: str) -> dict:
    """
    Generates an image based on a text prompt using DALL-E.

    Args:
        prompt: The text description for the image to generate.
        file_name: The name of the file to save the image.

    Returns:
        A dictionary containing the status and the base64 encoded image data
        or an error message.
    """
    try:
        client = OpenAI()
        # response = client.images.generate(
        #     model="dall-e-2",  # Or "dall-e-3" if you have access and prefer it
        #     prompt=prompt,
        #     size="256x256",  # Choose a supported size (256x256, 512x512, 1024x1024 for dall-e-2)
        #     response_format="b64_json",
        #     n=1  # Number of images to generate
        # )
        response = client.images.generate(
            model=ImageProducerConfig.OPENAI_MODEL,
            prompt=prompt,
            size=ImageProducerConfig.IMAGE_SIZE,
            quality=ImageProducerConfig.IMAGE_QUALITY,  # Choose a supported quality (low, medium, high)
            n=ImageProducerConfig.IMAGE_COUNT  # Number of images to generate
        )
        image_data_b64 = response.data[0].b64_json
        print(f"Image generated successfully for prompt: {prompt}")
        
        image_bytes = base64.b64decode(image_data_b64)
        # Save the image to a file
        with open(file_name, "wb") as f:
            f.write(image_bytes)
        
        return {"status": "success", "file": file_name}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
        

image_producer_agent = LlmAgent(
    model=ImageProducerConfig.MODEL,
    name=ImageProducerConfig.AGENT_NAME,
    description=ImageProducerConfig.DESCRIPTION,
    instruction= prompt.IMAGE_PRODUCER_PROMPT,
    tools=[generate_image], # Include the AgentTool
    output_key="image_info",  # Key to store the generated image info
)

print(f"✅ Agent '{image_producer_agent.name}' created using model '{image_producer_agent.model}'.")