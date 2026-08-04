# BeeX-Wallpapers

**語言：** [English](README.md) | [简体中文](README.zh-CN.md) | 繁體中文

**BeeX DeskNest** 的線上壁紙庫：所有壁紙透過 GitHub 倉庫 + jsDelivr CDN 分發，程式在「桌面壁紙 → 壁紙庫 → 線上壁紙」中拉取本倉庫的 `index.json` 清單展示並下載。

> 預設倉庫：`BeeX-Labs/BeeX-Wallpapers`（程式內可自訂為任意 `owner/repo`）

---

## 目錄結構

```
BeeX-Wallpapers/
├── index.json              ← 壁紙清單（程式只認這個檔案）
├── wallpapers/             ← 影片 / 圖片壁紙檔案
│   ├── aurora-glow.mp4
│   └── ...
├── web/
│   └── scene-star/         ← 網頁/場景壁紙目錄（整目錄上傳）
│       └── index.html
└── thumbs/                 ← 預覽縮圖（建議 320px 寬，jpg/png）
    └── ...
```

## index.json 清單格式

### 頂層

| 欄位 | 說明 |
|---|---|
| `version` | 清單版本號（整數）。內容有較大調整時可遞增，程式暫未強制校驗 |
| `items` | 壁紙條目陣列，一個壁紙一項 |

### 條目欄位

| 欄位 | 必填 | 適用類型 | 說明 |
|---|---|---|---|
| `id` | ✅ | 全部 | 唯一識別（英文/數字/連字號），本地快取檔名，**不可重複** |
| `name` | ✅ | 全部 | 顯示名稱，任意語言 |
| `kind` | ✅ | 全部 | `video` / `image` / `web` |
| `file` | ✅ | video、image | 檔案在倉庫內的相對路徑，如 `wallpapers/aurora-glow.mp4` |
| `dir` | ✅ | web | 網頁壁紙所在目錄，如 `web/scene-star` |
| `entry` | 選填 | web | 入口檔名，預設 `index.html` |
| `thumb` | 選填 | 全部 | 預覽圖相對路徑，如 `thumbs/aurora-glow.jpg` |
| `tags` | 選填 | 全部 | 標籤陣列，如 `["4K", "慢速"]` |
| `sizeMB` | 選填 | 全部 | 檔案大小（僅介面顯示用），如 `24` |

### 完整範例

```json
{
  "version": 1,
  "items": [
    {
      "id": "aurora-glow",
      "name": "極光流光",
      "kind": "video",
      "file": "wallpapers/aurora-glow.mp4",
      "thumb": "thumbs/aurora-glow.jpg",
      "tags": ["4K", "慢速", "光效"],
      "sizeMB": 24
    },
    {
      "id": "deep-space",
      "name": "深空星雲",
      "kind": "image",
      "file": "wallpapers/deep-space.jpg",
      "thumb": "thumbs/deep-space.jpg",
      "sizeMB": 6
    },
    {
      "id": "scene-star",
      "name": "星空場景",
      "kind": "web",
      "dir": "web/scene-star",
      "entry": "index.html",
      "thumb": "thumbs/scene-star.jpg"
    }
  ]
}
```

---

## 如何更新線上壁紙庫

**新增一張壁紙：**

1. 把檔案放到對應目錄：
   - 影片/圖片 → `wallpapers/`（如 `wallpapers/city-rain.webm`）
   - 網頁場景 → 新建 `web/場景名/` 目錄並放入入口 `index.html` 及資源
   - 預覽圖 → `thumbs/`（選填）
2. 在 `index.json` 的 `items` 陣列裡**追加一個條目**（照抄上面的範例格式）
3. `git add` → `git commit` → `git push`（推送到 `main` 分支）
4. 程式內點「線上壁紙」→「重新整理」即可看到

**修改/刪除一張壁紙：** 改 `index.json` 對應條目（或刪掉），推送即可。已下載到本地的使用者不會自動刪除舊檔，但下次重新整理後列表不再顯示。

**更換壁紙檔案（內容更新，id 不變）：** 直接覆蓋同名檔案推送。注意 jsDelivr 有快取（見注意事項第 6 條）。

---

## 注意事項

1. **預設分支必須是 `main`**：程式透過 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/...` 拉取清單與檔案，分支不對會 404。
2. **檔名不要用空格和中文**：CDN URL 對非 ASCII 路徑相容性差，統一用 `aurora-glow.mp4` 風格（小寫 + 連字號）。
3. **單檔體積**：倉庫內檔案 GitHub 限制 100MB；建議影片壁紙 ≤50MB（jsDelivr 對超大檔案傳輸不穩定）。影片用 H.264 + AAC 的 `.mp4` 相容性最好。
4. **網頁壁紙必須自包含**：`web/xxx/` 目錄內的 `index.html` 不要引用外部 CDN/遠端資源（腳本、樣式、圖片、字型一律內嵌或用相對路徑），否則載入會花屏或空白。線上直渲時 BeeX 會注入 runtime.js SDK，頁面無需（也不應）自行引入。
5. **清單語法錯誤會讓整庫不可用**：`index.json` 必須是合法 JSON（建議先本地用編輯器校驗，或訪問 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` 確認能正常回傳 JSON）。格式錯誤時程式會回退到上一次的離線快取。
6. **jsDelivr 快取**：CDN 有約 24 小時快取，剛推送的變動可能不會立刻生效；急著驗證可訪問 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` 強制重新整理快取（jsDelivr 的 purge 介面）後再在程式裡重新整理。
7. **離線兜底**：程式每次成功拉取清單會快取到本地；斷網/倉庫不可用時顯示上次的快取清單，下載過的壁紙照常可用。
8. **預覽圖建議**：`thumbs/` 下用 jpg 或 png，寬度 320px 左右即可，體積控制在 100KB 內，加快列表載入。
9. **授權合規**：上傳壁紙請確認版權；倉庫建議附帶 `LICENSE` 宣告散佈條款。

---

## 常見問題

**Q：程式裡點「線上壁紙」顯示載入失敗？**
A：檢查網路；確認倉庫名拼寫正確（`owner/repo`）；確認預設分支是 `main`；用瀏覽器打開 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` 看是否回傳 JSON。

**Q：影片下載後無法播放？**
A：確認影片編碼為 H.264/AAC（mp4）或 VP9/Opus（webm），部分高碼率 H.265 影片 WebView2 不支援。

**Q：網頁壁紙顯示空白？**
A：檢查頁面是否依賴了外部資源；在本地用瀏覽器打開 `index.html` 確認能獨立執行。
