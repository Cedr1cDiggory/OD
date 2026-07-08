# Agents.md

## 项目定位

本项目是面向 iPad/触屏课堂的少儿英语互动课件。页面不应像普通网页或营销页，而应像一张可操作的儿童学习工作纸：明亮、圆润、清楚、可点、可拖，并能自然引导学生完成纸质书写任务。

### 项目目录约定

- 正式 Unit 页面统一放在 `public/units/od{1-4}/unit-{01-18}/index.html`。
- Unit 运行时图片统一放在同级 `assets/images/`；跨 Unit 共享资源放在 `public/assets/`。
- Word、PDF、提取 Markdown、教材整页图和处理中间文件统一放在 `content/od{level}/unit-{NN}/`，不得放进正式页面目录。
- `public/units/<数字>/` 只保留旧链接兼容跳转，不得继续开发课程内容。
- 新建页面使用 `python tools/create_unit.py od1 1 "Unit title"`，完成后运行 `python tools/validate_units.py`。

当前参考页为 `public/units/od1/unit-12/index.html`，其核心气质是：

- 少儿英语教材感：主题直接、句型简单、任务目标明确。
- Duolingo 式互动卡片感：厚边框、圆角、胶囊按钮、即时反馈。
- 手绘思维导图感：插画、彩色分支、柔和纸面、课堂活动氛围。
- iPad 优先：触控区域大，拖拽和点击都可用，避免密集小控件。
- 纸质任务友好：写作区不在网页内手写，改为提示学生在纸上完成后交给老师。

## 审美风格

### 关键词

使用这些词校准视觉判断：

- 明亮
- 圆润
- 童趣
- 清爽
- 高对比
- 轻游戏化
- 课堂活动感
- 手绘插画感

避免这些方向：

- 成人商务后台风
- 复杂渐变科技风
- 暗色沉重风
- 过度装饰的海报风
- 大面积低饱和灰色
- 细线、尖角、小字号的传统表单风

## 色彩规范

页面应使用高饱和但友好的儿童教育色彩。当前基调来自以下颜色：

- 主蓝：`#7bd5df`，用于 hero、总结区、主操作按钮。
- 浅粉：`#f8b7d0`，用于重点词、选中态等局部强调，文字保持白色。
- 奖励绿：`#58CC02`，用于正确反馈和完成感。
- 警示红：`#FF4B4B`，用于错误反馈。
- 活动黄：`#ffce59` 或 `#FFC800`，用于 active 状态、可投放状态。
- 文本深灰：`#4B4B4B`，比纯黑更柔和。
- 边框浅灰：`#E5E5E5`，保持干净和轻量。
- 辅助纸粉：`#f9e0de`，用于图片边框、轻柔分隔。
- 半透明白：`rgba(255,255,255,.5)`，用于 hero 和 Wrap-Up 的主提示胶囊。
- 半透明白边：`rgba(255,255,255,.75)`，用于上述提示胶囊的边框。

设计时优先使用白底和彩色局部强调，不要让整页被单一色相吞没。蓝、浅粉、绿、黄应共同构成活泼感，但每个区块只选择 1 个主要强调色。大面积蓝色区块上的关键提示优先使用半透明白底和白色文字，不使用粉色底。

## 字体与文字

页面字体应保持圆润、饱满、亲切：

- 英文标题优先使用 `Baloo 2`。
- 正文和按钮优先使用 `Nunito`。
- 中文兜底使用 `PingFang SC`、`Microsoft YaHei`。

字号和字重应偏大、偏粗：

- 主标题：粗体，视觉上像儿童教材标题。
- 小节标题：清晰醒目，使用圆润粗体。
- 按钮、标签、chip：使用 `font-weight: 800` 或 `900`。
- 正文：保持 1.6 左右行高，适合学生朗读。

内容写法应直接给任务，不写冗长说明。推荐句式：

- `Goal: ...`
- `Use the picture to ...`
- `Check Answers`
- `Start Over`
- `Words left: ...`

## 布局思路

整体布局采用单列课件流：

1. 顶部语言/入口操作。
2. 大号 hero，说明单元名称和学习目标。
3. 学习地图，概览 Words / Reading / Grammar / Writing。
4. 分段任务，每段一个清晰目标。
5. Wrap-Up 总结区，强化学习成果。
6. 底部导航回到关键任务。

页面最大宽度保持在约 `900px`，居中显示，适合 iPad 竖屏和横屏。不要做复杂多栏页面；只有在词卡、规则卡、总结卡等重复内容中使用 grid。

移动端和窄屏下必须自然退化为单列，不能横向滚动。

## 组件规范

### 卡片

