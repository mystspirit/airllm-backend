from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from app.airllm_service import AirLLMService

service = AirLLMService()
ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT / "static" / "index.html"


def _json_response(handler: BaseHTTPRequestHandler, code: int, payload: dict[str, Any]) -> None:
    encoded = json.dumps(payload).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(encoded)))
    handler.end_headers()
    handler.wfile.write(encoded)


def _read_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length) if length else b"{}"
    return json.loads(raw.decode("utf-8"))


class AirLLMRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            content = INDEX_FILE.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if self.path == "/api/status":
            current = service.status()
            _json_response(self, HTTPStatus.OK, current.__dict__)
            return

        _json_response(self, HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/api/load-model":
            try:
                data = _read_json(self)
                model_name = str(data.get("model_name", "")).strip()
                if not model_name:
                    _json_response(
                        self,
                        HTTPStatus.BAD_REQUEST,
                        {"detail": "model_name is required"},
                    )
                    return
                current = service.load_model(model_name)
                _json_response(self, HTTPStatus.OK, current.__dict__)
                return
            except Exception as exc:  # noqa: BLE001
                _json_response(
                    self,
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"detail": f"Model loading failed: {exc}"},
                )
                return

        if self.path == "/api/generate":
            try:
                data = _read_json(self)
                prompt = str(data.get("prompt", "")).strip()
                if not prompt:
                    _json_response(
                        self, HTTPStatus.BAD_REQUEST, {"detail": "prompt is required"}
                    )
                    return
                max_new_tokens = int(data.get("max_new_tokens", 128))
                output = service.generate(prompt, max_new_tokens=max_new_tokens)
                _json_response(self, HTTPStatus.OK, {"output": output})
                return
            except RuntimeError as exc:
                _json_response(self, HTTPStatus.BAD_REQUEST, {"detail": str(exc)})
                return
            except Exception as exc:  # noqa: BLE001
                _json_response(
                    self,
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"detail": f"Generation failed: {exc}"},
                )
                return

        _json_response(self, HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def log_message(self, _format: str, *args: Any) -> None:
        return


def public_url(host: str, port: int) -> str:
    if host in {"0.0.0.0", "::"}:
        return f"http://localhost:{port}"
    return f"http://{host}:{port}"


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), AirLLMRequestHandler)
    print(f"AirLLM backend is running on {public_url(host, port)}")
    server.serve_forever()


if __name__ == "__main__":
    run()
