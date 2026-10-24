# Editable academic CV

`cv-data.json` contains the CV content and public paper references. `build_cv.py` creates the two-page PDF with ReportLab 4.x.

From the repository root, run:

```sh
python cv/build_cv.py
```

This updates `CV.pdf`. The generator embeds Times New Roman from macOS when available, with ReportLab's bundled Vera fonts as a fallback. To write a separate PDF, use `--output /absolute/path/to/CV.pdf`.

Equal-contribution marks on the AIED 2025 paper are supported by the publisher's statement: https://link.springer.com/chapter/10.1007/978-3-031-98462-4_34.

The three arXiv papers remain explicitly labeled as preprints. Earlier publications and research experience come from the original CV and personal homepage.
