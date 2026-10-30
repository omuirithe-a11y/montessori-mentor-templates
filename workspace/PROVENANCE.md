# Workspace - where each file came from (30 Oct 2026)

This folder is the exact copy of the working files. A new chat copies it with
`git clone https://github.com/omuirithe-a11y/montessori-mentor-templates` and proves every file with
`cd montessori-mentor-templates/workspace && sha256sum -c FINGERPRINTS.txt` (every line must say OK).
The Project's claude/workspace/ copies can only be read back as text, so they cannot be proved this way.
The templates (Essay, Resources, org-rule) are not copied here: the master copies are at the top of this repository.

## Sources
- 74 files: workspace-74-2026-10-30.zip, made by another chat from its copies (last changed 27 Oct 10:27-10:34);
  every file matched the zip's own fingerprint list.
- tools/format_check.py, live_match.py, strip_compare.py, visual_check.py: from this repository's tools-v5
  (handover-2026-10-29-evening). live_match.py differs from the Project text only at line 8.
- templates/copy-protection.html: typed from the Project; sha256 0d180ad6... is the one strip_compare.py expects.
- faces/yunet.onnx: from Drive (232,589 bytes, sha256 8f2383e4...).
- Changed or new 30 Oct:
  - tools/build_page.py: --shown-width, --no-blur <record>, large copies up to 2900 px (owner 30 Oct "Up to 2900 px - yes").
    The copy before the change matched the Project at 24 places.
  - pages/aun-aprendo.py: new. The 9 image descriptions written 30 Oct were removed (owner 28 Oct: descriptions "are not
    necessary anymore"). Whether the 52 copied from the live page stay is the owner's open question.
  - records/aun-aprendo-no-blur.json: the no-blur record (owner 29 Oct 10:25, agreed 30 Oct 09:24).
  - check-tools-v6-test/strip_compare.py: TEST copy of tools-v5's strip_compare.py, only the template pin changed to the
    30 Oct Essay template (3ebaef3a...). Not an agreed tool.

## Compared with the Project's text (30 Oct)
- tools/pages/frame.html: byte-identical (the Project handed over the file itself).
- tools/drawings.py, tools/menu_sync.py, tools/fetch_drive.py: identical (Project text typed out and compared).
- tools/convert_curriculum.py: identical except two invisible characters (a zero-width space, a no-break space on line
  157) that cannot be seen in the Project text; taken as the local ones.
- Every other file: NOT compared with the Project.
