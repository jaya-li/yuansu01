# 意大利调研 方案一

## 当前文件

- `figma-onboarding-interactive-demo.html`：主工程文件（含所有交互逻辑、样式、组件）
- `download_assets.py`：将 HTML 中远程素材下载到本地并自动改为本地引用

## 本地打开

直接双击或浏览器打开：

- `file:///Users/bytedance/Desktop/意大利调研%20方案一/figma-onboarding-interactive-demo.html`

## 上传 GitHub 并异地完整打开（推荐流程）

1. 进入该目录：
   - `cd "/Users/bytedance/Desktop/意大利调研 方案一"`
2. 先执行素材本地化：
   - `python3 download_assets.py`
3. 脚本会：
   - 创建 `assets/` 目录
   - 下载 HTML 内的 Figma 图片与视频资源
   - 自动把 HTML 中远程 URL 替换为 `./assets/...` 本地路径
4. 将整个 `意大利调研 方案一` 文件夹上传到 GitHub。
5. 在异地拉取后，打开同一个 HTML 即可完整显示。

## 注意

- 如果不执行 `download_assets.py`，页面仍依赖外链素材（例如 Figma MCP 资源），可能在异地出现资源失效。
- 建议把 `assets/` 一并提交到仓库，确保长期可用。
