# import argparse
# import asyncio
# from openmanuslite.schema import Message
# from openmanuslite.llm import LLM

# config_name = "default"  # Use the default LLM configuration
# message = "你好"
# llm_instance = LLM(config_name=config_name)  # llm_config=llm_config

# async def run():
#     messages = [Message(role="user", content=message)]
#     try:
#         print("messages:", messages)
#         response = await llm_instance.ask(messages, stream=True)
#         print(f"\nLLM Response: {response}")
#     except Exception as e:
#         print(f"Error: {e}")
        
# asyncio.run(run())

""""""

from openmanuslite.agent.toolcall import ToolCallAgent

SYSTEM_PROMPT = (
    "You are OpenManus, an all-capable AI assistant, aimed at solving any task presented by the user. You have various tools at your disposal that you can call upon to efficiently complete complex requests. Whether it's programming, information retrieval, file processing, or web browsing, you can handle it all."
    "The initial directory is: {directory}"
)

NEXT_STEP_PROMPT = """
Based on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps.
"""


class Manus(ToolCallAgent):
    name: str = "Manus"
    description: str = (
        "A versatile agent that can solve various tasks using multiple tools"
    )
    
    system_prompt: str = SYSTEM_PROMPT.format(
        directory="/mnt/data"  # Example initial directory, adjust as needed
    )
    next_step_prompt: str = NEXT_STEP_PROMPT
    
    # available_tools: ToolCollection = Field(
    #     default_factory=lambda: ToolCollection(
    #         PythonExecute(), BrowserUseTool(), StrReplaceEditor(), Terminate()
    #     )
    # )
    
    async def think(self) -> bool:
        """Process current state and decide next actions with appropriate context."""
        original_prompt = self.next_step_prompt
        recent_messages = self.memory.messages[-3:] if self.memory.messages else []
        # browser_in_use = any(
        #     tc.function.name == BrowserUseTool().name
        #     for msg in recent_messages
        #     if msg.tool_calls
        #     for tc in msg.tool_calls
        # )

        # if browser_in_use:
        #     self.next_step_prompt = (
        #         await self.browser_context_helper.format_next_step_prompt()
        #     )

        result = await super().think()

        # Restore original prompt
        self.next_step_prompt = original_prompt

        return result
    
async def main():
    import asyncio
    
    agent = Manus()
    prompt = "请帮我写一个Python脚本，计算1到100的和"
    
    await agent.run(prompt=prompt)
    
if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error running Manus agent: {e}")