卡片是本项目的基础视觉单位：

- 白底。
- `2px` 实线边框。
- 底边框加厚到 `4px`，形成轻微游戏按钮感。
- 圆角通常为 `16px`，大区块可用 `24px`。
- 内容区留足 padding，避免拥挤。

卡片标题栏可以使用白底或极浅灰底，但不要做复杂阴影。

### 按钮

按钮应像可按下的实体块：

- `2px` 边框，底边 `4px`。
- 圆角 `16px`。
- 点击时底边变薄，并 `translateY(2px)`。
- 主按钮使用蓝或绿，次按钮使用白底灰边。
- 按钮最小高度要适合手指点击，触屏下建议不低于 `48px`。

### Chip / Pill

词汇、短语、状态标签使用胶囊形态：

- 圆角 `999px`。
- 粗体。
- 可拖拽 chip 需要有足够 padding 和最小高度。
- 正确态用绿底，错误态用红底，选中态用浅粉底或浅蓝底。

### Hero 与 Summary

Hero 和 Wrap-Up 是页面情绪锚点：

- 使用大面积明亮蓝色。
- 标题可以带白色或深色投影，制造儿童标题贴纸感。
- 主提示文案使用半透明白色胶囊：`background: rgba(255,255,255,.5)`，`border: 2px solid rgba(255,255,255,.75)`，文字为白色。
- Hero 中的 Unit goal 不使用白色实底框；应去掉框、边和圆角，保留白色文字。
- 不要把 hero 做成营销页的图文分栏。

### 写作任务

写作区应引导学生完成纸质书写：

- 不使用网页内 canvas 手写板。
- 不提供 Undo Stroke / Clear Draft 这类网页书写工具。
- 使用静态提示卡说明：学生在纸上手写段落，完成后提交给老师。
- 页面可保留写作图片、范文、句型框架和提交提示。

### 图片与插画

图片应服务于学习任务：

- 词汇图、思维导图、写作图必须清晰可辨。
- 图片容器保持白底、浅灰边框、轻圆角。
- 手绘插画和教材图片优先，不使用抽象装饰图。
- 不使用纯装饰性的渐变球、背景光斑或无意义图形。

## 交互规范

交互要同时支持鼠标、触屏和键盘：

- 拖拽任务必须提供点击选择再点击投放的替代路径。
- 可交互元素应设置足够大的触控面积。
- 反馈区使用 `aria-live="polite"`。
- 可点击/可投放元素应能通过 `tabindex` 聚焦。
- 状态反馈要即时、明确：剩余数量、完成数量、正确数量。

拖拽练习的推荐状态：

- `over` / `tap-ready`：浅蓝或黄色，表示可以放置。
- `tap-selected`：浅粉或浅蓝，表示已选中。
- `good`：绿色，表示正确。
- `bad`：红色，表示需要修改。

## iPad 与响应式要求

本项目优先面向 iPad：

- 使用 `viewport-fit=cover`。
- 页面 padding 兼容 `safe-area-inset-*`。
- 触屏下加大字体、按钮和拖拽 chip。
- 写作任务以纸质手写为主，网页只提供提示与结构支持。
- 避免 hover-only 交互。

响应式断点可参考：

- `860px`：多列 grid 变为单列或两列。
- `700px`：压缩卡片 padding，增大输入/书写空间。
- `480px`：彻底单列，禁止横向溢出。
- `430px`：进一步缩小标题，确保按钮和句子不挤压。

所有文字必须在容器内完整显示，不能重叠，不能依赖横向滚动。

## 内容结构规范

每个学习段落应包含：

- 一个编号标题，例如 `1 Key Vocabulary`。
- 一个 `Goal:` 目标提示。
- 一个核心活动或解释区。
- 必要时提供检查按钮、重置按钮和结果反馈。

内容难度要符合少儿英语：

- 句子短。
- 指令具体。
- 重复关键句型。
- 先看图和词，再进入语法，再进入写作。

推荐学习路径：

1. 词汇识别。
2. 图片匹配。
3. 知识归类或阅读策略。
4. 思维导图复述。
5. 语法规则。
6. 拖拽句型练习。
7. 写作框架。
8. 纸质手写提交提示。
9. 总结自检。

### 标准 Unit 页面骨架

生成或修复 OD2 Unit 页面时，优先对齐 `public/units/od2/unit-03/index.html`、`public/units/od2/unit-04/index.html`、`public/units/od2/unit-05/index.html` 和 `public/units/od2/unit-12/index.html` 的 7 段式课件结构。除非用户明确要求，否则不要随意增加完整大段模块。

标准标题顺序应为：

