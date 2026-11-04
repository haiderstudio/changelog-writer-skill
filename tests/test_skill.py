"""Tests for the changelog-writer skill: frontmatter, required sections,
and the sample walkthrough (sample log -> sample changelog, no invented lines)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "changelog-writer" / "SKILL.md"
LOG = ROOT / "examples" / "sample-git-log.txt"
CHANGELOG = ROOT / "examples" / "sample-changelog.md"
README = ROOT / "README.md"
BANNED = ["TODO", "FIXME", "lorem", "coming soon"]


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        sys.exit(1)


def main():
    skill = SKILL.read_text()
    m = re.match(r"---\n(.*?)\n---\n", skill, re.S)
    check("test_skill_frontmatter", bool(m) and "name: changelog-writer" in m.group(1) and "description:" in m.group(1))
    for section in ["When to use this skill", "When NOT to use it", "Workflow", "Good examples", "Bad examples", "Output rules", "Limits and safety rules"]:
        check("test_skill_sections_" + section.split()[0], section in skill)
    for f in [SKILL, LOG, CHANGELOG, README]:
        text = f.read_text()
        check("test_no_placeholders_" + f.name, not any(b in text for b in BANNED))
    log = LOG.read_text()
    changelog = CHANGELOG.read_text()
    for h in ["a1b2c3d", "d4e5f6a", "b2c3d4e", "c3d4e5f"]:
        check("test_sample_hash_" + h, h in changelog)
    check("test_sample_sections", all(s in changelog for s in ["### Added", "### Changed", "### Fixed", "### Removed"]))
    check("test_sample_no_invented_version", "[Unreleased]" in changelog and "2.0.0" not in changelog)
    check("test_sample_chore_excluded", "e5f6a7b" in changelog and "dependency bump" in changelog.lower() and "bump test dependency" not in changelog.split("### Added")[1].split("### Changed")[0])
    check("test_sample_breaking_flagged", "BREAKING CHANGE" in changelog and "list_customers" in changelog)
    check("test_sample_log_hashes", all(h in log for h in ["a1b2c3d", "d4e5f6a", "b2c3d4e", "c3d4e5f", "e5f6a7b"]))
    print("All tests passed.")


if __name__ == "__main__":
    main()
