from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "eibee" / "SKILL.md"
README = ROOT / "README.md"
LICENSE = ROOT / "LICENSE"
VERSION = ROOT / "eibee" / "VERSION"
WINDOWS_UPDATER = ROOT / "eibee" / "scripts" / "update-skill.ps1"
UNIX_UPDATER = ROOT / "eibee" / "scripts" / "update-skill.sh"
AI_VOICE_SCANNER = ROOT / "eibee" / "scripts" / "ai_voice_scanner.py"
AI_VOICE_CORPUS = ROOT / "eibee" / "references" / "ai-voice-corpus.json"


def test_public_package_has_a_skill_and_install_guide():
    assert SKILL.is_file()
    assert README.is_file()
    assert LICENSE.is_file()
    assert "C:\\Users" not in README.read_text(encoding="utf-8")


def test_package_declares_mit_license():
    assert "MIT License" in LICENSE.read_text(encoding="utf-8")


def test_package_includes_explicit_user_triggered_updaters():
    assert VERSION.is_file()
    assert WINDOWS_UPDATER.is_file()
    assert UNIX_UPDATER.is_file()
    assert "coconut4210/eibee-content-factory" in WINDOWS_UPDATER.read_text(encoding="utf-8")
    assert "coconut4210/eibee-content-factory" in UNIX_UPDATER.read_text(encoding="utf-8")


def test_readme_offers_a_copy_paste_install_command():
    text = README.read_text(encoding="utf-8")
    assert "https://github.com/coconut4210/eibee-content-factory/tree/main/eibee" in text


def test_skill_is_portable_and_has_no_private_automation_or_paths():
    text = SKILL.read_text(encoding="utf-8").lower()
    forbidden = (
        "shadowbot",
        "影刀",
        "rpa-launcher",
        "ready.flag",
        "run_web.py",
        "start.bat",
        "localhost:8000",
        "eibee-calendar-cache",
        "knowledge-base",
        "<workspace>/upload",
    )
    assert not any(term in text for term in forbidden)


def test_skill_preserves_portable_content_quality_controls():
    text = SKILL.read_text(encoding="utf-8")
    for required in (
        "事实锚点",
        "P0",
        "P1",
        "P2",
        "传统替代测试",
        "功能清晰度",
        "4:5（1080 × 1350）",
        "blocking_count",
    ):
        assert required in text


def test_package_includes_versioned_ai_voice_quality_gate():
    assert AI_VOICE_SCANNER.is_file()
    assert AI_VOICE_CORPUS.is_file()
    skill = SKILL.read_text(encoding="utf-8")
    assert "ai_voice_scanner.py" in skill
    assert "阻断项" in skill


def test_ai_voice_corpus_blocks_recurrent_manufactured_contrasts():
    import importlib.util

    spec = importlib.util.spec_from_file_location("ai_voice_scanner", AI_VOICE_SCANNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    report = module.scan_text("这不是一张名单，而是一套增长引擎。")
    assert report["passed"] is False
    assert report["blocking_count"] == 1
    assert report["findings"][0]["rule_id"] == "zh-negative-parallelism"


def test_ai_voice_scanner_ignores_direct_concrete_copy():
    import importlib.util

    spec = importlib.util.spec_from_file_location("ai_voice_scanner", AI_VOICE_SCANNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    report = module.scan_text("发过了吗？对方回了吗？打开邀约列表查看当前状态。")
    assert report["passed"] is True
    assert report["blocking_count"] == 0