1. `1 Key Vocabulary`
2. `2 Knowledge List Guide`
3. `3 Mind Map Workshop`
4. `4 Grammar and Expression`
5. `5 Challenge Practice`
6. `6 Writing Task`
7. `7 Wrap-Up`

顶部学习地图也应对应四类主线：

- `Words`
- `Reading`
- `Grammar`
- `Writing`

如果教材中有 Communicate、Speaking、Listening、Word Study、Project、Wrap Up 等内容，应优先合并进上述主线：

- 制作 OD1 Unit 页面时，知识清单中的 Listening / Speaking 内容不提取、不转写，也不放入 Challenge Practice；Challenge 只使用主词汇、阅读、语法和写作主线内容。

- Communicate / Speaking / Listening：通常作为 `5 Challenge Practice` 或 `4 Grammar and Expression` 的文本卡、句型框架、听说补充，不单独扩成完整大段。
- Word Study：通常并入 `4 Grammar and Expression`。
- Project：通常并入 `6 Writing Task`，并保持纸质完成提示。
- Wrap Up / Big Question：通常并入 `7 Wrap-Up` 的总结卡和自检句，不要再额外新增一个普通 `Wrap Up` 大段。

## OD1 Unit 知识清单到网页的标准 SOP

本 SOP 适用于后续 OD1 Unit 5–10 以及同类知识清单。目标是把 Word 中的教学信息转为与 OD2 一致的 7 段式 iPad 互动课件，同时严格区分原始归档、网页内容和运行时图片。

### 1. 接收与归档输入

每个 Unit 至少需要：

- 一份知识清单 Word：`OD1-UnitX 知识清单.docx`。
- 一张最终 Reading 思维导图；如果暂未提供，可以先保留第 3 段位置，但交付前优先补齐。
- Unit 编号、英文标题和必要的特殊说明。

收到文件后：

1. 建立 `content/od1/unit-{NN}/`。
2. 把 Word 移入该目录，不要长期放在 `tools/`、`public/` 或项目根目录。
3. 把用户提供的原始思维导图保存在该目录，推荐命名为 `mind_map.png`。
4. `public/` 中只放网页真正会加载的运行时资源。

### 2. 原始 Word 提取

使用现有工具提取 Word：

```bash
python tools/extract_docx.py "content/od1/unit-05/OD1-Unit5 知识清单.docx"
```

提取结果保存在 Word 同级的 `*_extracted/` 目录：

- `content.md`：完整原始文字和表格转写。
- `images/`：Word 内嵌图片。

`content.md` 是原始归档，不是可以直接复制进网页的最终稿。自动提取可以保留 Word 中的所有栏目，但制作 OD1 网页时必须再执行一次人工内容筛选。

### 3. 分情况筛选内容

| Word 内容 | 网页处理方式 |
| --- | --- |
| Unit 标题、学习目标 | 提炼为 Hero 标题和一句简短 Unit goal |
| 主词汇、主短语 | 放入 `1 Key Vocabulary`；主短语只在服务主阅读或语法时保留 |
| Reading Skill、文章主旨、情节步骤、重点句型 | 提炼为 `2 Knowledge List Guide` 的 3–4 张短卡 |
| 课文复述、Reading 思维导图 | 放入 `3 Mind Map Workshop` |
| 核心语法规则、肯定/否定/疑问句 | 放入 `4 Grammar and Expression` |
| 主词汇、主阅读或语法可形成的单一练习 | 放入 `5 Challenge Practice` |
| Writing 范文、大小写、标点、句型框架 | 转写到 `6 Writing Task` |
| 本课可达成目标 | 回收到 `7 Wrap-Up` |
| Listening 单词、听力原文、听力题 | OD1 页面完全不提取、不转写、不使用 |
| Speaking 对话、口语补充句型 | OD1 页面完全不提取、不转写、不使用 |

特别注意：

- Challenge 不得从 Listening / Speaking 中取词、取句或改写题目。
- 如果 Writing 示例误用了 Listening / Speaking 中的人物或宠物，必须改回主阅读、主语法或真实 Writing 栏内容。
- Word 中的“课文复述”图片可能只是旧版思维导图。用户提供了新版 `mind_map.png` 时，以新版为准。
- 自动提取稿里保留 Listening / Speaking 不算网页内容错误，但正式 HTML 和运行时资源中不得出现这些内容。

### 4. 判断 Word 内嵌图片是否可用

查看 `*_extracted/images/` 中每张图，并按用途分类：

