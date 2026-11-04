# changelog-writer-skill

Turn a git log and a release range into a Keep-a-Changelog entry — with no invented features.

[![CI](https://github.com/hai02487/changelog-writer-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/hai02487/changelog-writer-skill/actions/workflows/ci.yml) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

## What it does

When an AI coding agent loads this skill, it turns the commits in
an exact release range into a Keep-a-Changelog entry:

- Sorts each commit into Added, Changed, Fixed, or Removed —
  Deprecated and Security only when a commit actually says so.
- Writes one plain-words line per change, linked to its commit
  hash, so a reader can check every line against the log.
- Flags breaking changes on the same line, never hidden.
- Excludes non-user-facing commits (chore, CI, build, test-only,
  formatting) and reports them as excluded, not silently dropped.
- Refuses to invent a version number, a release date, a feature,
  or a fix that no commit in the range shows.

## What it does NOT do

- It does not write release marketing, blog posts, or promises
  beyond what the commits show. Those are separate jobs.
- It does not work from a summary, a ticket list, or a memory of
  what changed. No log for the range, no entry.
- It does not describe uncommitted work, and it does not edit
  CHANGELOG.md, commit, or tag a release by itself. Writing the
  entry is the whole job; the user places it and releases it.
- It does not claim tests pass, a release shipped, or users are
  affected unless the log or the user actually shows it.

## Who it is for

Maintainers who publish releases and want a changelog readers can
verify — teammates, reviewers, and anyone checking what actually
changed between two versions, without marketing fluff.

## Install

This skill follows the open Agent Skills format: a folder with a
`SKILL.md` file.

**Claude Code / Codex / Gemini CLI (project level):**

```bash
mkdir -p .agents/skills
cp -r skills/changelog-writer .agents/skills/changelog-writer
```

## Usage

Ask the agent to write a changelog entry, giving the exact range
(two tags, a tag and HEAD, or a list of commits). The agent
follows `skills/changelog-writer/SKILL.md` and returns the entry
in a code block, every commit grouped as included or excluded,
and anything deliberately left out.

## Example

From `examples/sample-git-log.txt` (five commits, one of them a
chore), the skill produces `examples/sample-changelog.md`:

```markdown
## [Unreleased]

### Added

- Fuzzy matching in search results (a1b2c3d)

### Changed

- Search results are sorted by relevance first (d4e5f6a)

### Fixed

- Expired tokens are rejected instead of refreshed (b2c3d4e)

### Removed

- Legacy list_users endpoint (c3d4e5f)
  BREAKING CHANGE: list_users is removed. Callers must use
  list_customers, which takes the same arguments.
```

The chore dependency bump (`e5f6a7b`) is reported as excluded,
not turned into a changelog line, and no version or date is
invented — the heading stays `## [Unreleased]`.

## How it is tested

```bash
python3 tests/test_skill.py
```

The tests check that `SKILL.md` has valid `name` and `description`
frontmatter, the required workflow sections, and no unfinished
placeholder content; and that the sample changelog matches the
sample log exactly — every included hash present, every section
present, the chore commit excluded, the breaking change flagged,
and no invented version or date.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests
are welcome; please keep examples real and checkable.

## Licence

MIT — see [LICENSE](LICENSE). This is original work, built from
the public Keep-a-Changelog format (a format, not copied text).
