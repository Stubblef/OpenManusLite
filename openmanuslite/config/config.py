import threading
from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel, Field
from hyperpyyaml import load_hyperpyyaml
from openmanuslite.logger import logger
from openmanuslite.config.base import BaseConfig


PROJECT_ROOT = Path(__file__).resolve().parent  # 获取项目根目录的绝对路径
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
logger.debug(f"PROJECT_ROOT: {PROJECT_ROOT}, WORKSPACE_ROOT: {WORKSPACE_ROOT}")

class LLMSettings(BaseModel):
    model: str = Field(..., description="Model name")
    base_url: str = Field(..., description="API base URL")
    api_key: str = Field(..., description="API key")
    max_tokens: int = Field(4096, description="Maximum tokens per request")  # 默认值为4096，兼容性考虑
    max_input_tokens: Optional[int] = Field(None, description="Max input tokens")
    temperature: float = Field(1.0, description="Sampling temperature")
    api_type: str = Field("", description="API type: Azure, OpenAI, or Ollama")
    api_version: str = Field("", description="API version")


class Config(BaseConfig):
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, "_config"):
            self._load_config()

    @staticmethod
    def _get_config_path() -> Path:
        config_path = PROJECT_ROOT / "config.yaml"
        logger.debug(f"Loading configuration from: {config_path}")
        if config_path.exists():
            return config_path
        raise FileNotFoundError("No configuration file found")

    def _load_config(self):
        with self._get_config_path().open("r") as f:
            raw_config = load_hyperpyyaml(f)
        
        llm_configs = {}
        base_llm = raw_config.get("llm", {})
        
        for name, config in base_llm.items():
            if isinstance(config, dict):
                llm_configs[name] = LLMSettings(**config)
        
        self.load_config({"llm": llm_configs})
        return llm_configs

    @property
    def llm(self) -> Dict[str, LLMSettings]:
        return self.config_data["llm"]

config = Config()
