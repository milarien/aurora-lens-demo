"""Static public demo client invariants (no private runtime, no local evaluate API)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

# Constructed so this test file does not itself contain banned host/path literals.
_RAILWAY_APP = "railway" + ".app"
_UP_RAILWAY = "up." + _RAILWAY_APP
_RAILWAY_ENV_PREFIX = "RAIL" + "WAY_"
_PROD_SLUG = "auroralens" + "-production"
_PRIVATE_DIST = "private" + "-dist"
_API_EVALUATE = "/api/" + "evaluate"


def _repo_text_files() -> list[Path]:
    skip_dirs = {
        ".git",
        ".pytest_cache",
        "__pycache__",
        ".claude",
        ".venv",
        "venv",
        "node_modules",
        "audit",
        "dist",
        "build",
        ".egg-info",
    }
    out: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs or part.endswith(".egg-info") for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".pyc"}:
            continue
        out.append(path)
    return out


def _private_aurora_import(raw: str) -> bool:
    """True if private runtime ``aurora_lens`` (not ``aurora_lens_demo``) is imported."""
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("#"):
            continue
        if "import aurora_lens_demo" in s or "from aurora_lens_demo" in s:
            continue
        if s == "import aurora_lens" or s.startswith("import aurora_lens."):
            return True
        if s.startswith("from aurora_lens ") or s.startswith("from aurora_lens."):
            return True
        if s.startswith("from aurora_lens import"):
            return True
    return False


def test_index_html_is_interactive_demo() -> None:
    assert INDEX.is_file()
    text = INDEX.read_text(encoding="utf-8")
    assert "execution-boundary demo" in text
    assert 'id="freetext-submit-btn"' in text
    assert 'id="run-scenario-btn"' in text
    assert "DOMAIN_SCENARIOS" in text
    assert "/v1/chat/completions" in text
    assert "/v1/session/new-scenario" in text
    assert "js/main.js" not in text


def test_api_base_targets_aurora_lens_ai_v1() -> None:
    text = INDEX.read_text(encoding="utf-8")
    assert 'name="aurora-lens-api-base" content="https://aurora-lens.ai"' in text
    assert 'serviceBase() + "/v1/chat/completions"' in text
    assert 'serviceBase() + "/v1/session/new-scenario"' in text
    assert 'fetchServiceJson("/v1/audit/verify' in text


def test_no_railway_hostname_in_repo() -> None:
    forbidden = (_RAILWAY_APP, _UP_RAILWAY, _RAILWAY_ENV_PREFIX, _PROD_SLUG)
    offenders: list[str] = []
    for path in _repo_text_files():
        if path.name == "test_static_demo_client.py":
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        lower = raw.lower()
        for needle in forbidden:
            if needle.lower() in lower:
                offenders.append(f"{path.relative_to(ROOT)}:{needle}")
    assert offenders == [], offenders


def test_no_private_runtime_imports_or_wheel_paths() -> None:
    offenders: list[str] = []
    for path in _repo_text_files():
        if path.name == "test_static_demo_client.py":
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if _private_aurora_import(raw):
            offenders.append(f"{path.relative_to(ROOT)}:aurora_lens_import")
        if "aurora_lens-" in raw and ".whl" in raw:
            offenders.append(f"{path.relative_to(ROOT)}:wheel")
        if _PRIVATE_DIST in raw:
            offenders.append(f"{path.relative_to(ROOT)}:private-dist")
        if "pip install /private" in raw:
            offenders.append(f"{path.relative_to(ROOT)}:private_pip")
    assert offenders == [], offenders


def test_no_docker_or_public_demo_backend() -> None:
    assert not (ROOT / "Dockerfile").exists()
    assert not (ROOT / "Dockerfile.dockerignore").exists()
    assert not (ROOT / "src" / "public_demo").exists()
    assert not (ROOT / "tests" / "test_public_demo.py").exists()


def test_no_api_evaluate_contract() -> None:
    offenders: list[str] = []
    for path in _repo_text_files():
        if path.name == "test_static_demo_client.py":
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if _API_EVALUATE in raw:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], offenders


def test_demo_assets_present() -> None:
    assert (ROOT / "logo.png").is_file()
    assert (ROOT / "assets" / "images" / "gate-diagram.png").is_file()