- 真正的词汇识图、Reading 思维导图：可以作为候选学习资源。
- 主要由文字、表格、横线或题目组成的截图：不得直接嵌入，应转写为 HTML 卡片、规则、范文或句型框架。
- Writing 横线区：不嵌入网页，不制作网页手写区；只保留范文、结构提示和纸质提交说明。
- 旧思维导图：保留在 `content/` 归档，不覆盖用户更新的最终思维导图。

使用图片前必须检查清晰度、文字正确性、方向、裁切和内容是否与当前 Unit 一致。

### 5. 词汇缺图时的处理

如果 Word 没有可用的主词汇图：

1. 在 `content/od1/unit-{NN}/image-prompts.md` 保存最终生成提示词。
2. 提示词使用 `scientific-educational` 场景，明确图片用于少儿英语 iPad 词汇工作纸。
3. 优先生成一张横向 3×3 或结构清晰的词汇图；每格只表达一个概念。
4. 图片使用明亮手绘教材风、粗轮廓、白底、充足留白。
5. 默认不在生成图中加入单词、字母、数字或标签，词汇文字由 HTML 提供。
6. 生成图必须无水印、无品牌、无无关装饰、无裁切主体。
7. 最终图片复制到 `public/units/od1/unit-{NN}/assets/images/vocabulary.png` 或 `vocabulary.webp`。
8. 生成后目视检查每一格是否与目标词一致；错误或歧义明显时重新生成。

如果已有合格词汇图片，直接使用并保留来源，不为追求统一而重复生成。

### 6. 思维导图处理

- 原始文件保存在 `content/od1/unit-{NN}/mind_map.png`。
- 网页运行时副本放在 `public/units/od1/unit-{NN}/assets/images/mind-map.png`。
- 第 3 段必须包含真实思维导图、准确的 `alt`、简短图注和 3–5 个复述提示词。
- 不要把思维导图内容重新拆成新的完整 section。
- 用户更新思维导图时，保留 `content/` 原稿，并同步替换运行时副本。

### 7. 映射为 OD2 七段式页面

先运行脚手架：

```bash
python tools/create_unit.py od1 5 "Unit title"
```

然后严格按以下结构制作：

1. `1 Key Vocabulary`：词汇图 + 主词汇点击/拖拽分类；同时支持点击选择后点击投放。
2. `2 Knowledge List Guide`：Reading Skill、主旨、人物/步骤/关键信息卡。
3. `3 Mind Map Workshop`：真实思维导图 + 复述提示。
4. `4 Grammar and Expression`：规则卡 + 短例句，不嵌入语法截图。
5. `5 Challenge Practice`：只保留一个统一互动练习，内容来自主词汇、阅读或语法。
6. `6 Writing Task`：HTML 范文 + 3–4 条句型框架 + 纸上手写提交提示。
7. `7 Wrap-Up`：约 4 条 `I can ...` 自检句，回收 Words / Reading / Grammar / Writing。

顶部学习地图固定为 `Words`、`Reading`、`Grammar`、`Writing`。不要新增 Listening、Speaking、Communicate、Project 或普通 Wrap Up 大段。

### 8. 页面实现要求

- 页面继续使用单文件 HTML，CSS 内联，JS 放在底部。
- 页面最大宽度约 `900px`，兼容 safe area，手机端收成单列。
- 图片使用相对路径 `assets/images/...`，不得引用 `content/`、`*_extracted/` 或 `source-pages/`。
- 拖拽活动必须有触屏点击替代路径。
- 可投放区支持键盘聚焦；反馈使用 `aria-live="polite"`。
- 每个练习提供 `Check Answers`、`Start Over` 和即时结果。
- Writing 不使用 `canvas`、`textarea` 或网页横线手写区。
- 新 Unit 完成后，把 `public/levels/od-level-1.html` 对应卡片改为正式链接和真实标题。

### 9. 必做校验

完成页面后依次执行：

```bash
python tools/validate_units.py
rg -n "Listen & Speak|Listening|Speaking|source-pages|_extracted" public/units/od1/unit-05 -g "*.html"
rg -n "<h2|assets/images/mind-map|assets/images/vocabulary" public/units/od1/unit-05/index.html
```

验收时确认：

- 标准 7 个标题数量和顺序正确。
- 页面不存在 Listening / Speaking 内容。
- 词汇图和思维导图均能从本地打开。
- 所有本地 `src` / `href` 指向存在文件。
- 词汇拖拽可用鼠标、触屏点击和键盘完成。
- Challenge 每题只有一个正确答案，检查和重置逻辑有效。
- iPad 和手机宽度无横向滚动、遮挡和文字重叠。
- Writing 只引导纸质书写。
- Wrap-Up 与本 Unit 的实际学习目标一致。

### 10. 每个 Unit 的标准交付物

