import asyncio 
import argparse
from agents.director_agent import director_agent 
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
    # You can uncomment the line below to see *all* events during execution
    print(f"[Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

# --- Check for specific parts FIRST ---
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts: # Iterate through all parts
            if part.executable_code:
                # Access the actual code string via .code
                print(f"Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```")
                has_specific_part = True
            elif part.code_execution_result:
                # Access outcome and output correctly
                print(f"Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}")
                has_specific_part = True
            # Also print any text parts found in any event for debugging
            elif part.text and not part.text.isspace():
                print(f"Text: '{part.text.strip()}'")
                # Do not set has_specific_part=True here, as we want the final response logic below
                
    # is_final_response() marks the concluding message for the turn.
    if event.is_final_response():
        if event.actions and event.actions.escalate: # Handle potential errors/escalations
            print(f"Agent escalated: {event.error_message or 'No specific message.'}")
        # Add more checks here if needed (e.g., specific error codes)
        #break # Stop processing events once the final response is found
        

async def run_team_conversation(input_prompt:str):
    print("\n--- Starting Agent Team Delegation ---")
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    APP_NAME = "video_generation_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"
    session = session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    runner_agent_team = Runner( # Or use InMemoryRunner
        agent=director_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )
    print(f"Runner created for agent '{director_agent.name}'.")

    # --- Interactions using await (correct within async def) ---
    await call_agent_async(query = input_prompt,
                            runner=runner_agent_team,
                            user_id=USER_ID,
                            session_id=SESSION_ID)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Either we win or we learn. we never fail.")
    parser.add_argument(
        "--prompt", 
        type=str, 
        default="",
        help="Prompt to generate a video. (e.g., 'Either we win or we learn. we never fail.')"
    )
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_args()
    
    if not args.prompt:
        print("Please provide a prompt with --prompt")
        return
        
    print("Executing using 'asyncio.run()' (for standard Python scripts)...")
    try:
        # This creates an event loop, runs your async function, and closes the loop.
        input_prompt = args.prompt
        asyncio.run(run_team_conversation(args.prompt))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()