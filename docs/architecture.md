# 项目架构

## 设计目标

项目同时承载 OD1、OD2、OD3、OD4。课程级别和 Unit 编号必须共同构成唯一命名空间，避免不同级别的 Unit 1、Unit 12 相互覆盖。

```text
OD/
├─ public/                       # 唯一部署目录
│  ├─ assets/                   # 全站共享图片、样式等
│  ├─ levels/                   # OD1–OD4 课程入口
│  └─ units/
│     ├─ od1/unit-12/           # 当前 OD1 正式页面
│     ├─ od2/unit-01..unit-18/  # 当前 OD2 正式页面
│     ├─ od3/                   # 后续课程空间
│     └─ od4/                   # 后续课程空间
├─ content/                     # 不参与部署的教材原稿和提取中间产物
│  ├─ od1/
│  ├─ od2/unit-01..unit-18/
│  └─ shared/
├─ templates/                   # 新 Unit 的受控模板
├─ tools/                       # 脚手架与自动校验
└─ docs/                        # 架构和协作说明
```

## 正式路径

- 页面：`public/units/od{1-4}/unit-{01-18}/index.html`
- Unit 资源：`public/units/od{level}/unit-{NN}/assets/images/`
- 教材源文件：`content/od{level}/unit-{NN}/`
- 全站共享资源：`public/assets/`

新代码、课程入口和二维码应只引用正式路径。`public/units/<数字>/` 仅用于旧链接跳转，不得继续放课程实现或资源。

## 新增 Unit

1. 运行 `python tools/create_unit.py od1 1 "My Unit Title"`。
2. 把词汇图和思维导图等运行时图片放入新页面的 `assets/images/`。
3. 把 Word、PDF、提取 Markdown 和未采用的素材放入对应的 `content/` 目录。
4. 完成标准 7 段内容，并在 `public/levels/od-level-{level}.html` 加入正式链接。
5. 运行 `python tools/validate_units.py`，通过后再提交。

脚手架默认拒绝覆盖已存在的 Unit，避免误删现有课堂内容。

## 页面契约

每个正式 Unit 必须：

- 使用 `viewport-fit=cover`，支持 iPad safe area。
- 依次保留 `Key Vocabulary`、`Knowledge List Guide`、`Mind Map Workshop`、`Grammar and Expression`、`Challenge Practice`、`Writing Task`、`Wrap-Up` 七段。
- 不包含 `<canvas>` 或 `<textarea>`；写作任务引导学生在纸上完成。
- 不引用 `.docx`、提取目录、`source-pages` 或教材整页截图。
- 所有相对图片、脚本、样式和站内链接必须存在。

## 部署与兼容

静态服务器的发布根目录保持为 `public/`，无需构建。旧 OD2 地址（例如 `/units/3/3_en_ipad.html`）保留跳转页；新入口统一指向 `/units/od2/unit-03/`。兼容页只用于过渡，可在确认外部链接全部更新后按版本计划移除。
