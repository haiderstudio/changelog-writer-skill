---
name: changelog-writer
description: Turn a git log and a release range into a Keep-a-Changelog entry. Use when a user asks to write, update, or check a changelog for a release, or to turn recent commits into Added, Changed, Fixed, or Removed notes. Works only from the actual commits in the range, never invents features, and links every entry to its commit.
---

# changelog-writer

Write a changelog a reader can trust: every line traces to a real
commit in the release range, in Keep-a-Changelog format, with nothing
invented and nothing important hidden.

## When to use this skill

Use it when the user asks to:
- Write a changelog entry for a release, a version, or an
  unreleased range of commits.
- Update an existing CHANGELOG.md with a new release section.
- Turn a git log into Added, Changed, Fixed, or Removed notes.
- Check a changelog entry against the commits it claims to cover.

## When NOT to use it

- Do not use it to write release marketing, blog posts, or release
  notes that promise more than the commits show. Those are separate
  jobs; this skill writes the changelog only.
- Do not use it from a summary, a ticket list, or a memory of what
  changed. Read the git log for the exact range first.
- Do not use it to describe work that is not committed yet. If a
  change is uncommitted, it does not belong in a release entry.
- Do not use it as a commit-message writer or a code reviewer.
  Those are separate jobs with their own rules.

## Workflow

### 1. Fix the range, and read every commit in it

1. Confirm the exact range with the user: two tags, a tag and HEAD,
   or an explicit list of commits. A vague range ("recent work",
   "the last few changes") is not a range — ask, do not guess.
2. List every commit in the range: short hash, type, scope, and
   subject, in chronological order.
3. Read each commit's diff well enough to say what it changed for a
   user. A subject line alone is not proof; check the diff when a
   subject is vague or surprising.

### 2. Sort each commit into one Keep-a-Changelog section

- `Added` — a new user-facing capability.
- `Changed` — a change to existing behaviour, including a breaking
  change (flagged as breaking, see step 3).
- `Fixed` — a bug fix for existing behaviour.
- `Removed` — a capability, option, or endpoint that is gone.
- `Deprecated` and `Security` — only when a commit actually says
  so; never add these sections to fill space.

Commits that are not user-facing are excluded, and listed as
excluded (see step 4): `chore`, `ci`, `build` maintenance, test-only
changes, and pure formatting. A documentation-only change is listed
under `Changed` only when it changes what a user must do; a typo
fix in docs is excluded, not promoted to a feature.

### 3. Write one line per change, linked to its commit

Format for each line:

```markdown
- <what changed, in plain words> (<short hash>)
```

Rules for every line:
- One change per line. A commit that does two user-facing things
  gets two lines, each with the same hash.
- Past tense is wrong here: write what the release does, not what
  was done to it — "Fuzzy matching in search results", not
  "Added fuzzy matching".
- A breaking change carries its flag on the same line:
  `BREAKING CHANGE: <what breaks and what to do instead>`.
- Never write a feature, a fix, or a date that no commit in the
  range shows. If the range shows no change in a section, that
  section is omitted entirely — never written as "None" or filled
  with a guess.
- The version heading is `## [Unreleased]` when no version number
  was given, or `## [x.y.z] - YYYY-MM-DD` when the user gave both.
  Never invent a version number or a release date.

### 4. Report in this fixed format

1. The changelog entry, in a code block, ready to paste.
2. Every commit in the range, grouped: included (with its section)
   or excluded (with the exact reason).
3. Anything deliberately left out: a commit that could not be
   classified from its diff, a version number not supplied, a date
   not supplied — listed by name, with why it was left out.

## Good examples

A release with one entry in each main section (from the sample log
in `examples/sample-git-log.txt`):

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

An excluded commit is never hidden: the sample log's `chore`
dependency bump is reported as excluded, not turned into a line.

## Bad examples (do not write like this)

> `### Added`
>
> `- Lots of improvements and bug fixes`

No change named, no commit linked, nothing a reader can check.

> `### Added`
>
> `- Faster search, better security, new dashboard`

Three claims, no commits shown for any of them. If the log does
not show a dashboard, there is no dashboard in the changelog.

> `## [2.0.0] - 2026-01-01`

A version and a date nobody supplied. Invented headings are
invented claims, even when they look tidy.

## Output rules

- Output one entry per release range, in its own code block.
- Every line in the entry must trace to a commit in the range.
  If it cannot be traced, leave it out and list it as
  deliberately omitted.
- Never invent a version, a date, a feature, a fix, or a commit
  hash. A hash in the entry is a hash from the log, copied exactly.
- Never claim tests pass, a release shipped, or users are affected
  unless the log or the user actually shows it.
- Never edit CHANGELOG.md, commit, or tag a release by itself.
  Writing the entry is the whole job; the user places it and
  releases it, after reading it.

## Limits and safety rules

- This skill reads git logs and diffs only. It sends nothing
  anywhere, edits no file, commits nothing, and tags nothing.
- It does not work from a remembered or summarised change. If
  there is no log for the range, the report says so and stops at
  that fact; it does not invent one.
- Local fixture logs (see `examples/sample-git-log.txt`) cannot
  prove a live version, a live date, or a live release. A
  walkthrough run on fixtures uses `## [Unreleased]` and marks
  version and date as deliberately omitted, exactly as the sample
  entry does.
