import asyncio
from agents.image_producer_agent import ImageGeneratorAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

async def run_agent():
    session_service = InMemorySessionService()
    OUTPUT_FOLDER = "output"
    agent = ImageGeneratorAgent()
    runner = Runner(agent=agent, session_service=session_service)

    print(f"Image Generator Agent ready. Images will be saved in the '{OUTPUT_FOLDER}' folder.")
    print("Enter a prompt to generate an image, or type 'quit' to exit.")

    while True:
        user_input = input("Prompt:we never fail, either we win or learn")
        if user_input.lower() == 'quit':
            break
        await runner.run(user_input)

asyncio.run(run_agent())