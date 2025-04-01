import asyncio
import json
from typing import Any, List, Optional, Union

from pydantic import Field

from openmanuslite.agent.react import ReActAgent
# from app.exceptions import TokenLimitExceeded
from openmanuslite.logger import logger
# from app.prompt.toolcall import NEXT_STEP_PROMPT, SYSTEM_PROMPT
# from app.schema import TOOL_CHOICE_TYPE, AgentState, Message, ToolCall, ToolChoice
# from app.tool import CreateChatCompletion, Terminate, ToolCollection


TOOL_CALL_REQUIRED = "Tool calls required but none provided"


class ToolCallAgent(ReActAgent):
    """Base agent class for handling tool/function calls with enhanced abstraction"""

    name: str = "toolcall"
    description: str = "an agent that can execute tool calls."

    # system_prompt: str = SYSTEM_PROMPT
    # next_step_prompt: str = NEXT_STEP_PROMPT

    # available_tools: ToolCollection = ToolCollection(
    #     CreateChatCompletion(), Terminate()
    # )
    # tool_choices: TOOL_CHOICE_TYPE = ToolChoice.AUTO  # type: ignore
    # special_tool_names: List[str] = Field(default_factory=lambda: [Terminate().name])

    # tool_calls: List[ToolCall] = Field(default_factory=list)
    _current_base64_image: Optional[str] = None

    max_steps: int = 30
    max_observe: Optional[Union[int, bool]] = None

    async def run(self, request: Optional[str] = None) -> str:
        """Run the agent with cleanup when done."""
        try:
            return await super().run(request)
        finally:
            await self.cleanup()
