# 张骏的个人网站

## 本地查看

只需要 Python 3，无需安装依赖。

```powershell
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

浏览器打开 http://127.0.0.1:8000 。也可以直接双击 `dist/index.html`，所有页面均为静态 HTML，不依赖 JavaScript。

## 修改内容

中文资料存放在 `content/profile.json`，英文资料在 `content/profile.en.json`，修改后重新运行 `python scripts/build.py`。两个文件中对应的教育、研究、项目、动态等条目应同步更新。

网站默认入口 `dist/index.html` 为英文版，`dist/index-zh.html` 为中文版。每个页面右上角都有语言切换链接，切换后保持在同一栏目，导航也保留所选语言。切换不需要 JavaScript，本地双击 HTML 和 GitHub Pages 均支持。

- `name`、`english_name`、`headline`、`email`：基本资料。
- `about`、`interests`、`education`：简介、兴趣、教育背景。
- `news`、`research`、`awards` 对应动态、论文和奖项。`journal_rank` 是直接显示的期刊等级文字。`projects` 保留项目资料，供日后恢复项目页使用。
- `social_links`：目前留空。添加格式：`{"label": "GitHub", "url": "https://github.com/你的用户名"}`。
- 每项研究中的 `links` 可存放论文与代码地址，格式同上。
- `portrait` 为主页照片，按原图比例显示。`school_logo` 取自[厦门大学学校标识页](https://www.xmu.edu.cn/sdgl/xxbs.htm)。`education.logo` 使用[青岛大学国际教育学院官方页眉](https://istudy.qdu.edu.cn/themes/4/images/logo_new.png)中的深蓝色独立校徽。[青岛大学校徽说明](https://www.qdu.edu.cn/info/1007/1101.htm)
- `source_note`：资料版本说明；更新资料后可相应修改。

页面样式在 `assets/style.css`，页面结构与生成逻辑在 `scripts/build.py`。`dist/` 是生成结果，请修改源文件后构建，避免直接修改生成页面。

## 资料来源与当前进展

基本资料结合历史简历、本人在本次对话中的更新，以及相关本地论文与研究对话整理。

- 2026 年 9 月起在厦门大学信息学院攻读通信工程硕士。就读时间存放在 `school_period`。
- 青岛大学软件工程经历保留历史简历列出的 2022.09—2026.06 和成绩、奖学金信息。
- 高光谱分类论文已投稿 Pattern Recognition（PR），正在返修。题名及作者顺序按本人确认更新。
- TGRS 波段选择工作已正式发表，题名与作者信息依据青岛大学导师页面和作者代码仓库核实。论文页链接 DOI `10.1109/TGRS.2026.3676136`。
- ACM-TURC 2026 会议论文的题名和页码依据 [Crossref 的出版记录](https://api.crossref.org/works/10.1145/3833142.3833193)核对。末位署名及通信作者标记按本人提供的 `L. Tian†` 展示。
- VPPO 已投稿《自动化学报》，题名与研究简介依据本地 `Acta.tex` 及相关研究对话整理，署名按本人确认更新。
- CCPC 全国邀请赛为 2024 年 5 月，睿抗和计算机设计大赛为 2025 年 8 月，日期来自本地简历。CCPC 按本人确认写作铜奖。研究生数学建模国二为 2026 年 9 月。
- 仅展示用于联系的邮箱；未添加手机号，也未将包含更多个人信息的原始简历 PDF 打包到网站。
- 后续可补充个人 GitHub / Scholar 和最新版简历。

## GitHub Pages 部署

已配置 `.github/workflows/pages.yml`，推送到自己的仓库后自动构建并部署。

1. 在 GitHub 创建你自己的仓库。根域名主页推荐仓库名 `你的用户名.github.io`，其他仓库名也支持。
2. 将本项目文件提交并推送到仓库的 `main` 分支。
3. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
4. 在 **Actions** 中查看 `Deploy personal homepage` 的运行结果；必要时点击 **Run workflow**。
5. 部署完成后，Pages 设置和 Actions 部署结果会显示实际访问地址。

所有内部链接均为相对路径，因此兼容根域名主页和 `/仓库名/` 子路径。

此站点的 GitHub Pages 地址为 [forsko.github.io](https://forsko.github.io/)。
