# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Explicit support for Python 3.9

### Fixed
- Add documentation to `layaberr.flask_restx.add_error_handlers`.

## [3.0.0.dev0] - 2020-10-02
### Removed
- All [Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/) exceptions and handlers have been removed as this project is now dead. Stick to layaberr version 2 for flask-restplus support.

### Added
- Add `layaberr.starlette` module providing [Starlette](https://www.starlette.io) exceptions and handlers.
- Add `layaberr.flask_restx` module providing [flask-restx](https://flask-restx.readthedocs.io/en/latest/) exceptions and handlers.

## [2.2.0] - 2019-12-02
### Added
- Initial release.

[Unreleased]: https://github.com/Colin-b/layaberr/compare/v3.0.0.dev0...HEAD
[3.0.0.dev0]: https://github.com/Colin-b/layaberr/compare/v2.2.0...v3.0.0.dev0
[2.2.0]: https://github.com/Colin-b/layaberr/releases/tag/v2.2.0
