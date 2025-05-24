"""Agent to create text to audio from a given dialogue."""

import os
from google.adk.agents import LlmAgent

from moviepy.editor import (
    ImageClip,
    TextClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    CompositeAudioClip,
)

from . import prompt
from config.config import VideoBuilderConfig

def create_image_segments(folder_path: str) -> list[dict]:
    """
    Creates a list of image segments from the specified folder.
    Args:
        folder_path: Path to the folder containing images.
    Returns:
        A list of dictionaries containing image file names and their durations.
    """
    image_segments = []
   
    for filename in sorted(os.listdir(folder_path), key=lambda x: int(x.split("_")[0]) if x.split("_")[0].isdigit() else float('inf')):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            # each file name will start with start second and end second. parse this value and subtract end second with start second for duration. the file name will be like 0_3_dejected_setback.png
            start_second, end_second = map(int, filename.split("_")[:2])
            duration = end_second - start_second
            # Add the image file and its duration to the list
            # concatenate file name with folder path
            image_segments.append({"file": filename, "duration": duration})
    return image_segments


def create_video(output_folder:str, image_folder: str, voice_over_file: str, background_music_file: str, video_duration:int=30) -> dict:
    """
    Creates a video from a list of image segments and audio files.
    Args:
        output_folder: Path to the output folder where the video will be saved.
        image_folder: Path to the folder containing images.
        voice_over_file: Path to the voice over audio file.
        background_music_file: Path to the background music audio file.
        output_video_file: Path to the output video file to be created.
        video_duration: Duration of the video in seconds. default is 30 seconds.
    Returns:
        A dictionary containing the status and the path to the created video file.
    """
    # --- Configuration ---
    output_video_file = os.path.join(output_folder, "final_video.mp4")
    image_segments = create_image_segments(image_folder)
    #video_duration = 30  # seconds
    fps = 24
    video_size = (1960, 1080) # width, height # insta video size

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(image_folder):
        # This script expects images to be there. If the folder is missing,
        # ImageClip will fail. We can create it, but the user needs to populate it.
        os.makedirs(image_folder)
        print(f"Created images folder: {image_folder}. Please ensure it contains the required images.")

    # --- Load Audio ---
    try:
        voice_over_audio = AudioFileClip(voice_over_file)
    except Exception as e:
        print(f"Error loading voice over audio '{voice_over_file}': {e}")
        print("Please ensure the voice over file exists and is a valid audio format.")
        return
    try:
        background_music = AudioFileClip(background_music_file).volumex(0.2) # Lower volume
    except Exception as e:
        print(f"Error loading background music '{background_music_file}': {e}")
        print("Please ensure the background music file exists and is a valid audio format.")
        # Continue without background music or return, depending on requirements.
        # For this example, we'll try to proceed without it.
        background_music = None

    # --- Create Video Clips from Images ---
    video_clips = []
    current_time = 0
    for i, segment in enumerate(image_segments):
        image_path = os.path.join(image_folder, segment["file"])
        duration = segment["duration"]
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}. Using a black placeholder.")
            # Create a black clip as a placeholder
            clip = ColorClip(size=video_size, color=(0,0,0), duration=duration, ismask=False)
        else:
            clip = ImageClip(image_path, duration=duration)

        clip = clip.set_start(current_time).set_duration(duration)
        # add transition effect to clip
        clip = clip.crossfadein(1) # 1 second crossfade effect
        video_clips.append(clip)
        current_time += duration
        
    # --- Concatenate all visual clips ---
    final_video_visuals = concatenate_videoclips(video_clips, method="compose")
    final_video_visuals = final_video_visuals.set_duration(video_duration)

    # --- Combine Audio ---
    # Set voice over as the main audio for the visual composition
    final_video = final_video_visuals.set_audio(voice_over_audio)

    # If background music is available, composite it
    if background_music:
        background_music = background_music.subclip(0, video_duration)
        final_audio = CompositeAudioClip([final_video.audio, background_music])
        final_video = final_video.set_audio(final_audio)
    
    # Ensure final video is exactly `video_duration`
    final_video = final_video.subclip(0, video_duration)

    # --- Write Video File ---
    try:
        print(f"Writing video to {output_video_file}...")
        final_video.write_videofile(
            output_video_file,
            fps=fps,
            codec='libx264',          # Common codec
            audio_codec='aac',        # Common audio codec
            temp_audiofile='temp-audio.m4a', # Temporary audio file
            remove_temp=True,         # Remove temp audio file
            threads=4,                # Number of threads for encoding
            preset='medium'           # Encoding speed/quality trade-off
        )
        print("Video created successfully!")
    except Exception as e:
        print(f"Error writing video file: {e}")
        if "IMAGEMAGICK_BINARY" in str(e):
            print("This error might be related to ImageMagick not being found.")
            print("Please ensure ImageMagick is installed and in your system's PATH,")
            print("or specify its path using: change_settings({'IMAGEMAGICK_BINARY': r'/path/to/convert'})")

    # Clean up audio clips
    if voice_over_audio:
        voice_over_audio.close()
    if background_music and hasattr(background_music, 'close'): # Looped audio might not be original clip
        try:
            background_music.close()
        except Exception:
            pass # Already closed or not closable
    if final_video_visuals: # Should be final_video? No, individual clips are closed by concatenate or final write.
        pass
    # --- Return the final video path ---
    return {"status": "success", "video_path": output_video_file}

video_builder_agent = LlmAgent(
    model= VideoBuilderConfig.MODEL,
    name=VideoBuilderConfig.AGENT_NAME,
    description=VideoBuilderConfig.DESCRIPTION,
    instruction= prompt.VIDEO_BUILDER_PROMPT,
    tools=[create_video] # Include the AgentTool
)

print(f"✅ Agent '{video_builder_agent.name}' created using model '{video_builder_agent.model}'.")