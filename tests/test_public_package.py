from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"


def test_public_package_has_a_skill_and_install_guide():
    assert SKILL.is_file()
    assert README.is_file()
    assert "C:\\Users" not in README.read_text(encoding="utf-8")


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
        "10%",
    ):
        assert required in text
