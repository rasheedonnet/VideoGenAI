
"""Script Writer Agent to generate a script for a video.
This agent is responsible for generating a script based on the input.
It uses the Google ADK to manage the agents and their interactions.
"""
from config.config import ScriptWriterConfig
from google.adk.agents.llm_agent import Agent

from . import prompt

def save_script_to_file(script: str, file_name: str) -> None:
    """
    Saves the generated script to a file.
    Args:
        script: script to be saved in a file.
        file_name: The name of the file to save the script.

    Returns:
        script file path.
    """
    try:
        with open(file_name, "w") as f:
            f.write(script)
        print(f"Script saved to {file_name}")
        return {"status": "success", "file": file_name}
    except Exception as e:
        print(f"Error saving script to file: {e}")
        return {"status": "error", "error_message": str(e)}

script_writer_agent = Agent(
    model= ScriptWriterConfig.MODEL,
    name=ScriptWriterConfig.AGENT_NAME,
    description=ScriptWriterConfig.DESCRIPTION,
    instruction= prompt.SCRIPT_WRITER_PROMPT,
    tools=[save_script_to_file],  # Include the AgentTool
    output_key="video_script",  # Key to store the generated script

)

print(f"✅ Agent '{script_writer_agent.name}' created using model '{script_writer_agent.model}'.")