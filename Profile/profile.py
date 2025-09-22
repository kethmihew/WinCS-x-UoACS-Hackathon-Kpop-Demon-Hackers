# Profile/profile.py
"""
Profile module
--------------
Lightweight profile system that plugs into the existing Tk app without changing
Spencer's Work Timer class.

What you get:
- UserProfile dataclass persisted to ~/.touch_grass_profile.json
- ProfileWindow: a separate 500x600 window to edit name/focus/break and view XP
- attach_profile(...): adds a small top-right dark panel in Work Timer
  (matches Profile window theme) and shows "Lvl N"
- open_profile_window(...): opens/raises a single Profile window near the panel
- grant_xp(...), level_info(...): tiny XP/level helpers
- Plays small GIFs for some actions (see assets below)
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, List
import json, os
import tkinter as tk
from tkinter import messagebox, filedialog

# ----------------------------- theme -----------------------------------------
PROFILE_BG      = "#2E3440"   # dark background (Profile window + panel)
PROFILE_FG      = "#E5E9F0"   # primary text
PROFILE_SUB     = "#A3B1C6"   # secondary text
PROFILE_ACCENT  = "#A3BE8C"   # XP fill
PROFILE_CANVAS  = "#3B4252"   # canvas/track fill

PANEL_BG        = PROFILE_BG
PANEL_FG        = PROFILE_FG
PANEL_SUB       = PROFILE_SUB
PANEL_STROKE    = PROFILE_SUB

# ----------------------------- assets ----------------------------------------
# These paths are relative to the repository root: repo/pictures/*.gif
HERE       = os.path.dirname(__file__)
ASSETS_DIR = os.path.abspath(os.path.join(HERE, "..", "pictures"))

DRINK_GIF = os.path.join(ASSETS_DIR, "drink_water.gif")
TEETH_GIF = os.path.join(ASSETS_DIR, "brush_teeth.gif")
WALK_GIF  = os.path.join(ASSETS_DIR, "walking.gif")

# ----------------------------- storage ---------------------------------------

PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".touch_grass_profile.json")


@dataclass
class UserProfile:
    """Single source of truth for profile data."""
    display_name: str = "Player 1"
    focus_min:   int  = 50
    break_min:   int  = 10
    xp:          int  = 0
    avatar_path: Optional[str] = None  # file path to chosen image (optional)


def load_profile() -> UserProfile:
    """Load profile from disk, or create/reset to defaults if missing/corrupted."""
    if not os.path.exists(PROFILE_PATH):
        p = UserProfile()
        save_profile(p)
        return p
    try:
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return UserProfile(**data)  # default any missing keys
    except Exception:
        p = UserProfile()
        save_profile(p)
        return p


def save_profile(p: UserProfile) -> None:
    """Write the current profile to disk (human-readable JSON)."""
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(p), f, indent=2)

# ---------------------------- XP helpers -------------------------------------

BASE_LEVEL_XP = 500  # level N requires N * BASE_LEVEL_XP

# Button actions used in the UI
ACTION_XP = {
    "focus_session": 100,
    "brush_teeth":   60,
    "water_break":   20,
    "outdoor_break": 60,
}

ACTION_MULT = {
    "brush_teeth":   2.0,
    "outdoor_break": 2.0,
}


def level_info(xp: int) -> tuple[int, int, int, int]:
    """
    Translate total XP into: (level, into_level, needed_this_level, remaining_to_next).
    Example: if BASE_LEVEL_XP=500 and xp=750 -> level 2, into=250, need=1000, remaining=750.
    """
    lvl = 1
    rem = xp
    need = BASE_LEVEL_XP * lvl
    while rem >= need:
        rem -= need
        lvl += 1
        need = BASE_LEVEL_XP * lvl
    return lvl, rem, need, (need - rem)


def grant_xp(prof: UserProfile, action: str, units: int = 1) -> int:
    """Increment XP for an action and persist it. Returns XP gained for UI feedback."""
    base = ACTION_XP.get(action, 0)
    mult = ACTION_MULT.get(action, 1.0)
    gained = int(base * mult * max(1, units))
    prof.xp += gained
    save_profile(prof)
    return gained

# --------------- integrate with the timer without editing it -----------------

def _apply_to_app(app, prof: UserProfile) -> bool:
    """
    Push minutes into the running timer instance without modifying its class.
    Returns True if values were applied and a refresh was attempted.
    """
    changed = False
    if hasattr(app, "work_time"):
        app.work_time = prof.focus_min * 60
        changed = True
    if hasattr(app, "break_time"):
        app.break_time = prof.break_min * 60
        changed = True

    if changed:
        # Trigger a redraw/refresh using whatever hooks exist.
        if hasattr(app, "reset_timer"):
            try:
                app.reset_timer()
            except Exception:
                pass
        elif hasattr(app, "_update_timer_label"):
            try:
                if hasattr(app, "time_remaining"):
                    app.time_remaining = app.work_time
                app._update_timer_label()
            except Exception:
                pass
    return changed

# ------------------------------ Profile window -------------------------------

class ProfileWindow(tk.Toplevel):
    """
    500x600 window styled like Main, dedicated to the user's profile & XP.
    Launch with: ProfileWindow(root, app, prof, on_change=callback)
    """
    def __init__(
        self,
        master: tk.Tk,
        app,
        prof: UserProfile,
        on_change=None,
        title_prefix: str = "Profile"
    ):
        super().__init__(master)
        self.app = app
        self.prof = prof
        self.on_change = on_change  # callback to update Main’s small panel
        self.title(f"{title_prefix} — {prof.display_name}")
        self.geometry("500x600")
        self.configure(bg=PROFILE_BG)
        self.resizable(False, False)
        self.transient(master)  # sit on top of Main

        # animation state for action GIFs
        self._anim_after_id: Optional[str] = None
        self._anim_frames: Optional[List[tk.PhotoImage]] = None
        self._anim_index: int = 0
        self._anim_cycles_left: int = 0

        # Header
        tk.Label(self, text="Profile", font=("Arial", 20, "bold"),
                 fg=PROFILE_FG, bg=PROFILE_BG).pack(pady=12)

        # Avatar area
        self.avatar_img = None  # keep a reference so Tk doesn't GC the image
        self.avatar_canvas = tk.Canvas(self, width=150, height=150,
                                       bg=PROFILE_CANVAS, highlightthickness=0, bd=0)
        self.avatar_canvas.pack(pady=6)
        tk.Button(self, text="Choose Picture…", command=self._choose_avatar)\
            .pack(pady=(0, 8))

        # Editable basic settings
        frm = tk.Frame(self, bg=PROFILE_BG); frm.pack(pady=8)

        tk.Label(frm, text="Name:",  fg=PROFILE_FG, bg=PROFILE_BG, font=("Arial", 12))\
            .grid(row=0, column=0, sticky="e", padx=8, pady=4)
        tk.Label(frm, text="Focus:", fg=PROFILE_FG, bg=PROFILE_BG, font=("Arial", 12))\
            .grid(row=1, column=0, sticky="e", padx=8, pady=4)
        tk.Label(frm, text="Break:", fg=PROFILE_FG, bg=PROFILE_BG, font=("Arial", 12))\
            .grid(row=2, column=0, sticky="e", padx=8, pady=4)

        self.name_var  = tk.StringVar(value=prof.display_name)
        self.focus_var = tk.IntVar(value=prof.focus_min)
        self.break_var = tk.IntVar(value=prof.break_min)

        tk.Entry(frm, textvariable=self.name_var, width=20)\
            .grid(row=0, column=1, sticky="w")
        tk.Spinbox(frm, from_=5, to=180, increment=5, textvariable=self.focus_var, width=6)\
            .grid(row=1, column=1, sticky="w")
        tk.Spinbox(frm, from_=3, to=60,  increment=1, textvariable=self.break_var, width=6)\
            .grid(row=2, column=1, sticky="w")

        tk.Button(frm, text="Save", command=self._save_basic)\
            .grid(row=0, column=2, rowspan=3, padx=10)

        # Level + XP bar
        self.level_lbl = tk.Label(self, fg=PROFILE_FG, bg=PROFILE_BG, font=("Arial", 14, "bold"))
        self.level_lbl.pack(pady=(12, 4))

        self.xp_bar = tk.Canvas(self, width=340, height=18, bg=PROFILE_CANVAS, highlightthickness=0)
        self.xp_bar.pack()

        self.xp_detail = tk.Label(self, fg=PROFILE_SUB, bg=PROFILE_BG, font=("Arial", 10))
        self.xp_detail.pack(pady=4)

        # XP action buttons (small, gamified nudges)
        act = tk.Frame(self, bg=PROFILE_BG); act.pack(pady=10)
        self._mk_xp_btn(act, "Log Focus Session", lambda: self._earn("focus_session"))\
            .grid(row=0, column=0, padx=6, pady=4)
        self._mk_xp_btn(act, "Brush Teeth (x2)",  lambda: self._earn("brush_teeth"))\
            .grid(row=0, column=1, padx=6, pady=4)
        self._mk_xp_btn(act, "Drink Water",       lambda: self._earn("water_break"))\
            .grid(row=1, column=0, padx=6, pady=4)
        self._mk_xp_btn(act, "Outdoor Break (x2)",lambda: self._earn("outdoor_break"))\
            .grid(row=1, column=1, padx=6, pady=4)

        tk.Button(self, text="Close", command=self.destroy).pack(pady=8)

        # Initial paint
        self._draw_avatar()
        self._refresh_xp()

        # ESC key closes the window (nice UX)
        self.bind("<Escape>", lambda e: self.destroy())

    # ---- internal helpers (UI) ----

    def _mk_xp_btn(self, parent, text, cmd) -> tk.Button:
        """Create a consistently styled XP button."""
        return tk.Button(
            parent, text=text, command=cmd, font=("Arial", 12),
            bg="#81A1C1", fg=PROFILE_BG,
            activebackground="#81A1C1", activeforeground=PROFILE_BG,
            relief="ridge", bd=3
        )

    # ---------- avatar + simple GIF playback ----------

    def _choose_avatar(self) -> None:
        """Prompt the user to pick an image file; redraw + notify Main."""
        path = filedialog.askopenfilename(
            title="Choose a picture",
            initialdir=ASSETS_DIR,
            filetypes=[
                ("Common image types", "*.png;*.gif;*.ppm;*.pgm;*.jpg;*.jpeg"),
                ("GIF", "*.gif"),
                ("PNG", "*.png"),
            ],
        )
        if not path:
            return
        self.prof.avatar_path = path
        save_profile(self.prof)
        self._draw_avatar()
        if self.on_change:
            self.on_change(self.prof)

    def _draw_avatar(self) -> None:
        """Render the chosen image into a 150x150 box; no external deps needed."""
        c = self.avatar_canvas
        c.delete("all")
        self._stop_anim()

        if self.prof.avatar_path and os.path.exists(self.prof.avatar_path):
            try:
                self.avatar_img = tk.PhotoImage(file=self.prof.avatar_path)
                w, h = self.avatar_img.width(), self.avatar_img.height()
                fx = max(1, w // 150)
                fy = max(1, h // 150)
                if fx > 1 or fy > 1:
                    self.avatar_img = self.avatar_img.subsample(fx, fy)
                c.create_image(75, 75, image=self.avatar_img)
                return
            except Exception:
                pass

        # Placeholder avatar (simple, consistent with theme)
        c.create_oval(45, 25, 105, 85, fill=PROFILE_FG, outline="#D8DEE9", width=2)   # head
        c.create_oval(60, 45, 68, 53, fill=PROFILE_BG)  # eyes
        c.create_oval(82, 45, 90, 53, fill=PROFILE_BG)
        c.create_line(75, 85, 75, 120, fill=PROFILE_FG, width=6)                      # neck
        c.create_line(55, 120, 95, 120, fill=PROFILE_FG, width=12)                    # shoulders

    def _load_gif_frames(self, path: str, max_side: int = 150) -> Optional[List[tk.PhotoImage]]:
        """Return frames for a GIF (or None). Works without Pillow; Tk handles GIF."""
        if not os.path.exists(path):
            return None
        frames: List[tk.PhotoImage] = []
        ix = 0
        try:
            while True:
                frm = tk.PhotoImage(file=path, format=f"gif -index {ix}")
                w, h = frm.width(), frm.height()
                fx, fy = max(1, w // max_side), max(1, h // max_side)
                if fx > 1 or fy > 1:
                    frm = frm.subsample(fx, fy)
                frames.append(frm)
                ix += 1
        except Exception:
            pass
        return frames or None

    def _play_anim(self, frames: List[tk.PhotoImage], cycles: int = 1, delay_ms: int = 60) -> None:
        """Play frames in the avatar canvas for a few cycles."""
        self._stop_anim()
        self._anim_frames = frames
        self._anim_index = 0
        self._anim_cycles_left = max(1, cycles)

        def _tick():
            if not self._anim_frames:
                return
            frm = self._anim_frames[self._anim_index]
            self.avatar_canvas.delete("all")
            self.avatar_canvas.create_image(75, 75, image=frm)
            self._anim_index += 1
            if self._anim_index >= len(self._anim_frames):
                self._anim_index = 0
                self._anim_cycles_left -= 1
                if self._anim_cycles_left <= 0:
                    self._stop_anim()
                    self._draw_avatar()  # restore still image
                    return
            self._anim_after_id = self.after(delay_ms, _tick)

        _tick()

    def _stop_anim(self) -> None:
        if self._anim_after_id:
            try:
                self.after_cancel(self._anim_after_id)
            except Exception:
                pass
        self._anim_after_id = None
        self._anim_frames = None
        self._anim_index = 0
        self._anim_cycles_left = 0

    # ---------- save + xp + ui refresh ----------

    def _save_basic(self) -> None:
        """Persist name/focus/break changes and push minutes to the running timer."""
        self.prof.display_name = self.name_var.get().strip() or "Player 1"
        self.prof.focus_min   = int(self.focus_var.get())
        self.prof.break_min   = int(self.break_var.get())
        save_profile(self.prof)

        _apply_to_app(self.app, self.prof)
        self.title(f"Profile — {self.prof.display_name}")

        if self.on_change:
            self.on_change(self.prof)

        messagebox.showinfo("Saved", "Profile updated.", parent=self)

    def _earn(self, action: str) -> None:
        """Award XP and, for certain actions, play a short GIF in the avatar box."""
        gained = grant_xp(self.prof, action)
        self._refresh_xp()
        if self.on_change:
            self.on_change(self.prof)

        # Pick a clip for this action (if present)
        clip = None
        if action == "water_break":
            clip = DRINK_GIF
        elif action == "brush_teeth":
            clip = TEETH_GIF
        elif action == "outdoor_break":
            clip = WALK_GIF

        if clip and os.path.exists(clip):
            frames = self._load_gif_frames(clip)
            if frames:
                self._play_anim(frames, cycles=2, delay_ms=65)

        messagebox.showinfo("XP", f"+{gained} XP ({action.replace('_',' ').title()})", parent=self)

    def _refresh_xp(self) -> None:
        """Update the level label + XP bar + detail text."""
        lvl, into, need, left = level_info(self.prof.xp)
        self.level_lbl.config(text=f"Level {lvl}")

        # bar
        self.xp_bar.delete("all")
        w = int(340 * into / max(1, need))
        self.xp_bar.create_rectangle(0, 0, 340, 18, fill=PROFILE_CANVAS, outline="")
        self.xp_bar.create_rectangle(0, 0, w, 18, fill=PROFILE_ACCENT, outline="")

        self.xp_detail.config(text=f"{self.prof.xp} XP  •  {left} XP to next level")

# --------------------- public helpers used by Main ---------------------------

# Keep a single instance of the Profile window
_PROFILE_WIN_REF: ProfileWindow | None = None

def _position_near(widget: tk.Widget, window: tk.Toplevel, pad: tuple[int,int]=(12, 8)) -> None:
    """Position `window` near `widget` (top-right area)."""
    window.update_idletasks()
    try:
        wx = widget.winfo_rootx()
        wy = widget.winfo_rooty()
        ww = widget.winfo_width()
    except Exception:
        # fallback to the root's top-right
        root = window.master
        root.update_idletasks()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        wx, wy, ww = rx + rw, ry, 0

    W = window.winfo_width()
    x = int(wx + ww - W - pad[0])
    y = int(wy + pad[1])
    window.geometry(f"+{max(0,x)}+{max(0,y)}")


def open_profile_window(root: tk.Tk, app, on_change=None, near_widget: tk.Widget | None = None) -> None:
    """Open/raise the profile window (single instance)."""
    global _PROFILE_WIN_REF
    if _PROFILE_WIN_REF and _PROFILE_WIN_REF.winfo_exists():
        _PROFILE_WIN_REF.deiconify()
        _PROFILE_WIN_REF.lift()
        _PROFILE_WIN_REF.focus_force()
    else:
        prof = load_profile()
        _PROFILE_WIN_REF = ProfileWindow(root, app, prof, on_change=on_change)

    if near_widget is not None:
        _position_near(near_widget, _PROFILE_WIN_REF)


def attach_profile(root: tk.Tk, app, title_prefix: str = "Posture Pomodoro Timer") -> UserProfile:
    """
    Integration layer for Work Timer:
    - Loads the profile and sets the Main window title.
    - Places a tiny profile panel in the top-right (avatar + name/mins/level + Edit)
      using the same dark theme as the Profile window.
    - Pushes focus/break minutes into the running timer.
    """
    prof = load_profile()
    root.title(f"{title_prefix} — {prof.display_name}")

    # current level + strings
    lvl, _, _, _ = level_info(prof.xp)
    name_var = tk.StringVar(value=prof.display_name)
    mins_var = tk.StringVar(value=f"{prof.focus_min}/{prof.break_min} min  •  Lvl {lvl}")

    # panel (dark, matches Profile window)
    panel = tk.Frame(root, bg=PANEL_BG, bd=0, highlightthickness=0)
    panel.place(relx=1.0, rely=0.0, anchor="ne", x=-12, y=12)

    # grid: [ avatar ][ text (name + mins) ][ Edit ]
    panel.columnconfigure(0, weight=0)
    panel.columnconfigure(1, weight=1)
    panel.columnconfigure(2, weight=0)

    # avatar thumb (28x28)
    thumb_canvas = tk.Canvas(panel, width=28, height=28, bg=PANEL_BG, highlightthickness=0, bd=0)
    thumb_canvas.grid(row=0, column=0, rowspan=2, padx=(0, 8), pady=(2, 2), sticky="w")
    thumb_img = None  # closure ref

    # labels
    name_lbl = tk.Label(panel, textvariable=name_var, font=("Segoe UI", 10, "bold"),
                        fg=PANEL_FG, bg=PANEL_BG)
    name_lbl.grid(row=0, column=1, sticky="w")

    mins_lbl = tk.Label(panel, textvariable=mins_var, font=("Segoe UI", 9),
                        fg=PANEL_SUB, bg=PANEL_BG)
    mins_lbl.grid(row=1, column=1, sticky="w")

    # Edit button
    edit_btn = tk.Button(
        panel, text="Edit",
        command=lambda: open_profile_window(root, app, on_change=_on_change, near_widget=panel),
        cursor="hand2",
        font=("Segoe UI", 9, "bold"),
        bg=PANEL_BG, fg=PANEL_FG,
        activebackground=PANEL_BG, activeforeground=PANEL_FG,
        bd=0, highlightthickness=0, relief="flat", padx=6, pady=1
    )
    edit_btn.grid(row=0, column=2, rowspan=2, sticky="e")

    def _refresh_thumb(p: UserProfile) -> None:
        nonlocal thumb_img
        thumb_canvas.delete("all")
        if p.avatar_path and os.path.exists(p.avatar_path):
            try:
                img = tk.PhotoImage(file=p.avatar_path)
                w, h = img.width(), img.height()
                fx = max(1, w // 28); fy = max(1, h // 28)
                if fx > 1 or fy > 1:
                    img = img.subsample(fx, fy)
                thumb_img = img
                thumb_canvas.create_image(14, 14, image=thumb_img)
                return
            except Exception:
                pass
        # fallback placeholder
        thumb_canvas.create_oval(4, 4, 24, 24, outline=PANEL_STROKE)

    # initial paint + push minutes into timer
    _refresh_thumb(prof)
    _apply_to_app(app, prof)

    # when Profile window updates data, reflect it here too
    def _on_change(p: UserProfile) -> None:
        lvl_now, _, _, _ = level_info(p.xp)
        name_var.set(p.display_name)
        mins_var.set(f"{p.focus_min}/{p.break_min} min  •  Lvl {lvl_now}")
        root.title(f"{title_prefix} — {p.display_name}")
        _apply_to_app(app, p)
        _refresh_thumb(p)

    # make panel clickable to open Profile
    def _open_from_panel(_evt=None):
        open_profile_window(root, app, on_change=_on_change, near_widget=panel)

    for w in (panel, name_lbl, mins_lbl, thumb_canvas):
        w.bind("<Button-1>", _open_from_panel)
        w.configure(cursor="hand2")

    return prof