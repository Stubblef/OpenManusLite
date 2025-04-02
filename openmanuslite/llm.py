from openai import AsyncOpenAI
from typing import Dict, List, Optional, Union
from openmanuslite.schema import Message, Role
from openmanuslite.config.config import config

class LLM:
    _instances = {}

    def __new__(cls, config_name: str = "default", llm_config = None):
        if config_name not in cls._instances:
            instance = super().__new__(cls)
            if llm_config is None:
                llm_config = config.llm
            instance.__init__(config_name, llm_config)
            cls._instances[config_name] = instance
        return cls._instances[config_name]

    def __init__(self, config_name: str = "default", llm_config = None):
        if not hasattr(self, "client"): 
            llm_config = llm_config.get(config_name)
            self.model = llm_config.model
            self.max_tokens = llm_config.max_tokens
            self.temperature = llm_config.temperature
            self.api_key = llm_config.api_key
            self.base_url = llm_config.base_url
            self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    @staticmethod
    def format_messages(messages: List[Union[dict, Message]], supports_images: bool = False) -> List[dict]:
        formatted_messages = []
        for message in messages:
            if isinstance(message, Message):
                message = message.to_dict()
                
            
            if isinstance(message, dict):
                if "role" not in message:
                    raise ValueError("Message dict must contain 'role' field")
                
                if supports_images and message.get("base64_image"):
                    if not message.get("content"):
                        message["content"] = []
                    elif isinstance(message["content"], str):
                        message["content"] = [{"type": "text", "text": message["content"]}]
                    
                    message["content"].append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{message['base64_image']}"}
                    })
                    del message["base64_image"]
                
                if "content" in message or "tool_calls" in message:
                    formatted_messages.append(message)
            else:
                raise TypeError(f"Unsupported message type: {type(message)}")
        return formatted_messages

    async def ask(self, messages: List[Union[dict, Message]], 
                 system_msgs: Optional[List[Union[dict, Message]]] = None,
                 stream: bool = True,
                 temperature: Optional[float] = None) -> str:
        # supports_images = self.model in MULTIMODAL_MODELS
        supports_images = True  # 临时强制支持多模态，后续根据实际模型支持情况调整
        
        if system_msgs:
            messages = self.format_messages(system_msgs, supports_images) + self.format_messages(messages, supports_images)
        else:
            messages = self.format_messages(messages, supports_images)

        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature
        }

        if not stream:
            response = await self.client.chat.completions.create(**params, stream=False)
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("Empty or invalid response from LLM")
            return response.choices[0].message.content

        response = await self.client.chat.completions.create(**params, stream=True)
        collected_messages = []
        async for chunk in response:
            chunk_message = chunk.choices[0].delta.content or ""
            collected_messages.append(chunk_message)
            print(chunk_message, end="", flush=True)

        print()
        full_response = "".join(collected_messages).strip()
        if not full_response:
            raise ValueError("Empty response from streaming LLM")
        return full_response


def main():
    import argparse
    import asyncio
    from openmanuslite.schema import Message
    parser = argparse.ArgumentParser(description="LLM CLI")
    parser.add_argument("--config", type=str, default="default", help="LLM config name")
    parser.add_argument("--message", type=str, required=True, help="Input message for the LLM")
    args = parser.parse_args()
    
    config_name = args.config
    message = args.message
    llm_instance = LLM(config_name=config_name)  # llm_config=llm_config
    
    async def run():
        messages = [Message(role="user", content=message)]
        try:
            response = await llm_instance.ask(messages, stream=True)
            print(f"\nLLM Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
            
    asyncio.run(run())
    
if __name__ == "__main__":
    main()