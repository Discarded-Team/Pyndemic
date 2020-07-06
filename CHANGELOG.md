# Changelog
All notable changes to this project will be documented in this file.

The format is based on format provided by [Keep a Changelog](https://keepachangelog.com) website.

## [Unreleased]
- Game logic improvements
- Web browser visualization
- Fine colored messages in console version =)
- Refactoring, refactoring...

## [0.2.0] - 2020-07-06
### Added
- Internal API is created for interacting with various frontend versions
- API description is provided to help with programmatic game managing
- Game object serialization is added for transferring game information through the network
- Creation of several configurable game sessions is now supported (useful for a server application)
- Provided ability for manual game settings before start (player names, game difficulty, random state)
- Small improvements in the game logic
### Changed
- Project and code structure is completely redesigned 
- Game messages are not bound to logging anymore and are handled by UI classes

---

## [0.1.0] - 2020-05-01
### Added
- Basic game logic (custom characters, action cards, and hand limit are not included)
- Ability to create console-based game session on a single computer
- Human-readable game logs

