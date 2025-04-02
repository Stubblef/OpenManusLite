import argparse
import asyncio
from openmanuslite.llm import LLM
from openmanuslite.schema import Message


# llm_instance = LLM(config_name=config_name)  # llm_config=llm_config

async def run():
    messages = [Message(role="user", content="What is the capital of France?")]
    try:
        response = await llm_instance.ask(messages, stream=True)
        print(f"\nLLM Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        

if __name__ == "__main__":
    config_name = "default"  # Default LLM config
    llm_instance = LLM(config_name=config_name)  # Re-initialize with the provided config

    asyncio.run(run())