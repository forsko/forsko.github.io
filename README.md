# 个人网站

## 本地查看

只需要 Python 3，无需安装依赖。

```powershell
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

在浏览器打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)，也可以直接双击 `dist/index.html`。所有页面均为静态 HTML，无需 JavaScript。

## GitHub Pages 部署

已配置 `.github/workflows/pages.yml`。启用 GitHub Actions 作为部署来源后，每次推送到 `main` 分支都会自动构建并部署。

1. 在 GitHub 创建仓库。使用 `你的用户名.github.io` 作为仓库名可以部署到根域名。
2. 将项目文件提交并推送到仓库的 `main` 分支。
3. 在 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
4. 在 **Actions** 中查看 **Deploy personal homepage** 的运行结果。需要手动部署时，点击 **Run workflow**。
5. 部署完成后，在 **Settings → Pages** 或工作流运行结果中查看访问地址。

站内链接使用相对路径，支持部署到根域名或 `/仓库名/` 子路径。

当前站点 [forsko.github.io](https://forsko.github.io/)。
