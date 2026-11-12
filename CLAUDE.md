# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Aksara Nusantara is a PySide6 desktop app for learning and preserving Indonesian traditional scripts. It is built as a script-agnostic **Core Engine** (the "Foundation") plus pluggable **ScriptPacks** (Javanese is the reference pack). Python 3.12+ (the local `.venv` runs 3.14). Docs and research notes mix English and Indonesian.

## Commands

All commands run from the repo root (several paths, e.g. `Path("scriptpacks")`, are cwd-relative).

```bash
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
python main.py                     # run the desktop app

# Main suite: unittest, no pytest config, no __init__.py in test dirs
run_tests.bat                      # runs tests\test_*.py one module at a time; skips manual/smoke tests
python -m unittest tests.test_quiz_generator          # single module (top-level tests/)
python -m unittest tests.test_quiz_generator.TestX.test_y

# Research / transliteration experiment suites (not covered by run_tests.bat)
python -m unittest discover -s tests/research -p "test_*.py"
python -m unittest discover -s tests/transliteration/experiments
python -m unittest tests/research/test_step48_01_result_state_generalization.py   # single file by path
```

`run_tests.bat` deliberately skips `test_audio_*`, `test_engine.py`, `test_flashcard_session.py`, and `test_gtts_provider.py`, which are manual or smoke tests that need network or audio. Many UI tests build a `QApplication`, so they need a display.

No linter or formatter is configured.

## Architecture

Layering is strict. Dependencies point downward only: `ui → application → core`. ScriptPacks are reached only through the core. `docs/architecture/APPLICATION_ARCHITECTURE.md` makes this normative (RFC 2119 "SHALL"): the application/UI layers must not contain writing-system logic or import a specific ScriptPack.

- **`core/`: the Foundation** (frozen as "Foundation v1.0"; do not change its architecture without an explicit decision).
  - `engine.py` `CoreEngine`: discovers packs under `scriptpacks/`, holds the active pack and dataset, notifies listeners, and resolves per-pack data/asset/cache paths.
  - `loader.py` (reads `manifest.json`, imports `entry_point`), `validator.py`, `registry.py`, `scriptpack.py` (`BaseScriptPack` abstract interface), `exceptions.py`.
  - `core/learning/`: the Learning Engine (models, repositories, services, and `storage/` with `JSONAdapter`).
  - `core/audio/`, `core/services/`: TTS providers (gTTS / edge-tts), cache, and player.
  - `core/template/`: the reference skeleton for a new ScriptPack.
- **`scriptpacks/<id>/`**: each pack has `manifest.json` (identifier, `entry_point`, specification version, license) plus `script.py` implementing `BaseScriptPack`, and owns its own characters/fonts/audio/images. Contract: `docs/standards/SCRIPTPACK_INTERFACE_SPECIFICATION.md`.
- **`application/`**: `Application` (in `application.py`) is the composition root. `initialize()` starts the engine, calls `register_assets()` on every pack, wires `AudioService`, `FlashcardSession`, and the JSON-backed learner/learning repositories plus `LearningService`, restores or creates the Active Learner (guest mode / setup dialog), and only then builds `MainWindow`. Services are injected through constructors, not globals. Quiz and flashcard session logic lives in `application/learning/`.
- **`ui/`**: `MainWindow`, `CentralWorkspace`, tabs (home, alphabet, flashcard, quiz, script explorer, transliterasi), and widgets.
- **Persistence**: learner data goes to `ApplicationPaths.learning_data_dir()` (`%LOCALAPPDATA%\AksaraNusantara\learning`, falling back to `~/.local/...`), not to the repo. Audio cache goes in `cache/audio/`.

Key decisions are recorded as ADRs in `docs/decisions/`: deferred ScriptPack activation, learner ownership of learning sessions, learner identity and guest mode.

## Transliteration research (AD-TR-01): current focus

The Transliteration Module is being designed through a long, numbered, architecture-first research process. It is not implemented yet.

- Each step gets a design doc in `docs/development/transliteration/NN. AD-TR-01 — Phase X — Step N — <Title>.md`, which ends with a "Step N Completion Status" block (experiment/test counts, Experimental / Architectural / Documentation status).
- Each step's executable probes live in `tests/research/test_stepNN_MM_<topic>.py`, with earlier ones in `tests/transliteration/experiments/`. They are self-contained `unittest` files: plain dicts or local `Experimental*` dataclasses, no imports from production code, and test methods numbered `test_01_...` under `# NN-M-X` section comments. They probe semantic boundaries (admission, permission, authority, result vs. decision, etc.) across several domains; they are not tests of app behavior.
- Do not promote research concepts into `core/` or `application/` unless a contract step explicitly concludes that.

## Conventions

- Every Python module starts with the standard header (`docs/standards/PYTHON_MODULE_TEMPLATE.md`, AN-STD-002): Module / Module Type / Purpose / Implements / References / `SPDX-License-Identifier: GPL-3.0-or-later`, followed by import sections labelled `Standard Library`, `Third-party Packages`, `Local Project Imports`. Copy the layout from an existing file such as `core/engine.py`.
- Workflow is spec-first (`CONTRIBUTING.md`, `docs/PROJECT_WORKFLOW.md`): architecture and spec docs come before implementation, and documentation updates (`docs/development/PROJECT_LOG.md`, `TRACEABILITY.md`, `CHANGELOG.md`) count as part of the change.
- Commit style: conventional prefixes, e.g. `docs(transliteration): ...`, `research: checkpoint ...`, `chore: ...`.
- The license is GPL-3.0-or-later everywhere, manifests included.

## Aturan Wajib Proyek AksaraNusantara (Strict Rules)
- **Git Branch:** Selalu bekerja secara eksklusif pada branch `claude`. Jangan pernah menyentuh branch `main`.
- **Lisensi Kode & Dokumen:** SELURUH file Python (`.py`) dan dokumen spesifikasi Markdown (`.md`) yang dibuat atau dimodifikasi WAJIB menyertakan header lisensi **GNU General Public License v3 (GPLv3)**. Dilarang keras memasukkan lisensi MIT atau lainnya.
- **Tech Stack:** Python dengan UI PySide6. Pisahkan logika bisnis (`core/`) dari antarmuka pengguna (`ui/`).

