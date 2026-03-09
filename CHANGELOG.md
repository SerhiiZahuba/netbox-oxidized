# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-03-09

### Added
- Dashboard widget: Oxidized Backup Status showing backup freshness summary
  - Configurable staleness thresholds (default: 24h stale, 7d critical)
  - Color-coded badges: recent (green), stale (yellow), critical (red), failed (dark), never (gray)
  - HTMX async loading for non-blocking dashboard page loads
  - Configurable cache timeout
  - Link to Oxidized UI

## [0.1.0] - 2026-02-03

### Added
- Initial release
- Device tab view
- Virtual Machine tab view
- Settings page
- Caching support
