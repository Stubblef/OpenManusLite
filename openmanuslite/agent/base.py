from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from openmanuslite.llm import LLM
from openmanuslite.schema import AgentState, Memory, Message


class BaseAgent(BaseModel, ABC):
    name: str = Field(..., description="Unique name of the agent")
    description: Optional[str] = Field(None, description="Optional agent description")

    system_prompt: Optional[str] = Field(
        None, description="System-level instruction prompt"
    )
    next_step_prompt: Optional[str] = Field(
        None, description="Prompt for determining next action"
    )

    # Dependencies
    llm: LLM = Field(default_factory=LLM, description="Language model instance")
  
    max_steps: int = Field(default=10, description="Maximum steps before termination")
    current_step: int = Field(default=0, description="Current step in execution")

    duplicate_threshold: int = 2

    async def run(self, request: Optional[str] = None) -> str:

        results: List[str] = []
        while (self.current_step < self.max_steps):
            self.current_step += 1
            print(f"Executing step {self.current_step}/{self.max_steps}")
            step_result = await self.step()

            # Check for stuck state
            if self.is_stuck():
                self.handle_stuck_state()

            results.append(f"Step {self.current_step}: {step_result}")

        if self.current_step >= self.max_steps:
            self.current_step = 0
            # self.state = AgentState.IDLE
            results.append(f"Terminated: Reached max steps ({self.max_steps})")
        # await SANDBOX_CLIENT.cleanup()
        return "\n".join(results) if results else "No steps executed"

