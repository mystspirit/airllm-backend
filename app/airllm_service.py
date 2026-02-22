from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AirLLMStatus:
    installed: bool
    model_loaded: bool
    model_name: str | None
    message: str


def build_import_error_message(exc: Exception) -> str:
    error_text = str(exc)
    base = (
        "AirLLM dependencies are not available. "
        "Install them with `pip install airllm \"optimum<2\"`. "
    )

    if "optimum.bettertransformer" in error_text:
        return (
            base
            + "Your installed `optimum` version is likely incompatible with AirLLM "
            "(missing module `optimum.bettertransformer`). "
            "Try: `pip install --upgrade --force-reinstall \"optimum<2\" airllm`. "
            f"Import error: {error_text}"
        )

    return base + f"Import error: {error_text}"


class AirLLMService:
    def __init__(self) -> None:
        self._airllm_cls = None
        self._model = None
        self._model_name: str | None = None
        self._import_error: str | None = None
        self._load_airllm()

    def _load_airllm(self) -> None:
        try:
            from airllm import AutoModel as airllm_cls  # type: ignore

            self._airllm_cls = airllm_cls
        except Exception as exc:  # noqa: BLE001
            self._import_error = build_import_error_message(exc)

    def load_model(self, model_name: str) -> AirLLMStatus:
        if self._airllm_cls is None:
            return self.status()

        self._model = self._airllm_cls.from_pretrained(model_name)
        self._model_name = model_name
        return self.status()

    def generate(self, prompt: str, max_new_tokens: int = 128) -> str:
        if self._model is None:
            raise RuntimeError(
                "Model is not loaded. Load a model first from the web UI or API."
            )

        outputs = self._model.generate(prompt, max_new_tokens=max_new_tokens)
        if isinstance(outputs, list):
            return "\n".join(str(item) for item in outputs)
        return str(outputs)

    def status(self) -> AirLLMStatus:
        if self._airllm_cls is None:
            return AirLLMStatus(
                installed=False,
                model_loaded=False,
                model_name=None,
                message=self._import_error or "AirLLM is not available.",
            )

        return AirLLMStatus(
            installed=True,
            model_loaded=self._model is not None,
            model_name=self._model_name,
            message="AirLLM is ready" if self._model is not None else "AirLLM installed",
        )
