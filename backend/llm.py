# llm.py - LLM Client for OpenRouter/DeepSeek
import time
import logging
from openai import OpenAI

from config import Config

logger = logging.getLogger("be_aware_backend")


class LLMClient:
    """Client for calling OpenRouter/DeepSeek LLM"""

    def __init__(self):
        """Initialize LLM client with OpenRouter API"""
        self.client = None
        self.configured = False

        if Config.OPENROUTER_API_KEY:
            try:
                self.client = OpenAI(
                    api_key=Config.OPENROUTER_API_KEY,
                    base_url="https://openrouter.ai/api/v1"
                )
                self.configured = True
                logger.info("✅ OpenRouter (DeepSeek) client configured")
            except Exception as e:
                logger.exception("⚠️ Failed to configure OpenRouter client: %s", e)
        else:
            logger.warning("⚠️ OPENROUTER_API_KEY not set. LLM calls will fail until configured.")

    def call(self, prompt: str,
             model: str = None,
             temperature: float = None,
             max_tokens: int = None,
             max_retries: int = None,
             timeout: int = None) -> str:
        """
        Call the LLM with retry logic.

        Args:
            prompt: The prompt to send to the LLM
            model: Model to use (defaults to Config.LLM_MODEL)
            temperature: Temperature setting (defaults to Config.LLM_TEMPERATURE)
            max_tokens: Max tokens to generate (defaults to Config.LLM_MAX_TOKENS)
            max_retries: Number of retries (defaults to Config.LLM_MAX_RETRIES)
            timeout: Request timeout in seconds (defaults to Config.LLM_TIMEOUT)

        Returns:
            LLM response text

        Raises:
            RuntimeError: If client not configured or all retries fail
        """
        if not self.configured or not self.client:
            raise RuntimeError("LLM client not configured. Set OPENROUTER_API_KEY in environment.")

        # Use defaults from config if not specified
        model = model or Config.LLM_MODEL
        temperature = temperature if temperature is not None else Config.LLM_TEMPERATURE
        max_tokens = max_tokens or Config.LLM_MAX_TOKENS
        max_retries = max_retries or Config.LLM_MAX_RETRIES
        timeout = timeout or Config.LLM_TIMEOUT

        for attempt in range(1, max_retries + 1):
            try:
                logger.info("🤖 LLM request (attempt %s/%s) model=%s", attempt, max_retries, model)

                resp = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=timeout
                )

                result = resp.choices[0].message.content.strip()
                logger.info("✅ LLM returned result (length=%d)", len(result))
                return result

            except Exception as e:
                logger.warning("⚠️ LLM attempt %s failed: %s", attempt, e)
                if attempt < max_retries:
                    wait = 2 ** (attempt - 1)
                    logger.info("⏳ waiting %s seconds before retry", wait)
                    time.sleep(wait)
                else:
                    logger.exception("❌ LLM retries exhausted")
                    raise

    def test_connection(self) -> dict:
        """
        Test the LLM connection.

        Returns:
            Dictionary with success status and response
        """
        if not self.configured:
            return {
                "success": False,
                "error": "LLM client not configured"
            }

        try:
            response = self.call(
                prompt="Say 'Hello, I am working!' in exactly those words.",
                max_tokens=50,
                timeout=10
            )
            return {
                "success": True,
                "response": response
            }
        except Exception as e:
            logger.exception("LLM test failed: %s", e)
            return {
                "success": False,
                "error": str(e)
            }