```text
content/od1/unit-{NN}/
├─ OD1-UnitX 知识清单.docx
├─ OD1-UnitX 知识清单_extracted/
├─ mind_map.png
└─ image-prompts.md              # 仅在需要生成图片时创建

public/units/od1/unit-{NN}/
├─ index.html
└─ assets/images/
   ├─ vocabulary.png|webp
   └─ mind-map.png|webp
```

如果某项资源确实不需要，允许省略对应文件；但 HTML 中不得保留失效引用、占位按钮、死代码或“稍后补充”文案。


## 代码实现约束

当前页面是单文件 HTML，新增或修改同类页面时优先保持这种轻量结构：

- CSS 写在页面内，使用 `:root` 变量集中管理颜色和圆角。
- JS 写在页面底部，避免引入重型框架。
- 资源路径使用相对路径，例如 `assets/images/...`。
- 不依赖构建工具即可打开和使用。

命名应语义化，参考现有类名：

- `.hero`
- `.section`
- `.purpose`
- `.card`
- `.chip`
- `.topic-word-chip`
- `.phrase-chip`
- `.report`
- `.summary`

交互代码应保持小函数组织：

- 初始化函数只负责一个活动。
- 状态更新函数单独命名。
- 检查、重置、拖放、触屏选择逻辑分开。

## 质量检查清单

修改页面后至少检查：

- iPad 宽度下没有横向滚动。
- 手机宽度下所有 grid 都能收成单列。
- 所有按钮和 chip 可用手指准确点击。
- 拖拽活动也能通过点击完成。
- 正确/错误/选中/可投放状态颜色清楚。
- 图片没有变形，裁切区域符合题目。
- 英文任务说明短而明确。
- Wrap-Up 能明确回收本课目标。

## 已知生成问题记录

生成或修改新 Unit 页面时，必须特别避免以下已出现过的问题：

- 不要在 Unit 12 模板主线之外随意新增完整学习模块。例如 Unit 3 不应新增独立的 `Listening Clues` 大段；听力词汇可作为词汇补充或不放入页面，页面主线仍应贴近 Words / Reading / Mind Map / Grammar / Practice / Writing / Wrap-Up。
- 思维导图是核心学习资源，类似 `public/units/od2/unit-03/assets/images/mind-map.webp` 的 mind map 图片必须保留。删除辅助复述截图时，不要误删 mind map 区块。
- 语法和作文模块如果素材图片主要是文字题目或表格，应提取为 HTML 文本、表格、卡片和句型框架，不要直接嵌入整张文字截图。词汇图、思维导图等真正服务识图和复述的图片可以保留。
- 对照 Unit 12 模板时，先核对段落数量、编号和导航锚点，再处理局部素材。删除模块后必须同步清理对应 JS 初始化、按钮 id、报告区 id 和导航目标，避免残留死代码。
- 写作模块仍然只引导纸质手写提交，不要加入网页内书写板或把图片里的横线作文区域原样嵌入。
- Unit 2 曾出现过整个架构偏离相邻单元的问题：页面把 Reading Strategy、Communicate、Speaking、Story Check、Writing Project、Wrap Up 等拆成过多独立大段，并把教材截图作为正文内容嵌入。以后修复或生成类似页面时，必须先核对相邻 Unit 的 7 段式标题和学习地图，再把教材图片中的文字提取成 HTML 文本、卡片、表格、句型框架或单一 Challenge 练习。
- Unit 2 类型内容的处理原则：`1 Key Vocabulary` 可以保留词汇识图；`3 Mind Map Workshop` 必须保留真实 mind map；其它教材页截图（reading comprehension、grammar、communicate、speaking、project、wrap-up 等）不得作为主要正文图片嵌入，应转写为 HTML。第 5 段通常只保留一个统一的 `Challenge Practice` 互动活动，避免把多个小练习拆成多个完整 section。
- 页面修复完成后，必须用 `rg` 检查是否仍有不应存在的教材截图路径残留，例如 `unitX-reading-*`、`unitX-grammar-*`、`unitX-communicate-*`、`unitX-speaking-*`、`unitX-project-*`、`unitX-wrap-*`、`source-pages`。如果这些图片只是文字页或整页教材截图，应删除对应 `<img>` 并改成 HTML 文本。

## 设计判断原则

当不确定怎么设计时，优先问：

1. 小学生能不能一眼看懂现在要做什么？
2. 老师能不能直接拿到课堂上使用？
3. iPad 上点、拖、写是否舒服？
4. 颜色是否活泼但不混乱？
5. 页面是否像学习活动，而不是广告页或后台系统？

满足以上问题的方案，通常就是本项目正确的设计方向。
