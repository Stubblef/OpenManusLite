from openmanuslite.agent.toolcall import ToolCallAgent
from openmanuslite.schema import Memory, Message
from openmanuslite.tools.tool_collection import ToolCollection
from openmanuslite.tools.create_chat_completion import CreateChatCompletion
from openmanuslite.tools.pyexec import PythonExecute

SYSTEM_PROMPT = (
    "You are OpenManus, an all-capable AI assistant, aimed at solving any task presented by the user. "
    "You have various tools at your disposal that you can call upon to efficiently complete complex requests. "
    "Whether it's programming, information retrieval, file processing, or web browsing, you can handle it all."
    "The initial directory is: {directory}"
)

NEXT_STEP_PROMPT = """
Based on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps.
"""


class Manus(ToolCallAgent):
    name: str = "Manus"
    description: str = "A versatile agent that can solve various tasks using multiple tools"
    
    system_prompt: str = SYSTEM_PROMPT.format(
        directory="/mnt/data"  # Example initial directory, adjust as needed
    )
    next_step_prompt: str = NEXT_STEP_PROMPT
    memory: Memory = Memory()  # Initialize memory
    
    available_tools: ToolCollection = ToolCollection(
        # CreateChatCompletion(),
        PythonExecute(),
    )  # Terminate()
    
    
    async def think(self) -> bool:
        """Process current state and decide next actions with appropriate context."""
        # Store the original prompt
        original_prompt = self.next_step_prompt
        
        # Call parent think method
        result = await super().think()
        
        # Restore original prompt
        self.next_step_prompt = original_prompt
        
        return result
    
async def main():
    agent = Manus()
    prompt = "写一个Python脚本，计算1到100的和"
    
    # Initialize memory with user request
    # agent.memory.add_message(Message(role="user", content=prompt))
    
    await agent.run(request=prompt)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())