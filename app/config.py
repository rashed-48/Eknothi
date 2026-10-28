import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class Settings:
    # Agent model. Any OpenAI-compatible endpoint: a stand-in Llama provider now,
    # Muse Spark Open on Baseten / Meta Model API once credits arrive.
    llm_base_url: str = _env("LLM_BASE_URL")
    llm_api_key: str = _env("LLM_API_KEY")
    llm_model: str = _env("LLM_MODEL")

    # Vision and speech can live on a different provider than the agent.
    # Each falls back to the agent settings when left empty.
    vision_base_url: str = _env("VISION_BASE_URL") or _env("LLM_BASE_URL")
    vision_api_key: str = _env("VISION_API_KEY") or _env("LLM_API_KEY")
    vision_model: str = _env("VISION_MODEL") or _env("LLM_MODEL")

    asr_base_url: str = _env("ASR_BASE_URL") or _env("LLM_BASE_URL")
    asr_api_key: str = _env("ASR_API_KEY") or _env("LLM_API_KEY")
    asr_model: str = _env("ASR_MODEL")

    # WhatsApp Cloud API
    wa_token: str = _env("WHATSAPP_TOKEN")
    wa_phone_number_id: str = _env("WHATSAPP_PHONE_NUMBER_ID")
    wa_verify_token: str = _env("WHATSAPP_VERIFY_TOKEN")
    wa_app_secret: str = _env("WHATSAPP_APP_SECRET")
    graph_version: str = _env("GRAPH_API_VERSION", "v21.0")

    public_base_url: str = _env("PUBLIC_BASE_URL", "http://localhost:8000")

    data_dir: Path = ROOT / "data"
    var_dir: Path = Path(_env("EKNOTHI_VAR_DIR") or ROOT / "var")

    @property
    def db_path(self) -> Path:
        return self.var_dir / "eknothi.db"

    @property
    def files_dir(self) -> Path:
        return self.var_dir / "case_files"


settings = Settings()
settings.files_dir.mkdir(parents=True, exist_ok=True)
