# Contributing

The point of this repository is a single self-contained HTML file that an agent can copy and fill in. That constraint decides most questions.

## Welcome

- Bug reports, especially with a browser and version, and the map file that shows the problem.
- Fixes to the template's behaviour, accessibility or print output.
- New example maps — particularly writing-recovery maps, which the repository is short of.
- Corrections to the wording of `SKILL.md` when a model reads it the wrong way. Say what the model did.

## Not taken

- Frameworks, bundlers, build steps, package manifests, or a dependency on any CDN.
- Remote fonts, analytics, telemetry, or anything else the map would fetch at runtime.
- Deeper outlining: moving individual leaves between branches is deliberately out of scope for this version.

## Before opening a pull request

```sh
scripts/check.sh assets/template.html   # placeholders make this one fail by design
scripts/check.sh examples/*.html
```

The template and the examples carry identical CSS and script. A change to the template belongs in the examples in the same commit.
