# SI26 deck construction plan

The SI26 deck is a native copy of the official SDSC and UC San Diego
presentation template that Cindy Wong shared with instructors on July 16,
2026. The source attachment is `SDSC-UCSanDiego-HSDSC.potx`.

The template defines:

- Teko for headlines.
- Source Sans 3 for body text.
- White and SDSC navy slide families with blue and yellow accents.
- Current San Diego Supercomputer Center and UC San Diego marks.
- A branded photograph on the title slide only.
- Simple, full-width text-first layouts for the remaining slides.
- A gray institutional footer on every content slide.

Narrative text remains native and editable. Content-slide headings are 54
points and body text is 36 points. The deck reserves photography for the
opening. All other slides use generous whitespace so learners can keep the
notebook beside the slide.

## Narrative structure

The 43-slide deck is the session control center:

| Slides | Time | Section | Coordination role |
| --- | --- | --- | --- |
| 1 to 8 | 8:30 to 8:42 | Setup | Goals, participation system, launch, Python environment, import check, workflow |
| 9 to 14 | 8:42 to 9:15 | Numba | Divider, introduction, notebook launch, question pause, exercise, debrief |
| 15 to 20 | 9:15 to 9:40 | Threads and processes | Divider, mental model, notebook launch, question pause, exercise, debrief |
| 21 | 9:40 to 9:50 | Break | Divider |
| 22 to 29 | 9:50 to 10:20 | Dask tasks and chunks | Divider, two introductions, two notebook launches, two exercises, debrief |
| 30 | 10:20 to 10:30 | Cluster setup | Two-terminal cluster instructions |
| 31 to 35 | 10:30 to 11:02 | Multi-node Dask | Divider, role diagram, notebook launch, exercise, cleanup debrief |
| 36 to 38 | 11:02 to 11:20 | Recap | Divider, decision map, take-home files |
| 39 to 43 | Optional | AI workflow | Appendix divider, review loop, page launch, exercise, debrief |

Every section divider states its section number and target clock time. Every
core file has an explicit launch slide that says what to open and where to
stop. Every activity is followed by a debrief before the next section begins.
Every term and action used in the live class is introduced on a slide in plain
language before it appears in a notebook or exercise.

## Template mapping

- Slide 1 uses the official photographic title layout.
- Slides 5, 9, 15, 21, 22, 31, 36, and 39 use the navy divider family.
- Slides 2 to 4 and all introduction, launch, activity, and debrief slides use
  the white text-first family.
- Slide 38 uses the white closing family.
- Slides 8 and 32 use native, editable flow diagrams. Diagram labels are at
  least 24 points and use the template colors.
- No raster media appears after the title slide.

Speaker cues are stored as native speaker notes.
The exported deck must be checked as a complete contact sheet and at full
resolution. The review must confirm:

1. 43 slides in the intended order.
2. 43 populated speaker-note pages.
3. 54-point titles, 36-point body text, and readable diagram labels.
4. No clipped or overlapping text.
5. Exact notebook paths and clock targets.
6. No images after the title slide.
