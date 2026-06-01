import warnings
import urllib3
import httpx
from openai import OpenAI
from typing import Optional, List, Dict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")


class BaseAgent:
    """Base class for all AI agents. Uses the custom OpenAI-compatible gateway."""

    GATEWAY_URL = "https://keygateway.arshnivlabs.com/v1"
    GATEWAY_KEY = "learner001"
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_MAX_TOKENS = 500  # gateway enforces max 500

    def __init__(self, name: str, system_prompt: str, model: str = DEFAULT_MODEL):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.client = OpenAI(
            api_key=self.GATEWAY_KEY,
            base_url=self.GATEWAY_URL,
            http_client=httpx.Client(verify=False),
        )

    def analyze(
        self,
        user_content: str,
        context: Optional[str] = None,
        max_tokens: int = 500,
    ) -> str:
        """Run the agent against the provided content, with optional prior-agent context."""
        full_content = user_content
        if context:
            full_content = (
                f"=== CONTEXT FROM PRIOR AGENT ANALYSIS ===\n{context}\n"
                f"=== END CONTEXT ===\n\n"
                f"=== DATA TO ANALYZE ===\n{user_content}\n=== END DATA ==="
            )

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_content},
            ],
        )
        return response.choices[0].message.content

    def chat(
        self,
        conversation_history: List[Dict],
        user_message: str,
        context: Optional[str] = None,
    ) -> str:
        """Continue a conversation with the agent, injecting analysis context if provided."""
        system = self.system_prompt
        if context:
            system = (
                f"{self.system_prompt}\n\n"
                f"=== AVAILABLE ANALYSIS CONTEXT ===\n{context}\n=== END CONTEXT ==="
            )

        messages = [{"role": "system", "content": system}]
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.DEFAULT_MAX_TOKENS,
            messages=messages,
        )
        return response.choices[0].message.content
