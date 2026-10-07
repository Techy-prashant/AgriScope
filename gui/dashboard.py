"""
AutoEverGreen GUI — Home Panel
Clean, elegant control center.
"""
from __future__ import annotations
import threading
import tkinter as tk
import customtkinter as ctk
from typing import Optional, Callable
from .theme import *
from .components import (
    Card, Divider, PrimaryButton, SecondaryButton, ConnectionDot, ExecutionPanel, SectionLabel
)

class DashboardPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, service, on_run_complete: Optional[Callable] = None, **kw):
        super().__init__(parent, fg_color=BG_BASE, corner_radius=0, **kw)
        self._svc = service
        self._on_run_complete = on_run_complete
        self._executing = False
        self._build()
        self.refresh()

    def _build(self):
        # ── Header ──────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=40, pady=(40, 20))

        title_col = ctk.CTkFrame(hdr, fg_color="transparent")
        title_col.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_col, text="AutoEverGreen",
            font=(FONT_FAMILY, 28, "bold"), text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_col, text="Automate your GitHub publishing workflow.",
            font=FONT_BODY, text_color=TEXT_MUTED, anchor="w"
        ).pack(anchor="w")
        
        self._conn_dot = ConnectionDot(hdr)
        self._conn_dot.pack(side="right", anchor="ne", pady=(10, 0))

        Divider(self).pack(fill="x", padx=40, pady=10)

        # ── Configuration Card ────────────────────────────────────────
        config_card = Card(self)
        config_card.pack(fill="x", padx=40, pady=20)
        
        inner = ctk.CTkFrame(config_card, fg_color="transparent")
        inner.pack(fill="both", padx=20, pady=20)

        # Repository URL
        SectionLabel(inner, text="GitHub Repository").pack(anchor="w", pady=(0, 4))
        
        self._repo_var = tk.StringVar()
        self._repo_entry = ctk.CTkEntry(
            inner, textvariable=self._repo_var,
            font=FONT_BODY, height=36, text_color=TEXT_PRIMARY,
            fg_color=BG_BASE, border_color=BORDER
        )
        self._repo_entry.pack(fill="x", pady=(0, 20))

        # Commits per session
        SectionLabel(inner, text="Commits per session").pack(anchor="w", pady=(0, 4))
        
        spin_frame = ctk.CTkFrame(inner, fg_color="transparent")
        spin_frame.pack(anchor="w")
        
        self._commits_var = tk.StringVar(value="1")
        
        btn_minus = SecondaryButton(
            spin_frame, text="−", width=36,
            command=lambda: self._adj_commits(-1)
        )
        btn_minus.pack(side="left")
        
        self._commits_entry = ctk.CTkEntry(
            spin_frame, textvariable=self._commits_var,
            font=FONT_BODY, height=32, width=60, justify="center",
            text_color=TEXT_PRIMARY, fg_color=BG_BASE, border_color=BORDER
        )
        self._commits_entry.pack(side="left", padx=8)
        
        btn_plus = SecondaryButton(
            spin_frame, text="+", width=36,
            command=lambda: self._adj_commits(1)
        )
        btn_plus.pack(side="left")

        # Save Config Button
        save_btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        save_btn_frame.pack(fill="x", pady=(20, 0))
        
        self._save_cfg_btn = SecondaryButton(
            save_btn_frame, text="Save Settings",
            command=self._save_config
        )
        self._save_cfg_btn.pack(side="left")
        
        self._cfg_status = ctk.CTkLabel(
            save_btn_frame, text="", font=FONT_SMALL, text_color=STATUS_SUCCESS
        )
        self._cfg_status.pack(side="left", padx=12)

        Divider(self).pack(fill="x", padx=40, pady=10)

        # ── Status Area ─────────────────────────────────────────────────
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(fill="x", padx=40, pady=20)
        
        self._status_lbl = ctk.CTkLabel(
            status_frame, text="● Ready", font=FONT_BODY, text_color=STATUS_SUCCESS, anchor="w"
        )
        self._status_lbl.pack(anchor="w", pady=(0, 10))
        
        # Next job
        self._nj_lbl = ctk.CTkLabel(
            status_frame, text="Next job: —", font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w"
        )
        self._nj_lbl.pack(anchor="w", pady=(0, 5))
        
        # Progress
        self._progress_lbl = ctk.CTkLabel(
            status_frame, text="Progress: — / — completed", font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w"
        )
        self._progress_lbl.pack(anchor="w")

        # ── Queue Overview ─────────────────────────────────────────────
        queue_card = Card(self)
        queue_card.pack(fill="x", padx=40, pady=(0, 20))
        
        inner_queue = ctk.CTkFrame(queue_card, fg_color="transparent")
        inner_queue.pack(fill="both", padx=20, pady=20)
        
        SectionLabel(inner_queue, text="Job Queue").pack(anchor="w", pady=(0, 10))
        
        self._queue_text = ctk.CTkTextbox(
            inner_queue, font=FONT_MONO, height=180, text_color=TEXT_PRIMARY,
            fg_color=BG_BASE, border_width=1, border_color=BORDER, wrap="none"
        )
        self._queue_text.pack(fill="x", expand=True)
        self._queue_text.configure(state="disabled")

        # ── Run Now button ───────────────────────────────────────────
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=40, pady=(0, 20))

        self._run_btn = PrimaryButton(
            btn_row, text="RUN NOW",
            command=self._on_run_now
        )
        self._run_btn.pack(side="left", ipadx=20)

    def _adj_commits(self, delta: int):
        try:
            val = int(self._commits_var.get())
        except ValueError:
            val = 1
        val += delta
        if val < 1:
            val = 1
        self._commits_var.set(str(val))

    def _save_config(self):
        try:
            max_commits = int(self._commits_var.get())
            repo_url = self._repo_var.get().strip()
            self._svc.save_home_settings(repo_url, max_commits)
            self._cfg_status.configure(text="✓ Saved", text_color=STATUS_SUCCESS)
            self.after(3000, lambda: self._cfg_status.configure(text=""))
            self.refresh()
        except ValueError as e:
            self._cfg_status.configure(text=f"✗ {e}", text_color=STATUS_FAILED)
        except Exception as e:
            self._cfg_status.configure(text=f"✗ Error saving: {e}", text_color=STATUS_FAILED)

    def refresh(self):
        self._svc.reload()
        data = self._svc.get_dashboard_data()
        if not data:
            self._status_lbl.configure(text=f"✗ Config error: {self._svc.load_error}", text_color=STATUS_FAILED)
            self._run_btn.configure(state="disabled")
            return

        # Update input fields
        self._repo_var.set(data.repo_url)
        self._commits_var.set(str(data.max_commits_per_run))

        # Update Status
        if data.dry_run:
            self._status_lbl.configure(text="● Ready (DRY RUN)", text_color=STATUS_PENDING)
        else:
            self._status_lbl.configure(text="● Ready", text_color=STATUS_SUCCESS)
            
        nj = data.next_job
        if nj:
            self._nj_lbl.configure(text=f"Next job: {nj.job_id} • {nj.file_path}")
        else:
            self._nj_lbl.configure(text="Next job: None (all work complete)")
            
        self._progress_lbl.configure(text=f"Progress: {data.completed_jobs} / {data.total_jobs} completed")

        # Update Queue
        self._queue_text.configure(state="normal")
        self._queue_text.delete("1.0", "end")
        jobs = self._svc.get_job_views()
        lines = []
        for j in jobs:
            if j.status == "success": mark = "✓"
            elif j.status == "pending": mark = "○"
            elif j.status == "error": mark = "✗"
            elif j.status == "skipped": mark = "⏭"
            else: mark = "−"
            lines.append(f"{mark} [{j.job_id}] {j.file_path} - {j.status.upper()}")
        self._queue_text.insert("end", "\n".join(lines))
        
        # Scroll to the first pending job if any
        first_pending = next((i for i, j in enumerate(jobs) if j.status == "pending"), 0)
        if jobs:
            frac = max(0.0, first_pending / len(jobs))
            self._queue_text.yview_moveto(frac)
            
        self._queue_text.configure(state="disabled")

        # Connection (async)
        self._conn_dot.set_checking()
        threading.Thread(target=self._check_connection, daemon=True).start()

        # Run button state
        if not self._executing:
            has_work = data.pending_jobs > 0
            self._run_btn.configure(state="normal" if has_work else "disabled")

    def _check_connection(self):
        ok = self._svc.check_connection()
        self._conn_dot.after(0, lambda: self._conn_dot.set_connected(ok))

    # ── RUN NOW ───────────────────────────────────────────────────────
    def _on_run_now(self):
        if self._executing:
            return
        self._executing = True
        self._run_btn.configure(state="disabled", text="Running...")
        self._status_lbl.configure(text="● Running...", text_color=STATUS_PENDING)

        panel = ExecutionPanel(self.winfo_toplevel())

        def progress(msg):
            panel.after(0, lambda m=msg: panel.append(m))

        def complete(success, summary):
            panel.after(0, lambda: panel.finish(success, summary))
            self.after(0, self._on_execution_done)

        self._svc.run_once(on_progress=progress, on_complete=complete)

    def _on_execution_done(self):
        self._executing = False
        self._run_btn.configure(text="RUN NOW")
        self.refresh()
        if self._on_run_complete:
            self._on_run_complete()
