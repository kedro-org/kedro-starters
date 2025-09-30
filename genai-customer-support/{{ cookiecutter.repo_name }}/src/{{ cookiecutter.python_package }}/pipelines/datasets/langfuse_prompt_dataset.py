import json
import hashlib
from pathlib import Path
from typing import Any, Literal

from kedro.io import AbstractDataset
from langchain.prompts import ChatPromptTemplate
from langfuse import Langfuse


def _hash(data: str | list) -> str:
    """Return SHA-256 hash of a prompt (string or list of messages)."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def _get_content(data: str | list) -> str:
    """
    Extract comparable text content from a prompt.
    - If string: return as-is.
    - If list of messages: join their `content`.
    """
    if isinstance(data, str):
        return data
    return "\n".join(msg["content"] for msg in data)


class PromptDataset(AbstractDataset):
    """
    Kedro dataset for managing LangChain prompts with Langfuse versioning.

    Behavior:
    - On save: writes prompt JSON to disk and creates/updates it in Langfuse.
    - On load: prefers local file, syncs with Langfuse, ensures reproducibility.
    - Returns LangChain `ChatPromptTemplate` when loaded.
    """

    def __init__(
        self,
        filepath: str,
        prompt_name: str,
        credentials: dict[str, Any],
        prompt_type: Literal["chat", "text"] = "text",
    ):
        """
        Args:
            filepath: Local JSON file path for storing prompt.
            prompt_name: Unique identifier for the prompt in Langfuse.
            prompt_type: Either "chat" or "text".
            credentials: Dict with Langfuse credentials {public_key, secret_key, host}.
        """
        self._filepath = Path(filepath)
        self._prompt_name = prompt_name
        self._prompt_type: Literal["chat", "text"] = prompt_type
        self._langfuse = Langfuse(
            public_key=credentials["public_key"],
            secret_key=credentials["secret_key"],
            host=credentials["host"],
        )

    def _describe(self):
        return {"filepath": self._filepath, "prompt_name": self._prompt_name}

    def save(self, data: str) -> None:
        """
        Save prompt to local JSON and push to Langfuse.
        If prompt already exists in Langfuse, a new version is created.
        """
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self._langfuse.create_prompt(
            name=self._prompt_name,
            prompt=data,
            type=self._prompt_type,
        )

    def _sync_with_langfuse(
        self, local_data: str | None, langfuse_prompt: Any | None
    ) -> Any:
        """
        Ensure local file and Langfuse prompt are consistent.
        Returns latest Langfuse prompt after synchronization.

        Cases handled:
        - Local exists but not in Langfuse → push local to Langfuse.
        - Both exist but differ → update Langfuse with local.
        - Only Langfuse exists → write to local.
        """
        if local_data is not None:
            if langfuse_prompt is None:
                # Push local to Langfuse
                self.save(local_data)
                return self._langfuse.get_prompt(
                    self._prompt_name, type=self._prompt_type, label="latest"
                )

            # If mismatch → update Langfuse
            if _hash(_get_content(local_data)) != _hash(
                _get_content(langfuse_prompt.prompt)
            ):
                self.save(local_data)
                return self._langfuse.get_prompt(
                    self._prompt_name, type=self._prompt_type, label="latest"
                )
            return langfuse_prompt

        # If local missing but Langfuse exists → persist locally
        if langfuse_prompt:
            self._filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(langfuse_prompt.prompt, f, indent=2)
            return langfuse_prompt

        raise FileNotFoundError(
            f"No prompt found locally or in Langfuse for '{self._prompt_name}'"
        )

    def load(self) -> ChatPromptTemplate:
        """
        Load prompt with synchronization logic.
        Returns LangChain `ChatPromptTemplate`.
        """
        try:
            langfuse_prompt = self._langfuse.get_prompt(
                self._prompt_name, type=self._prompt_type, label="latest"
            )
        except Exception:
            langfuse_prompt = None

        local_data = None
        if self._filepath.exists():
            with open(self._filepath, "r", encoding="utf-8") as f:
                local_data = json.load(f)

        langfuse_prompt = self._sync_with_langfuse(local_data, langfuse_prompt)

        return ChatPromptTemplate.from_messages(langfuse_prompt.get_langchain_prompt())
