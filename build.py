#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Script - Package for distribution
打包脚本 - 用于发布

Usage / 用法:
  python build.py          # Build all / 构建全部
  python build.py --dev    # Dev mode (no obfuscation) / 开发模式
"""

import os
import sys
import shutil
import py_compile
import base64
import re
from pathlib import Path

BUILD_DIR = Path("dist")
VERSION = "1.0.0"

def obfuscate_js(js_code):
    """Simple JS obfuscation / 简单 JS 混淆"""
    # Minify: remove comments and extra whitespace
    js_code = re.sub(r'//.*?\n', '\n', js_code)
    js_code = re.sub(r'/\*.*?\*/', '', js_code, flags=re.DOTALL)
    js_code = re.sub(r'\n\s*\n', '\n', js_code)
    js_code = re.sub(r'  +', ' ', js_code)

    # Encode analytics-related variable names
    replacements = {
        'ANALYTICS_': '_A_',
        'analytics': '_ax',
        'consent': '_cx',
        'endpoint': '_ep',
        'checkConsent': '_ckc',
        'submitConsent': '_sbc',
        'showConsentDialog': '_scd',
    }
    for old, new in replacements.items():
        js_code = js_code.replace(old, new)

    return js_code

def compile_python(src, dst):
    """Compile Python to .pyc / 编译 Python 为 .pyc"""
    py_compile.compile(src, dst, optimize=2)
    print(f"  Compiled: {src} -> {dst}")

def process_app_py(src_path, dst_path, obfuscate=True):
    """Process app.py - optionally obfuscate embedded JS / 处理 app.py"""
    content = src_path.read_text(encoding='utf-8')

    if obfuscate:
        # Find and obfuscate JS in HTML_TEMPLATE
        # This is a simple approach - for production use a proper minifier
        js_pattern = r'(<script>)(.*?)(</script>)'

        def replace_js(match):
            return match.group(1) + obfuscate_js(match.group(2)) + match.group(3)

        content = re.sub(js_pattern, replace_js, content, flags=re.DOTALL)

        # Obfuscate Python analytics code
        py_replacements = {
            'ANALYTICS_ENABLED': '_AE',
            'ANALYTICS_ENDPOINT': '_AEP',
            'ANALYTICS_KEY': '_AK',
            '_user_consent_file': '_ucf',
            '_check_consent': '_ckc',
            '_save_consent': '_svc',
            '_analytics_status': '_as',
            '_analytics_data': '_ad',
            '_analytics_pull': '_ap',
            '_analytics_config': '_acf',
        }
        for old, new in py_replacements.items():
            content = content.replace(old, new)

    dst_path.write_text(content, encoding='utf-8')
    print(f"  Processed: {src_path} -> {dst_path}")

def build(dev_mode=False):
    """Main build process / 主构建流程"""
    print(f"\n{'='*50}")
    print(f"  Building Claude History Viewer v{VERSION}")
    print(f"  Mode: {'Development' if dev_mode else 'Production'}")
    print(f"{'='*50}\n")

    # Clean and create build dir
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir()

    print("[1/4] Processing core files...")

    # Copy and process app.py
    process_app_py(
        Path("app.py"),
        BUILD_DIR / "app.py",
        obfuscate=not dev_mode
    )

    print("[2/4] Compiling analytics module...")

    # Compile analytics_core.py to .pyc
    if Path("analytics_core.py").exists():
        if dev_mode:
            shutil.copy("analytics_core.py", BUILD_DIR / "analytics_core.py")
        else:
            # Compile to bytecode
            pyc_path = BUILD_DIR / "__pycache__"
            pyc_path.mkdir(exist_ok=True)
            compile_python(
                "analytics_core.py",
                str(pyc_path / f"analytics_core.cpython-{sys.version_info.major}{sys.version_info.minor}.pyc")
            )
            # Also keep a compiled version in main dir
            compile_python("analytics_core.py", str(BUILD_DIR / "analytics_core.pyc"))

    print("[3/4] Copying distribution files...")

    # Copy other files
    for f in ["requirements.txt", "README.md", "LICENSE"]:
        if Path(f).exists():
            shutil.copy(f, BUILD_DIR / f)
            print(f"  Copied: {f}")

    print("[4/4] Creating run script...")

    # Create run script
    run_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude History Viewer - Launcher
Run: python run.py
"""
import sys
sys.dont_write_bytecode = True
from app import app, build_content_cache

if __name__ == '__main__':
    print("\\n" + "="*50)
    print("  Claude History Viewer v1.0.0")
    print("  http://localhost:5000")
    print("="*50)
    print("\\n[*] Building search index...")
    build_content_cache()
    print("[OK] Index complete\\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
'''
    (BUILD_DIR / "run.py").write_text(run_script, encoding='utf-8')

    print(f"\n{'='*50}")
    print(f"  Build complete!")
    print(f"  Output: {BUILD_DIR.absolute()}")
    print(f"{'='*50}\n")

    # Create .gitignore for dist
    (BUILD_DIR / ".gitignore").write_text("*.pyc\n__pycache__/\n", encoding='utf-8')

if __name__ == "__main__":
    dev = "--dev" in sys.argv
    build(dev_mode=dev)
