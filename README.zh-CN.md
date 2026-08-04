# BeeX-Wallpapers

**语言：** [English](README.md) | 简体中文 | [繁體中文](README.zh-TW.md)

**BeeX DeskNest** 的在线壁纸库：所有壁纸通过 GitHub 仓库 + jsDelivr CDN 分发，程序在「桌面壁纸 → 壁纸库 → 在线壁纸」中拉取本仓库的 `index.json` 清单展示并下载。

> 默认仓库：`BeeX-Labs/BeeX-Wallpapers`（程序内可自定义为任意 `owner/repo`）

---

## 目录结构

```
BeeX-Wallpapers/
├── index.json              ← 壁纸清单（程序只认这个文件）
├── wallpapers/             ← 视频 / 图片壁纸文件
│   ├── aurora-glow.mp4
│   └── ...
├── web/
│   └── scene-star/         ← 网页/场景壁纸目录（整目录上传）
│       └── index.html
└── thumbs/                 ← 预览缩略图（建议 320px 宽，jpg/png）
    └── ...
```

## index.json 清单格式

### 顶层

| 字段 | 说明 |
|---|---|
| `version` | 清单版本号（整数）。内容有较大调整时可递增，程序暂未强制校验 |
| `items` | 壁纸条目数组，一个壁纸一项 |

### 条目字段

| 字段 | 必填 | 适用类型 | 说明 |
|---|---|---|---|
| `id` | ✅ | 全部 | 唯一标识（英文/数字/连字符），本地缓存文件名，**不可重复** |
| `name` | ✅ | 全部 | 显示名称，任意语言 |
| `kind` | ✅ | 全部 | `video` / `image` / `web` |
| `file` | ✅ | video、image | 文件在仓库内的相对路径，如 `wallpapers/aurora-glow.mp4` |
| `dir` | ✅ | web | 网页壁纸所在目录，如 `web/scene-star` |
| `entry` | 选填 | web | 入口文件名，默认 `index.html` |
| `thumb` | 选填 | 全部 | 预览图相对路径，如 `thumbs/aurora-glow.jpg` |
| `tags` | 选填 | 全部 | 标签数组，如 `["4K", "慢速"]` |
| `sizeMB` | 选填 | 全部 | 文件大小（仅界面显示用），如 `24` |

### 完整示例

```json
{
  "version": 1,
  "items": [
    {
      "id": "aurora-glow",
      "name": "极光流光",
      "kind": "video",
      "file": "wallpapers/aurora-glow.mp4",
      "thumb": "thumbs/aurora-glow.jpg",
      "tags": ["4K", "慢速", "光效"],
      "sizeMB": 24
    },
    {
      "id": "deep-space",
      "name": "深空星云",
      "kind": "image",
      "file": "wallpapers/deep-space.jpg",
      "thumb": "thumbs/deep-space.jpg",
      "sizeMB": 6
    },
    {
      "id": "scene-star",
      "name": "星空场景",
      "kind": "web",
      "dir": "web/scene-star",
      "entry": "index.html",
      "thumb": "thumbs/scene-star.jpg"
    }
  ]
}
```

---

## 如何更新在线壁纸库

**新增一张壁纸：**

1. 把文件放到对应目录：
   - 视频/图片 → `wallpapers/`（如 `wallpapers/city-rain.webm`）
   - 网页场景 → 新建 `web/场景名/` 目录并放入入口 `index.html` 及资源
   - 预览图 → `thumbs/`（可选）
2. 在 `index.json` 的 `items` 数组里**追加一个条目**（照抄上面的示例格式）
3. `git add` → `git commit` → `git push`（推送到 `main` 分支）
4. 程序内点「在线壁纸」→「刷新」即可看到

**修改/删除一张壁纸：** 改 `index.json` 对应条目（或删掉），推送即可。已下载到本地的用户不会自动删除旧文件，但下次刷新后列表不再显示。

**更换壁纸文件（内容更新，id 不变）：** 直接覆盖同名文件推送。注意 jsDelivr 有缓存（见注意事项第 6 条）。

---

## 注意事项

1. **默认分支必须是 `main`**：程序通过 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/...` 拉取清单与文件，分支不对会 404。
2. **文件名不要用空格和中文**：CDN URL 对非 ASCII 路径兼容性差，统一用 `aurora-glow.mp4` 风格（小写 + 连字符）。
3. **单文件体积**：仓库内文件 GitHub 限制 100MB；推荐视频壁纸 ≤50MB（jsDelivr 对超大文件传输不稳定）。视频用 H.264 + AAC 的 `.mp4` 兼容性最好。
4. **网页壁纸必须自包含**：`web/xxx/` 目录内的 `index.html` 不要引用外部 CDN/远程资源（脚本、样式、图片、字体一律内嵌或用相对路径），否则加载会花屏或空白。在线直渲时 BeeX 会注入 runtime.js SDK，页面无需（也不应）自行引入。
5. **清单语法错误会让整库不可用**：`index.json` 必须是合法 JSON（推荐先本地用编辑器校验，或访问 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` 确认能正常返回 JSON）。格式错误时程序会回退到上一次的离线缓存。
6. **jsDelivr 缓存**：CDN 有约 24 小时缓存，刚推送的改动可能不会立刻生效；着急验证可访问 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` 强制刷新缓存（jsDelivr 的 purge 接口）后再在程序里刷新。
7. **离线兜底**：程序每次成功拉取清单会缓存到本地；断网/仓库不可用时显示上次的缓存清单，下载过的壁纸照常可用。
8. **预览图建议**：`thumbs/` 下用 jpg 或 png，宽度 320px 左右即可，体积控制在 100KB 内，加快列表加载。
9. **许可合规**：上传壁纸请确认版权；仓库建议附带 `LICENSE` 声明分发条款。

---

## 常见问题

**Q：程序里点「在线壁纸」显示加载失败？**
A：检查网络；确认仓库名拼写正确（`owner/repo`）；确认默认分支是 `main`；用浏览器打开 `https://cdn.jsdelivr.net/gh/{owner}/{repo}@main/index.json` 看是否返回 JSON。

**Q：视频下载后无法播放？**
A：确认视频编码为 H.264/AAC（mp4）或 VP9/Opus（webm），部分高码率 H.265 视频 WebView2 不支持。

**Q：网页壁纸显示空白？**
A：检查页面是否依赖了外部资源；在本地用浏览器打开 `index.html` 确认能独立运行。
