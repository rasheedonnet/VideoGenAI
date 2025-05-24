"""Root agent to generate a video from a user prompt.
This agent coordinates the entire video generation process by calling other agents in sequence.
It uses the Google ADK to manage the agents and their interactions.
"""
from config.config import DirectorConfig
from google.adk.agents import SequentialAgent

from agents.script_writer_agent import script_writer_agent
from agents.image_producer_agent import image_producer_agent 
from agents.dubbing_agent import dubbing_agent
from agents.bgscore_agent import bgscore_agent
from agents.video_builder_agent import video_builder_agent

# Sequential agent to coordinate the entire video generation process
# This agent will call other agents in sequence to generate the video
director_agent = SequentialAgent(
    name=DirectorConfig.AGENT_NAME,
    description=DirectorConfig.DESCRIPTION,
    sub_agents=[
        script_writer_agent,
        image_producer_agent,
        dubbing_agent,
        bgscore_agent,
        video_builder_agent
    ]    
)
root_agent = director_agent
print(f"✅ Agent '{director_agent.name}'")