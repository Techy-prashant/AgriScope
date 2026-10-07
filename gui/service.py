"""
AutoEverGreen GUI — Application Service Layer

Wraps the existing engine (ConfigManager, StateTracker, executor,
startup, logger) and exposes a clean API to the GUI layer.
No Git logic lives here — it delegates entirely to the existing modules.
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Dict, Any

# ── existing engine imports ──────────────────────────────────────────
import sys, os
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import ConfigManager, AppConfig, CommitConfig
from state import StateTracker
from paths import get_app_root, resolve_path
from validator import ConfigValidator


# ──────────────────────────────────────────────────────────────────────
# DATA MODELS (GUI-facing views on existing data)
# ──────────────────────────────────────────────────────────────────────

@dataclass
class JobView:
    index: int
    job_id: str
    phase: str
    enabled: bool
    operation: str
    file_path: str
    source_path: Optional[str]
    message_template: str
    # resolved from state
    status: str        # "pending" | "success" | "error" | "skipped" | "disabled"
    commit_sha: Optional[str] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None


@dataclass
class DashboardData:
    repo_name: str
    repo_url: str
    branch: str
    total_jobs: int
    completed_jobs: int
    pending_jobs: int
    failed_jobs: int
    skipped_jobs: int
    disabled_jobs: int
    max_commits_per_run: int
    dry_run: bool
    last_commit_sha: Optional[str]
    last_commit_message: Optional[str]
    last_timestamp: Optional[str]
    next_job: Optional[JobView]
    config_path: str
    state_path: str
    connection_verified: bool = False


# ──────────────────────────────────────────────────────────────────────
# SERVICE
# ──────────────────────────────────────────────────────────────────────

class AppService:
    """
    Single source of truth for the GUI.
    Wraps ConfigManager + StateTracker.
    Delegates execution to the existing AutoEverGreenExecutor.
    """

    APP_VERSION = "2.0.0"

    def __init__(self, config_path: Optional[str] = None):
        self._app_root = get_app_root()
        if config_path:
            self._config_path = resolve_path(config_path)
        else:
            self._config_path = resolve_path("config/publish_config.json")

        self._state_path  = self._app_root / "state.json"
        self._log_dir     = self._app_root / "logs"

        self.config_manager: Optional[ConfigManager] = None
        self.state_tracker:  Optional[StateTracker]  = None
        self._load_error: Optional[str] = None

        self._lock = threading.Lock()
        self._reload()

    # ── LOAD / RELOAD ──────────────────────────────────────────────────

    def _reload(self):
        """Load or re-load config and state from disk."""
        try:
            self.config_manager = ConfigManager(str(self._config_path))
            self.config_manager.load_config()
            self._load_error = None
        except Exception as e:
            self.config_manager = None
            self._load_error = str(e)

        try:
            self.state_tracker = StateTracker(self._state_path)
        except Exception as e:
            self.state_tracker = None

    def reload(self):
        with self._lock:
            self._reload()

    # ── PROPERTIES ────────────────────────────────────────────────────

    @property
    def config_path(self) -> Path:
        return self._config_path

    @property
    def state_path(self) -> Path:
        return self._state_path

    @property
    def log_dir(self) -> Path:
        return self._log_dir

    @property
    def app_root(self) -> Path:
        return self._app_root

    @property
    def is_config_loaded(self) -> bool:
        return self.config_manager is not None and self.config_manager.config is not None

    @property
    def load_error(self) -> Optional[str]:
        return self._load_error

    @property
    def config(self) -> Optional[AppConfig]:
        if self.config_manager:
            return self.config_manager.config
        return None

    # ── JOB VIEWS ──────────────────────────────────────────────────────

    def get_job_views(self) -> List[JobView]:
        if not self.is_config_loaded:
            return []

        repo = self.config.repositories[0]
        batch = self._current_batch()
        job_state_map: Dict[int, Any] = {}
        if batch:
            for js in batch.jobs:
                if js.repository == repo.name and js.branch == repo.branch:
                    job_state_map[js.job_index] = js

        views = []
        for idx, c in enumerate(repo.commits):
            js = job_state_map.get(idx)
            if not c.enabled:
                status = "disabled"
                sha = None
                ts = None
                err = None
            elif js:
                status = js.status
                sha = js.commit_sha
                ts = js.timestamp
                err = js.error
            else:
                status = "pending"
                sha = None
                ts = None
                err = None

            views.append(JobView(
                index=idx,
                job_id=c.id or f"JOB-{idx+1:03d}",
                phase=c.phase or "—",
                enabled=c.enabled,
                operation=c.operation,
                file_path=c.file_path,
                source_path=c.source_path,
                message_template=c.message_template,
                status=status,
                commit_sha=sha,
                timestamp=ts,
                error=err,
            ))
        return views

    def _current_batch(self):
        if not self.state_tracker or not self.state_tracker.current_batch_id:
            return None
        return self.state_tracker.batch_states.get(self.state_tracker.current_batch_id)

    # ── DASHBOARD DATA ─────────────────────────────────────────────────

    def get_dashboard_data(self) -> Optional[DashboardData]:
        if not self.is_config_loaded:
            return None

        repo   = self.config.repositories[0]
        jobs   = self.get_job_views()
        total  = len(jobs)
        comp   = sum(1 for j in jobs if j.status == "success")
        fail   = sum(1 for j in jobs if j.status == "error")
        skip   = sum(1 for j in jobs if j.status == "skipped")
        dis    = sum(1 for j in jobs if j.status == "disabled")
        pend   = total - comp - fail - skip - dis

        # Most recent successful commit
        batch = self._current_batch()
        last_sha = None
        last_msg = None
        last_ts  = None
        if batch:
            successes = [js for js in batch.jobs if js.status == "success" and js.repository == repo.name]
            if successes:
                latest = max(successes, key=lambda j: j.timestamp or "")
                last_sha = latest.commit_sha
                last_ts  = latest.timestamp
                # find message from config
                try:
                    c = repo.commits[latest.job_index]
                    last_msg = c.message_template
                except (IndexError, AttributeError):
                    pass

        # Next pending job
        next_job = next((j for j in jobs if j.status == "pending"), None)

        return DashboardData(
            repo_name=repo.name,
            repo_url=repo.url,
            branch=repo.branch,
            total_jobs=total,
            completed_jobs=comp,
            pending_jobs=pend,
            failed_jobs=fail,
            skipped_jobs=skip,
            disabled_jobs=dis,
            max_commits_per_run=self.config.settings.max_commits_per_run,
            dry_run=self.config.settings.dry_run,
            last_commit_sha=last_sha,
            last_commit_message=last_msg,
            last_timestamp=last_ts,
            next_job=next_job,
            config_path=str(self._config_path),
            state_path=str(self._state_path),
        )

    # ── HISTORY ────────────────────────────────────────────────────────

    def get_history(self) -> List[Dict]:
        """Return all recorded job states across all batches, newest first."""
        if not self.state_tracker:
            return []

        rows = []
        repo_name = ""
        if self.is_config_loaded:
            repo_name = self.config.repositories[0].name

        for batch_id, batch in self.state_tracker.batch_states.items():
            for js in batch.jobs:
                msg = "—"
                try:
                    if self.is_config_loaded:
                        c = self.config.repositories[0].commits[js.job_index]
                        msg = c.message_template
                except (IndexError, AttributeError):
                    pass
                rows.append({
                    "batch_id":   batch_id[:8],
                    "timestamp":  js.timestamp or "—",
                    "job_index":  js.job_index,
                    "repository": js.repository,
                    "branch":     js.branch,
                    "status":     js.status,
                    "commit_sha": (js.commit_sha or "—")[:10],
                    "message":    msg,
                    "error":      js.error or "",
                })

        rows.sort(key=lambda r: r["timestamp"], reverse=True)
        return rows

    # ── LOG READER ─────────────────────────────────────────────────────

    def read_log_lines(self, max_lines: int = 1000) -> List[str]:
        log_file = self._log_dir / "autoevergreen.log"
        if not log_file.exists():
            return []
        try:
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
            return lines[-max_lines:]
        except Exception:
            return []

    # ── CONFIG SAVE ────────────────────────────────────────────────────

    def save_home_settings(self, repo_url: str, max_commits: int) -> None:
        """Patch repository URL and max_commits in the JSON file without destroying other content."""
        if type(max_commits) is not int or max_commits < 1:
            raise ValueError("'max_commits' must be a positive integer.")
        if not repo_url or "github.com" not in repo_url:
            raise ValueError("Invalid GitHub repository URL.")

        raw = self._read_raw_config()
        
        # Patch repo URL
        if "repositories" in raw and len(raw["repositories"]) > 0:
            raw["repositories"][0]["url"] = repo_url
        
        # Patch max commits
        raw.setdefault("settings", {})
        raw["settings"]["max_commits_per_run"] = max_commits
        
        self._write_raw_config(raw)
        self._reload()

    def save_settings(self, dry_run: bool, log_enabled: bool) -> None:
        """Patch settings in the JSON file without destroying other content."""
        if not isinstance(dry_run, bool):
            raise ValueError("'dry_run' must be boolean.")

        raw = self._read_raw_config()
        raw.setdefault("settings", {})
        raw["settings"]["dry_run"] = dry_run
        
        self._write_raw_config(raw)
        self._reload()

    def _read_raw_config(self) -> Dict:
        with open(self._config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_raw_config(self, data: Dict) -> None:
        import tempfile, os
        parent = self._config_path.parent
        parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=parent, suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, self._config_path)
        except Exception:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise

    # ── VALIDATE CONFIG ────────────────────────────────────────────────

    def validate_config(self) -> Optional[str]:
        """Return error string or None if valid."""
        try:
            raw = self._read_raw_config()
            ConfigValidator.validate_and_parse(raw)
            return None
        except Exception as e:
            return str(e)

    # ── STARTUP ────────────────────────────────────────────────────────

    def get_startup_enabled(self) -> bool:
        try:
            from startup import is_startup_enabled
            return is_startup_enabled()
        except Exception:
            return False

    def set_startup_enabled(self, enabled: bool) -> bool:
        try:
            if enabled:
                from startup import enable_startup
                return enable_startup()
            else:
                from startup import disable_startup
                return disable_startup()
        except Exception:
            return False

    # ── GIT CONNECTION CHECK ───────────────────────────────────────────

    def check_connection(self) -> bool:
        """Quick ls-remote check to see if remote is reachable."""
        if not self.is_config_loaded:
            return False
        try:
            url = self.config.repositories[0].url
            kwargs = {
                "capture_output": True,
                "timeout": 10
            }
            if os.name == 'nt':
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                
            result = subprocess.run(
                ["git", "ls-remote", "--exit-code", url, "HEAD"],
                **kwargs
            )
            return result.returncode == 0
        except Exception:
            return False

    # ── EXECUTION ──────────────────────────────────────────────────────

    def has_pending_work(self) -> bool:
        if not self.is_config_loaded:
            return False
        self._reload()  # pick up any state changes
        repo = self.config.repositories[0]
        st = StateTracker(self._state_path)
        for idx, c in enumerate(repo.commits):
            if c.enabled and not st.is_job_completed(repo.name, repo.branch, idx):
                return True
        return False

    def run_once(
        self,
        on_progress: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[bool, str], None]] = None,
    ) -> None:
        """
        Delegate to the existing AutoEverGreenExecutor in a background thread.
        on_progress(message) called with log-style updates.
        on_complete(success, summary) called when done.
        """
        def _run():
            try:
                from executor import AutoEverGreenExecutor
                from config import ConfigManager as CM

                if on_progress:
                    on_progress("Loading configuration...")

                cm = CM(str(self._config_path))
                cm.load_config()
                dry = cm.config.settings.dry_run

                if on_progress:
                    mode = "DRY RUN" if dry else "LIVE"
                    on_progress(f"Mode: {mode}")
                    on_progress("Verifying repository access...")

                executor = AutoEverGreenExecutor(
                    cm,
                    work_dir=str(self._app_root / "repos"),
                    state_file=str(self._state_path),
                    dry_run=dry,
                )

                if not executor.has_pending_work():
                    if on_progress:
                        on_progress("No pending work — all jobs complete.")
                    if on_complete:
                        on_complete(True, "NO_WORK")
                    return

                result = executor.run()
                self._reload()

                success = all(r.success for r in result.repo_results)
                completed = sum(
                    1 for r in result.repo_results
                    for j in r.jobs if j.success
                )
                summary = f"Completed {completed} job(s)."
                if on_progress:
                    on_progress(f"✓ {summary}")
                if on_complete:
                    on_complete(success, summary)

            except Exception as e:
                if on_progress:
                    on_progress(f"✗ Error: {e}")
                if on_complete:
                    on_complete(False, str(e))

        t = threading.Thread(target=_run, daemon=True)
        t.start()
