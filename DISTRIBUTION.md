# Distribution Guide / 发布指南

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Build for Distribution

```bash
# Production build (obfuscated)
python build.py

# Development build (readable)
python build.py --dev
```

Output will be in `dist/` folder.

### Distribution Package Structure

```
dist/
├── app.py              # Main app (JS obfuscated)
├── analytics_core.pyc  # Core module (compiled)
├── run.py              # Launcher script
├── requirements.txt
├── README.md
└── LICENSE
```

### Protection Levels

| Component | Protection | Can be modified? |
|-----------|------------|------------------|
| app.py (HTML/CSS) | Readable | Yes |
| app.py (JS) | Minified + Obfuscated | Difficult |
| analytics_core.pyc | Compiled bytecode | No |
| API routes | Obfuscated names | Difficult |

### Self-Hosted Deployment

1. Build the package: `python build.py`
2. Copy `dist/` to your server
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python run.py`
5. (Optional) Configure reverse proxy (nginx/caddy)

### Data Collection Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/consent` | GET | Check consent status |
| `/api/consent` | POST | Update consent |
| `/a/s?k=KEY` | GET | Analytics status |
| `/a/d?k=KEY` | GET | Data summary |
| `/a/g?k=KEY&s=SID` | GET | Get session |
| `/a/c?k=KEY` | POST | Configure |

Default key: `chv2026` (change in analytics_core.py before building)

---

<a name="中文"></a>
## 中文

### 构建发布包

```bash
# 生产构建（混淆）
python build.py

# 开发构建（可读）
python build.py --dev
```

输出在 `dist/` 目录。

### 发布包结构

```
dist/
├── app.py              # 主程序（JS已混淆）
├── analytics_core.pyc  # 核心模块（已编译）
├── run.py              # 启动脚本
├── requirements.txt
├── README.md
└── LICENSE
```

### 保护级别

| 组件 | 保护方式 | 可修改？ |
|------|----------|----------|
| app.py (HTML/CSS) | 可读 | 可以 |
| app.py (JS) | 压缩 + 混淆 | 困难 |
| analytics_core.pyc | 编译字节码 | 不可以 |
| API 路由 | 混淆名称 | 困难 |

### 自建服务器部署

1. 构建: `python build.py`
2. 复制 `dist/` 到服务器
3. 安装依赖: `pip install -r requirements.txt`
4. 运行: `python run.py`
5. (可选) 配置反向代理 (nginx/caddy)

### 数据收集接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/consent` | GET | 检查同意状态 |
| `/api/consent` | POST | 更新同意状态 |
| `/a/s?k=KEY` | GET | 分析状态 |
| `/a/d?k=KEY` | GET | 数据摘要 |
| `/a/g?k=KEY&s=SID` | GET | 获取会话 |
| `/a/c?k=KEY` | POST | 配置 |

默认密钥: `chv2026` (构建前在 analytics_core.py 中修改)

---

## For Fork Users / Fork 用户说明

If you fork this project and want to disable analytics:

如果你 fork 了此项目并想禁用分析功能：

1. Delete `analytics_core.py` / 删除 `analytics_core.py`
2. In `app.py`, remove the Analytics Module section / 在 `app.py` 中删除 Analytics Module 部分
3. Remove consent dialog JS code / 删除同意弹窗 JS 代码

Or simply set `ANALYTICS_ENABLED = False` in app.py

或者直接在 app.py 中设置 `ANALYTICS_ENABLED = False`
