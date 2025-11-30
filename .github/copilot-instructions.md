# Repository Copilot Instructions

This file provides repository-local guidance for AI coding agents working in `laravel-recipes-2025`.

## WSL Path Guidance
When agents run on a Windows machine using WSL, prefer Linux-style absolute paths inside the WSL environment (for example: `/home/doug/dev/laravel-recipes-2025`). If a Windows-native path is required, use the UNC form `\\wsl.localhost\\Ubuntu\\home\\doug\\dev\\laravel-recipes-2025`. Avoid relative paths in automation and scripts; always use absolute paths appropriate to the execution environment.

## Where to look for global agent guidance
- `AGENTS.md` at repo root — canonical agent instructions
- `docs/plan/SETUP-STATUS.md` — session handoff and environment notes

## Quick actions for agents
- Use Linux-style paths for file reads/writes when running in WSL.
- If a tool requires Windows paths, convert `/home/doug/...` → `\\wsl.localhost\\Ubuntu\\home\\doug\\...`.
# AI Coding Agent Instructions

This file references centralized AI agent instructions to ensure all AI assistants follow the same guidelines.

## For All AI Agents

Please read and follow the instructions in `/AGENTS.md` for comprehensive guidelines on:
- Project architecture and technology stack
- Code organization and standards
- Implementation patterns and best practices
- Testing and quality requirements
- Common development commands
- Documentation references

## Quick Summary

**Key Files**:
- `/AGENTS.md` - Complete AI agent guidelines (centralized)
- `/docs/CONTRIBUTING.md` - Human developer workflow
- `/docs/design/DATA.md` - Data model and entity relationships
- `/docs/design/TECH-STACK.md` - Technology versions and specifications
- `/docs/BUILD_PLAN.md` - Implementation plan with 15 phases

**Technology Stack**:
- Backend: PHP 8.5+, Laravel 12.x, Eloquent ORM
- Frontend: Tailwind CSS 4+, Alpine.js 3.x, Blade templates
- Testing: PHPUnit 10+ or Pest 2.0+
- Build: Vite with npm

**Core Principle**: Follow Laravel 12 conventions, preserve legacy patterns where applicable, and reference `/AGENTS.md` for any guidelines not addressed in project-specific documentation.

---

**Note**: This file is a redirect to centralized instructions. Do not duplicate guidelines here - maintain a single source of truth in `/AGENTS.md`.
