# PMO Service — Documentation Set

Formal documentation for the **P3MAI PMO Service** (projects, milestones,
resources, allocations, risks and reporting). Organised like the *Microsoft
Ecosystem – PMO Project*: numbered documents, each Word document paired with a
PowerPoint summary, plus a house style and generated diagrams.

## Documents

| ID | Document | Word | PowerPoint summary |
|----|----------|------|--------------------|
| DOC-01 | **Architecture & Design** — stack, data model, backend/front-end, deployment | [01_Architecture_and_Design.docx](01_Architecture_and_Design.docx) | [01_…_Summary.pptx](01_Architecture_and_Design_Summary.pptx) |
| DOC-02 | **User Manual** — dashboard, projects, milestones, resources, risks, reports | [02_User_Manual.docx](02_User_Manual.docx) | [02_…_Summary.pptx](02_User_Manual_Summary.pptx) |
| DOC-03 | **Operation Manual** — configuration, data, deployment, monitoring, runbooks | [03_Operation_Manual.docx](03_Operation_Manual.docx) | [03_…_Summary.pptx](03_Operation_Manual_Summary.pptx) |

All three are **v1.1, 6 August 2026** (v1.0 was 1 August; v1.1 reflects the apps.p3mai.com/pmo front-door move, APP_BASE, the legacy 301, CI + Dependabot and optional Sentry). DOC-03 is **OFFICIAL-SENSITIVE**; the others are **OFFICIAL**.

## Regenerating

The Office files are generated from Python (`docs/_source/`, using `python-docx`,
`python-pptx`, `matplotlib`, `Pillow`):

```bash
python gen_diagrams.py   # PNG diagrams → ../assets
python gen_arch.py       # 01
python gen_user.py       # 02
python gen_ops.py        # 03
python gen_decks.py      # the three *_Summary.pptx
```

`docstyle.py` / `deckstyle.py` are the shared P3MAI-branded helpers (identical to
those used for the Method Map docs).

> The Word documents contain an auto Table of Contents field — click it and press **F9** on first open to populate it.
