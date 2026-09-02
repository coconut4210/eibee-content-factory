from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "eibee" / "SKILL.md"
README = ROOT / "README.md"
LICENSE = ROOT / "LICENSE"
VERSION = ROOT / "eibee" / "VERSION"
WINDOWS_UPDATER = ROOT / "eibee" / "scripts" / "update-skill.ps1"
UNIX_UPDATER = ROOT / "eibee" / "scripts" / "update-skill.sh"


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
        "10%",
    ):
        assert required in text
