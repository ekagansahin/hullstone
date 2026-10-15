# Hullstone

**English** | [Türkçe](README.tr.md)

Design low-poly, flat-bottomed stones (faceted convex blocks) in your browser and export them as STL for 3D printing.

The name comes from the **convex hull**: every stone is the hull of a set of points you can generate or edit.

**Try it online:** [ekagansahin.github.io/hullstone](https://ekagansahin.github.io/hullstone/). Nothing to install; it runs entirely in your browser.

![Hullstone app](docs/screenshot.png)

## Features

- **Random shapes** with an exact number of planar faces (4–40).
- **Size limits**: set a min/max size in mm for X, Y and Z. Random shapes always fall inside them.
- **Manual editing** of base and top points in tables. The shape is the convex hull of the points.
- **Limit check**: if an edited shape is out of range, the app says which axis. **Fit to limits** scales only those axes.
- **Live 3D preview** with size, volume, face count and triangle count.
- **STL download** (binary STL, millimetres).
- **4 languages**: English, Türkçe, Deutsch, Français. Switch from the top-right corner.

Shapes are always convex and the base always sits flat on z = 0, so they print without supports.

## Web version

The online version is the same Streamlit app running in the browser with [stlite](https://github.com/whitphx/stlite) (Python compiled to WebAssembly). `index.html` loads `hullstone_app.py` straight from this repository, so the web and local versions are always the same code. The first load takes a few seconds while Python and the packages download; after that the browser caches them.

## Running locally

You need Python 3.10 or newer.

### Windows

1. Download the repository (**Code → Download ZIP**) and extract it.
2. Double-click `run_app.bat`.

On the first run the script creates a virtual environment in `.venv` and installs the packages. This takes a few minutes. If Python is not installed, it installs it with `winget`. Later runs start straight away. The app opens in your browser. Close the console window to stop it.

### macOS / Linux

In a terminal, inside the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run hullstone_app.py
```

After the first setup, you only need `source .venv/bin/activate` and `streamlit run hullstone_app.py`.

## Usage

1. Set the **size limits** (mm) for each axis.
2. Choose the **number of faces** and click **Generate**. Or edit the points in the **Base points** and **Top points** tables and click **Update shape**.
3. Check the preview and the numbers under it. If a warning appears, click **Fit to limits**.
4. Click **Download STL** and slice the file as usual.

Tips:

- Points that end up inside the hull don't change the shape.
- Keep `z = 0` for the base points to get a flat bottom.
- Add `?lang=tr`, `?lang=de` or `?lang=fr` to the URL to open the app in that language.

## How it works

- **Shape**: the mesh is the convex hull of all points (`scipy.spatial.ConvexHull`). Each triangle's normal is flipped outward if needed. Coplanar triangles are counted as one face.
- **Random generation**: the base is a k-sided polygon on an ellipse and the top points lie on an ellipsoid dome. Euler's formula gives the number of top points needed:
  `faces = 2 × top points + k − 1`. A random shear makes the block asymmetric. Attempts are repeated until the face count matches exactly.
- **Size limits**: the shape is scaled separately on each axis to a target size drawn from the limits. This is an affine transform, so planar faces stay planar, the shape stays convex and the face count doesn't change.

## Project structure

```
hullstone_app.py     Streamlit app (UI, geometry, STL export)
i18n.py              UI strings for all languages
assets/icon.png      App icon (favicon)
run_app.bat          One-click launcher for Windows
hullstone_script.py  Minimal script version: edit points in the file, writes an STL
requirements.txt     Python dependencies
LICENSE              MIT license
index.html           Web version for GitHub Pages (stlite)
```

## Adding a language

In `i18n.py`, add the language code and name to `LANGS`, then add a translation for that code to every entry in `STRINGS`. If a translation is missing, the app shows the English text.

## License

[MIT](LICENSE) © 2026 Eyup Kağan Şahin. You can use, modify and share this project freely, including commercially, as long as the license notice is kept.
