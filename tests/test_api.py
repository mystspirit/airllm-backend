import json
import threading
import time
import unittest
import urllib.request
from contextlib import closing
from http.server import ThreadingHTTPServer

from app.main import AirLLMRequestHandler


class MockService:
    def __init__(self) -> None:
        self.loaded = False

    def status(self):
        from types import SimpleNamespace

        return SimpleNamespace(
            installed=True,
            model_loaded=self.loaded,
            model_name="mock/model" if self.loaded else None,
            message="ok",
        )

    def load_model(self, _model_name: str):
        self.loaded = True
        return self.status()

    def generate(self, prompt: str, max_new_tokens: int = 128):
        if not self.loaded:
            raise RuntimeError("Model is not loaded. Load a model first from the web UI or API.")
        return f"{prompt} [{max_new_tokens}]"


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app.main as main_module

        cls.original_service = main_module.service
        main_module.service = MockService()

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), AirLLMRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        import app.main as main_module

        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=1)
        main_module.service = cls.original_service

    def _request(self, method: str, path: str, payload=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            method=method,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with closing(urllib.request.urlopen(req)) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_flow(self):
        status, payload = self._request("GET", "/api/status")
        self.assertEqual(status, 200)
        self.assertFalse(payload["model_loaded"])

        status, payload = self._request(
            "POST", "/api/load-model", {"model_name": "mock/model"}
        )
        self.assertEqual(status, 200)
        self.assertTrue(payload["model_loaded"])

        status, payload = self._request(
            "POST", "/api/generate", {"prompt": "Hello", "max_new_tokens": 10}
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["output"], "Hello [10]")


if __name__ == "__main__":
    unittest.main()
