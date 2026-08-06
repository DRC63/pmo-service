"""P3MAI-branded architecture diagrams for the PMO Service docs."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(ASSETS, exist_ok=True)
NAVY = "#0B2545"; NAVYL = "#1B3F6E"; GOLD = "#C9A227"; GOLDD = "#A8841C"
GREEN = "#2E7D5B"; RED = "#C0392B"; PURPLE = "#8E5BE0"; GREY = "#5B6675"
BG = "#F6F7F9"; STEEL = "#3D5A80"


def box(ax, x, y, w, h, text, fill=NAVY, fg="white", fs=11, bold=True, edge=None, sub=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                linewidth=1.4, edgecolor=edge or fill, facecolor=fill, zorder=2))
    ax.text(x + w / 2, y + h / 2 + (0.12 if sub else 0), text, ha="center", va="center",
            color=fg, fontsize=fs, fontweight="bold" if bold else "normal", zorder=3)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.22, sub, ha="center", va="center", color=fg, fontsize=fs - 2.5, zorder=3)


def arrow(ax, x1, y1, x2, y2, color=GREY, text=None, style="-|>", lw=1.6):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                                 color=color, linewidth=lw, zorder=1))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.14, text, ha="center", va="bottom",
                color=color, fontsize=8.5, fontstyle="italic")


def fig():
    f, ax = plt.subplots(figsize=(11, 6.6), dpi=150)
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    f.patch.set_facecolor("white")
    return f, ax


def save(f, name):
    f.savefig(os.path.join(ASSETS, name), bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(f); print("wrote", name)


# 1. Deployment
f, ax = fig()
ax.text(6, 7.6, "PMO Service — Deployment Architecture", ha="center", fontsize=15, fontweight="bold", color=NAVY)
box(ax, 0.4, 4.2, 2.2, 1.1, "User", fill="white", fg=NAVY, edge=NAVY, sub="web browser")
ax.add_patch(FancyBboxPatch((4.1, 2.2), 6.4, 3.6, boxstyle="round,pad=0.02,rounding_size=0.1",
             linewidth=1.6, edgecolor=NAVY, facecolor=BG, zorder=1))
ax.text(7.3, 5.5, "Render — Docker Web Service  (single origin)", ha="center", fontsize=11, fontweight="bold", color=NAVY)
box(ax, 4.5, 4.35, 2.7, 0.95, "uvicorn + FastAPI", fill=NAVY, sub="/api/* routes")
box(ax, 7.5, 4.35, 2.7, 0.95, "React SPA", fill=STEEL, sub="served from frontend/dist")
box(ax, 4.5, 2.55, 2.7, 0.95, "SQLite", fill=GREEN, sub="pmo.db (auto-seeded)")
box(ax, 7.5, 2.55, 2.7, 0.95, "Seed data", fill=GOLDD, sub="sample portfolio")
arrow(ax, 7.5, 3.02, 7.2, 3.02, color=NAVY, style="-|>")
ax.text(7.35, 3.5, "seeds DB\non boot", ha="center", va="bottom", color=GREY, fontsize=7.5, fontstyle="italic")
arrow(ax, 2.6, 4.75, 4.1, 4.75, color=NAVYL, text="HTTPS", style="-|>")
ax.text(3.35, 4.35, "apps.p3mai.com/pmo", ha="center", fontsize=8, color=GOLDD, fontstyle="italic")
box(ax, 4.1, 0.5, 6.4, 0.95, "GitHub  ·  DRC63/pmo-service", fill="white", fg=NAVY, edge=GREY)
arrow(ax, 7.3, 1.45, 7.3, 2.2, color=GOLD, text="push → deploy (Docker build)", style="-|>")
ax.text(6, 0.05, "No authentication in v1 — deployed openly (deliberate). Render disk is ephemeral; DB re-seeds on boot.",
        ha="center", fontsize=8.5, color=GREY, fontstyle="italic")
save(f, "pmo_deployment.png")


# 2. Data model
f, ax = fig()
ax.text(6, 7.6, "PMO Service — Data Model", ha="center", fontsize=15, fontweight="bold", color=NAVY)
box(ax, 4.4, 5.7, 3.2, 1.2, "Project", fill=NAVY, sub="code · category · RAG · budget")
box(ax, 0.4, 2.7, 3.0, 1.1, "Milestone", fill=STEEL, sub="due · status")
box(ax, 8.6, 2.7, 3.0, 1.1, "Risk", fill=RED, sub="likelihood × impact = score")
box(ax, 4.4, 2.7, 3.2, 1.1, "Allocation", fill=GOLDD, sub="allocation %")
box(ax, 4.4, 0.4, 3.2, 1.1, "Resource", fill=GREEN, sub="role · capacity (hrs/wk)")
arrow(ax, 4.9, 5.7, 2.4, 3.8, color=GREY, text="1→many", style="-|>")
arrow(ax, 7.1, 5.7, 9.4, 3.8, color=GREY, text="1→many", style="-|>")
arrow(ax, 6.0, 5.7, 6.0, 3.8, color=GREY, text="1→many", style="-|>")
arrow(ax, 6.0, 1.5, 6.0, 2.7, color=GREY, text="1→many", style="-|>")
ax.text(6, 0.05, "Allocation is the join of Resource ↔ Project. Dashboard & Reports aggregate across all of these.",
        ha="center", fontsize=8.5, color=GREY, fontstyle="italic")
save(f, "pmo_datamodel.png")


# 3. Screens map
f, ax = fig()
ax.text(6, 7.6, "PMO Service — Screens", ha="center", fontsize=15, fontweight="bold", color=NAVY)
box(ax, 0.4, 0.8, 1.9, 6.2, "Sidebar", fill=NAVY, fs=10, sub="navigation")
screens = [("Dashboard", "RAG summary · upcoming\nmilestones · top risks", GREEN),
           ("Projects", "portfolio list →\nproject detail", STEEL),
           ("Resources", "people · allocations", GOLDD),
           ("Risks", "register · scores", RED),
           ("Reports", "portfolio & project\nreports", PURPLE)]
for i, (t, sub, c) in enumerate(screens):
    x = 2.7 + (i % 3) * 3.0
    y = 4.2 - (i // 3) * 2.6
    box(ax, x, y, 2.7, 1.9, t, fill=c, fs=12, sub=sub)
ax.text(6, 0.15, "Plus a Settings page. All screens share a sidebar + top bar layout.",
        ha="center", fontsize=8.5, color=GREY, fontstyle="italic")
save(f, "pmo_screens.png")
print("done")
