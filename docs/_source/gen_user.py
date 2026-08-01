"""Generate 02_User_Manual.docx for the PMO Service."""
import os
import docstyle as ds

OUT = os.path.join(os.path.dirname(__file__), "..", "02_User_Manual.docx")
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
VER, DATE = "v1.0", "1 August 2026"

doc = ds.new_doc()
ds.footer(doc, "OFFICIAL", VER)
ds.title_page(doc, "DOC-02", "User Manual", "Using the P3MAI PMO Service",
              VER, DATE, "Douglas Colvin, P3MAI", "OFFICIAL")
ds.doc_control(doc, [[VER, "2026-08-01", "Douglas Colvin", "Initial issue"]])
ds.add_toc(doc)

ds.heading(doc, "1.  Welcome", 1)
ds.para(doc, "The **PMO Service** is P3MAI's project-management-office tool. In one place you can track "
        "your **projects**, their **milestones**, the **people** working on them and how they are "
        "**allocated**, the **risks**, and see it all rolled up on a **dashboard** and in **reports**.")
ds.heading(doc, "1.1  Getting in", 2)
ds.para(doc, "Open **app.p3mai.com** in a web browser, or use the **Example** button on the PMO card of "
        "the P3MAI website's Services page. There is no login. Nothing to install.")
ds.callout(doc, "note", "Sample data",
           ["The app comes pre-loaded with a realistic sample portfolio so you can explore every screen "
            "immediately. You can add, edit and delete freely."])

ds.heading(doc, "2.  The screen at a glance", 1)
ds.figure(doc, os.path.join(ASSETS, "pmo_screens.png"), "Figure 1 — The main screens.")
ds.para(doc, "A **sidebar** on the left switches between screens; the main area shows the selected "
        "screen. A **Back to Website** link returns you to p3mai.com.")

ds.heading(doc, "3.  The Dashboard", 1)
ds.para(doc, "The landing screen gives portfolio health at a glance:")
ds.bullet(doc, "**RAG counts** — how many projects are Green, Amber and Red;")
ds.bullet(doc, "**Upcoming milestones** — the next ones due, with days remaining;")
ds.bullet(doc, "**High-severity risks** — open risks scoring 15 or more;")
ds.bullet(doc, "**Overdue milestones** — a count of anything past its due date.")

ds.heading(doc, "4.  Projects", 1)
ds.para(doc, "The **Projects** screen lists the portfolio; filter it and open any project for detail.")
ds.heading(doc, "4.1  Creating & editing a project", 2)
ds.para(doc, "Use **New project** (or Edit on a row) to set the name, code, category, owner, dates, "
        "budget, spend, RAG status and a description. Save to update the list.")
ds.heading(doc, "4.2  Project detail", 2)
ds.para(doc, "Opening a project shows its **milestones**, **risks** and **allocations** together, plus "
        "budget vs. spend and percent-complete — the single view of one project.")

ds.heading(doc, "5.  Milestones", 1)
ds.para(doc, "Add milestones to a project with a name, due date and status. Statuses are **Not "
        "started**, **In progress**, **Complete** and **Late**; anything past its due date and not "
        "complete is flagged **overdue**.")

ds.heading(doc, "6.  Resources & allocations", 1)
ds.para(doc, "The **Resources** screen holds people — their role, email and weekly capacity. An "
        "**allocation** assigns a share (%) of a person to a project. Where someone's allocations across "
        "projects add up beyond their capacity, the over-allocation is shown so you can rebalance.")

ds.heading(doc, "7.  Risks", 1)
ds.para(doc, "The **Risks** screen is the register. Each risk has a **likelihood** and **impact** (each "
        "1–5); the app multiplies them into a **score** (1–25) and shows a coloured badge. Set a "
        "**status** (Open / Mitigating / Closed), an owner and a mitigation plan.")
ds.callout(doc, "tip", "What counts as 'high severity'?",
           ["A score of **15 or more** is high severity and appears on the dashboard. Reduce likelihood "
            "or impact (through mitigation) to bring the score down."])

ds.heading(doc, "8.  Reports", 1)
ds.para(doc, "The **Reports** screen produces a **portfolio report** — every project with its "
        "percent-complete, open-risk count, top risk score and budget vs. spend — and a **per-project "
        "report** for a single drill-down.")

ds.heading(doc, "9.  Settings", 1)
ds.para(doc, "The **Settings** screen holds application settings.")

ds.heading(doc, "10.  Reading the colours", 1)
ds.table(doc, ["Indicator", "Meaning"], [
    ["Green / Amber / Red badge", "Project RAG health — on track / at risk / in trouble"],
    ["Risk-score badge", "likelihood × impact (1–25); the higher and redder, the more severe"],
    ["Overdue flag", "A milestone past its due date and not complete"],
], col_widths=[4.5, 11.0])

ds.heading(doc, "11.  Tips & FAQ", 1)
ds.table(doc, ["Question", "Answer"], [
    ["Is there a login?", "No — v1 is open and single-user. Don't put sensitive data in it yet."],
    ["Can I get back to the website?", "Yes — the 'Back to Website' link in the sidebar."],
    ["How is a risk score worked out?", "Likelihood × impact; 15+ is high severity."],
    ["Why is a person shown over-allocated?", "Their allocations across projects exceed their weekly capacity — rebalance."],
    ["Where do the sample projects come from?", "The app seeds a sample portfolio on first run; edit or delete freely."],
], col_widths=[5.2, 10.3])

ds.heading(doc, "12.  Glossary", 1)
ds.table(doc, ["Term", "Meaning"], [
    ["Portfolio", "The whole set of projects."],
    ["RAG", "Red / Amber / Green health status."],
    ["Milestone", "A dated checkpoint within a project."],
    ["Allocation", "The % of a resource assigned to a project."],
    ["Risk score", "likelihood × impact (1–25)."],
], col_widths=[3.5, 12.0])

doc.save(OUT)
print("wrote", os.path.basename(OUT), os.path.getsize(OUT), "bytes")
