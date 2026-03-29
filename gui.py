import tkinter as tk
from indexer import load_indexes
from queryProcessor import process_boolean, process_proximity

# ── Colors ──────────────────────────────────────────────
BG         = "#fdf6f9"   
PANEL      = "#ffffff"
PINK       = "#f4c0d1"   
PINK_DARK  = "#d4537e"   
GREEN      = "#c0dd97"   
GREEN_DARK = "#3b6d11"   
TEXT       = "#2c2c2a"
SUBTEXT    = "#888780"
BORDER     = "#edcfda"
ENTRY_BG   = "#fff0f5"

# ── Load indexes ─────────────────────────────────────────
inv, pos, doc_mapping = load_indexes()
all_docs = set(doc_mapping.keys())


def search(event=None):
    q = entry.get().strip()
    if not q:
        return

    if "/" in q:
        result_ids = process_proximity(q, pos)
    else:
        result_ids = process_boolean(q, inv, all_docs)

    for widget in results_frame.winfo_children():
        widget.destroy()

    if result_ids:
        count_label.config(
            text=f"{len(result_ids)} document(s) found",
            fg=GREEN_DARK
        )
        for i, doc_id in enumerate(sorted(result_ids)):
            row = tk.Frame(results_frame, bg=PANEL, padx=10, pady=6,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{i+1}.", bg=PANEL, fg=PINK_DARK,
                     font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
            tk.Label(row, text=doc_mapping[doc_id], bg=PANEL,
                     fg=TEXT, font=("Segoe UI", 10)).pack(side="left")
    else:
        count_label.config(text="No documents found", fg=PINK_DARK)
        tk.Label(results_frame, text="Try a different query.",
                 bg=BG, fg=SUBTEXT, font=("Segoe UI", 10)).pack(pady=8)


# ── Window ────────────────────────────────────────────────
root = tk.Tk()
root.title("Boolean IR System")
root.geometry("620x560")
root.configure(bg=BG)
root.resizable(True, True)

# ── Title ─────────────────────────────────────────────────
tk.Label(root, text="Boolean IR System", bg=BG, fg=PINK_DARK,
         font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=28, pady=(24, 2))
tk.Label(root, text="Trump Speeches · 56 Documents",
         bg=BG, fg=SUBTEXT, font=("Segoe UI", 9)).pack(anchor="w", padx=28)

tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=28, pady=14)

# ── Search area ───────────────────────────────────────────
search_frame = tk.Frame(root, bg=BG)
search_frame.pack(fill="x", padx=28)

entry = tk.Entry(search_frame, bg=ENTRY_BG, fg=TEXT, font=("Segoe UI", 12),
                 relief="flat", highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=PINK,
                 insertbackground=PINK_DARK)
entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=8)
entry.bind("<Return>", search)

btn = tk.Button(search_frame, text="Search", bg=PINK, fg=PINK_DARK,
                font=("Segoe UI", 10, "bold"), relief="flat",
                bd=0, padx=16, pady=8, cursor="hand2",
                activebackground=GREEN, activeforeground=GREEN_DARK,
                command=search)
btn.pack(side="left", padx=(8, 0))

tk.Label(root, text='e.g.  "america"   |   "trump AND wall"   |   "great OR america"   |   "trump wall / 3"',
         bg=BG, fg=SUBTEXT, font=("Segoe UI", 8)).pack(anchor="w", padx=28, pady=(6, 0))

tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=28, pady=14)

# ── Results header ────────────────────────────────────────
results_header = tk.Frame(root, bg=BG)
results_header.pack(fill="x", padx=28, pady=(0, 8))

tk.Label(results_header, text="Results", bg=BG, fg=SUBTEXT,
         font=("Segoe UI", 9)).pack(side="left")
count_label = tk.Label(results_header, text="", bg=BG,
                       font=("Segoe UI", 9))
count_label.pack(side="right")

# ── Scrollable results ────────────────────────────────────
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y", padx=(0, 8))
canvas.pack(fill="both", expand=True, padx=28, pady=(0, 20))

results_frame = tk.Frame(canvas, bg=BG)
canvas_window = canvas.create_window((0, 0), window=results_frame, anchor="nw")

results_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

root.mainloop()