"""Agent to create text to audio from a given dialogue."""

import asyncio
import aiohttp
import aiofiles
from pathlib import Path
from google.adk.agents import LlmAgent

from . import prompt
from config.config import BackgroundScoreConfig

# Ensure the output folder exists
Path(BackgroundScoreConfig.output_dir).mkdir(parents=True, exist_ok=True)

BACKEND_V1_API_URL =  BackgroundScoreConfig.beatoven_v1_api_url
BACKEND_API_HEADER_KEY = BackgroundScoreConfig.beatoven_api_key       

async def compose_track(request_data):
    """
    Generates a background score based on a text prompt using Beatoven API.
    Args:
        request_data: Data to send to the Beatoven API for track composition.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{BACKEND_V1_API_URL}/tracks/compose",
                json=request_data,
                headers={"Authorization": f"Bearer {BACKEND_API_HEADER_KEY}"},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
        except aiohttp.ClientConnectionError:
            raise Exception({"error": "Could not connect to beatoven.ai"})
        except Exception as e:
            raise Exception({"error": "Failed to make a request to beatoven.ai"}) from e
        finally:
            if not data.get("task_id"):
                raise Exception(data)


async def get_track_status(task_id):
    """
    Get the status of the track composition task.
    Args:
        task_id: The ID of the task to check the status for.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{BACKEND_V1_API_URL}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {BACKEND_API_HEADER_KEY}"},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception({"error": "Composition failed"})
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": "Could not connect"}) from e
        except Exception as e:
            raise Exception({"error": "Failed to make a request"}) from e


async def handle_track_file(track_path: str, track_url: str):
    """
    Downloads the track file from the given URL and saves it to the specified path.
    Args:
        track_path: The path where the track file will be saved.
        track_url: The URL from which to download the track file.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(track_url) as response:
                if response.status == 200:
                    async with aiofiles.open(track_path, "wb+") as f:
                        await f.write(await response.read())
                        return {}
        except aiohttp.ClientConnectionError as e:
            raise Exception({"error": "Could not download file"}) from e
        except Exception as e:
            raise Exception(
                {"error": "Failed to make a request to get track file"}
            ) from e


async def watch_task_status(task_id, interval=10):
    while True:
        track_status = await get_track_status(task_id)
        if "error" in track_status:
            raise Exception(track_status)

        print(f"Task status: {track_status}")
        if track_status.get("status") == "composing":
            await asyncio.sleep(interval)
        elif track_status.get("status") == "failed":
            raise Exception({"error": "task failed"})
        else:
            return track_status


async def create_and_compose(prompt: str, file_name: str):
    """
    Generates a background score based on a text prompt using Beatoven API.
    Args:
        prompt: Text to convert to background score.
        file_name: The name of the file to save the audio.
    """
    try:
        track_meta = {"prompt": {"text": prompt}, "format": "wav"}

        compose_res = await compose_track(track_meta)
        task_id = compose_res["task_id"]
        print(f"Started composition task with ID: {task_id}")

        generation_meta = await watch_task_status(task_id)
        print(generation_meta)
        track_url = generation_meta["meta"]["track_url"]
        print("Downloading track file")
        await handle_track_file(file_name, track_url)
        print("Composed! you can find your track as {file_name}")
        return {"status": "success", "file": file_name}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
        

bgscore_agent = LlmAgent(
    model= BackgroundScoreConfig.MODEL,
    name=BackgroundScoreConfig.AGENT_NAME,
    description=BackgroundScoreConfig.DESCRIPTION,
    instruction= prompt.BGSCORE_PROMPT,
    tools=[create_and_compose], # Include the AgentTool
    output_key="background_music"
)

print(f"✅ Agent '{bgscore_agent.name}' created using model '{bgscore_agent.model}'.")