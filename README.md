# OD Interactive Courseware

面向 iPad / 触屏课堂的 OD1–OD4 少儿英语互动课件。项目保持零运行时依赖：部署时只需发布 `public/`。

## 常用命令

```bash
python tools/validate_units.py
python tools/create_unit.py od1 1 "Unit title"
```

规范页面地址统一为 `/units/od{level}/unit-{NN}/`。完整目录约定和迁移说明见 [项目架构](docs/architecture.md)。
