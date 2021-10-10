# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Implement JWT and OAuth2

## [0.0.4] 2021-10-10

### Added
- User auth with JWT and OAuth2

## [0.0.3] 2021-10-10

### Added
- pagination system and filters

## [0.0.2] 2021-10-09

### Deleted
- Populating data with python script in api entrypoint (dumps are used at db container init instead)

### Added
- CRUD routes for comments

## [0.0.1] 2021-10-08

### Added
- Import python script from web to db ([script](./db/script/write_from_web_to_json.py))
- api route to get episode and character data
- Base files for project (README, CHANGELOG, gitignore)

[0.0.4]: https://github.com/benjmathias/jellyrick/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/benjmathias/jellyrick/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/benjmathias/jellyrick/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/benjmathias/jellyrick/releases/tag/v0.0.1