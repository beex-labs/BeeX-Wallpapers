# BeeX-Wallpapers

**Languages:** English | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

The online wallpaper library for **BeeX DeskNest**. All wallpapers are distributed via a GitHub repository + jsDelivr CDN. The app fetches the `index.json` manifest from this repository under **Desktop wallpaper → Library → Online wallpapers**, then displays and downloads the listed items.

> Default repository: `BeeX-Labs/BeeX-Wallpapers` (can be overridden to any `owner/repo` in the app).

---

## Directory layout

```
BeeX-Wallpapers/
├── index.json              ← Wallpaper manifest (the only file the app reads)
├── wallpapers/             ← Video / image wallpaper files
│   ├── aurora-glow.mp4
│   └── ...
├── web/
│   └── scene-star/         ← Web/scene wallpaper folders (upload the whole folder)
│       └── index.html
└── thumbs/                 ← Preview thumbnails (≈320px wide, jpg/png)
    └── ...
```

## The index.json manifest

### Top level

| Field | Description |
|---|---|
| `version` | Manifest version (integer). Bump it for major changes; not strictly validated by the app yet |
| `items` | Array of wallpaper entries, one per wallpaper |

### Entry fields

| Field | Required | Applies to | Description |
|---|---|---|---|
| `id` | ✅ | all | Unique identifier (letters/digits/hyphens). Used for local cache file names; **must not repeat** |
| `name` | ✅ | all | Display name, any language |
| `kind` | ✅ | all | `video` / `image` / `web` |
| `file` | ✅ | video, image | Relative path inside the repo, e.g. `wallpapers/aurora-glow.mp4` |
| `dir` | ✅ | web | Directory of the web wallpaper, e.g. `web/scene-star` |
| `entry` | optional | web | Entry file name, defaults to `index.html` |
| `thumb` | optional | all | Relative path of the preview image, e.g. `thumbs/aurora-glow.jpg` |
| `tags` | optional | all | Tag array, e.g. `["4K", "slow"]` |
| `sizeMB` | optional | all | File size (display only), e.g. `24` |

### Complete example

```json
{
  "version": 1,
  "items": [
    {
      "id": "aurora-glow",
      "name": "Aurora Glow",
      "kind": "video",
      "file": "wallpapers/aurora-glow.mp4",
      "thumb": "thumbs/aurora-glow.jpg",
      "tags": ["4K", "slow", "glow"],
      "sizeMB": 24
    },
    {
      "id": "deep-space",
      "name": "Deep Space Nebula",
      "kind": "image",
      "file": "wallpapers/deep-space.jpg",
      "thumb": "thumbs/deep-space.jpg",
      "sizeMB": 6
    },
    {
      "id": "scene-star",
      "name": "Starry Scene",
      "kind": "web",
      "dir": "web/scene-star",
      "entry": "index.html",
      "thumb": "thumbs/scene-star.jpg"
    }
  ]
}
```

---

## How to update the online library

**Add a wallpaper:**

1. Put the file(s) into the matching folder:
   - Video/image → `wallpapers/` (e.g. `wallpapers/city-rain.webm`)
   - Web scene → create `web/<name>/` and place the entry `index.html` plus resources
   - Preview → `thumbs/` (optional)
2. **Append one entry** to `items` in `index.json` (copy the example format above)
3. `git add` → `git commit` → `git push` (make sure it lands on `main`)
4. In the app, open **Online wallpapers** and hit **Refresh**

**Modify / remove a wallpaper:** edit (or delete) its entry in `index.json` and push. Users who already downloaded it keep the local copy, but it disappears from the list after the next refresh.

**Replace a file (same id, new content):** overwrite the file with the same name and push. Note jsDelivr caching (see Note 6 below).

---

## Notes

1. **The default branch must be `main`**: the app fetches via `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/...`; any other branch → 404.
2. **No spaces or non-ASCII in file names**: CDN URLs handle ASCII paths reliably. Use `aurora-glow.mp4` style (lowercase + hyphens).
3. **File size**: GitHub caps repo files at 100MB. Keep video wallpapers ≤50MB (jsDelivr is unreliable for very large files). H.264 + AAC `.mp4` has the best compatibility.
4. **Web wallpapers must be self-contained**: the `index.html` inside `web/<name>/` must not reference external CDN/remote resources (inline scripts, styles, images, fonts or use relative paths), otherwise it renders blank/broken. BeeX injects the runtime.js SDK for online rendering — the page does not (and should not) include it itself.
5. **A broken manifest takes down the whole library**: `index.json` must be valid JSON (validate it locally, or open `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` in a browser to confirm). On failure the app falls back to the last offline cache.
6. **jsDelivr caching**: the CDN caches for ~24 hours, so fresh pushes may not show immediately. To verify instantly, purge the cache for `index.json` (jsDelivr purge API) and refresh in the app.
7. **Offline fallback**: the app caches every successfully fetched manifest locally; when offline/unreachable it shows the cached list, and already-downloaded wallpapers keep working.
8. **Thumbnails**: use jpg/png ≈320px wide, under ~100KB each, to keep the list fast.
9. **Licensing**: make sure you have the rights to distribute every uploaded wallpaper; consider adding a `LICENSE` file to the repo.

---

## FAQ

**Q: "Online wallpapers" fails to load?**
A: Check the network; verify the repo name (`owner/repo`); confirm the default branch is `main`; open `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` in a browser to see whether it returns JSON.

**Q: A downloaded video won't play?**
A: Use H.264/AAC (mp4) or VP9/Opus (webm). High-bitrate H.265 videos are not supported by WebView2.

**Q: A web wallpaper renders blank?**
A: Check for external dependencies; open `index.html` in a local browser to confirm it runs standalone.
