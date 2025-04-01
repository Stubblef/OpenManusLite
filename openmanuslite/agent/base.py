from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from app.llm import LLM
# from app.logger import logger
# from app.sandbox.client import SANDBOX_CLIENT
# from app.schema import ROLE_TYPE, AgentState, Memory, Message


class BaseAgent(BaseModel, ABC):
    """Abstract base class for managing agent state and execution.

    Provides foundational functionality for state transitions, memory management,
    and a step-based execution loop. Subclasses must implement the `step` method.
    """

    # Core attributes
    name: str = Field(..., description="Unique name of the agent")
    description: Optional[str] = Field(None, description="Optional agent description")

    # Prompts
    system_prompt: Optional[str] = Field(
        None, description="System-level instruction prompt"
    )
    next_step_prompt: Optional[str] = Field(
        None, description="Prompt for determining next action"
    )

    # Dependencies
    llm: LLM = Field(default_factory=LLM, description="Language model instance")
    # memory: Memory = Field(default_factory=Memory, description="Agent's memory store")
    
    # state: AgentState = Field(
    #     default=AgentState.IDLE, description="Current agent state"
    # )

    # Execution control
    max_steps: int = Field(default=10, description="Maximum steps before termination")
    current_step: int = Field(default=0, description="Current step in execution")

    duplicate_threshold: int = 2

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"  # Allow extra fields for flexibility in subclasses

    async def run(self, request: Optional[str] = None) -> str:

        results: List[str] = []
        # async with self.state_context(AgentState.RUNNING):
        while (self.current_step < self.max_steps):
            self.current_step += 1
            # logger.info(f"Executing step {self.current_step}/{self.max_steps}")
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

  