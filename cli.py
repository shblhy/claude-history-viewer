#!/usr/bin/env python3
"""
Claude History Viewer - CLI Query Tool
命令行查询工具 - 无需启动 Web 服务

Usage / 用法:
    python cli.py list                    # 列出所有会话
    python cli.py search <keyword>        # 搜索关键词
    python cli.py view <session-id>       # 查看对话详情
    python cli.py projects                # 列出所有项目
"""

import sys
import json
from pathlib import Path

# 导入 app.py 中的函数
from app import (
    build_content_cache,
    get_all_sessions,
    search_sessions,
    get_conversation,
    CLAUDE_PROJECTS
)

# ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.END}\n")

def cmd_list(args):
    """列出所有会话"""
    print_header("所有会话 / All Sessions")

    sessions, stats = get_all_sessions()

    print(f"{Colors.CYAN}统计 / Stats:{Colors.END}")
    print(f"  项目 / Projects: {stats['projects']}")
    print(f"  会话 / Sessions: {stats['sessions']}")
    print(f"  消息 / Messages: {stats['messages']:,}\n")

    print(f"{Colors.CYAN}最近 20 个会话 / Recent 20 Sessions:{Colors.END}\n")

    for i, s in enumerate(sessions[:20], 1):
        source_tag = f"{Colors.GREEN}[Web]{Colors.END} " if s['source'] == 'web' else ""
        print(f"{Colors.DIM}{i:3d}.{Colors.END} {source_tag}{Colors.BOLD}{s['title'][:50]}{Colors.END}")
        print(f"     {Colors.DIM}项目: {s['project_name']} | 时间: {s['date']} | ID: {s['id'][:12]}...{Colors.END}")
        print()

def cmd_search(args):
    """搜索会话"""
    if not args:
        print(f"{Colors.RED}错误: 请提供搜索关键词{Colors.END}")
        print("用法: python cli.py search <keyword>")
        return

    keyword = ' '.join(args)
    print_header(f"搜索: '{keyword}'")

    results = search_sessions(keyword, search_content=True, search_title=True)

    if not results:
        print(f"{Colors.YELLOW}未找到匹配结果{Colors.END}")
        return

    print(f"{Colors.GREEN}找到 {len(results)} 个匹配结果{Colors.END}\n")

    for i, s in enumerate(results[:20], 1):
        source_tag = f"{Colors.GREEN}[Web]{Colors.END} " if s['source'] == 'web' else ""
        match_info = f"{Colors.YELLOW}({s.get('match_count', 0)}次匹配){Colors.END}" if 'match_count' in s else ""

        print(f"{Colors.DIM}{i:3d}.{Colors.END} {source_tag}{Colors.BOLD}{s['title'][:50]}{Colors.END} {match_info}")
        print(f"     {Colors.DIM}项目: {s['project_name']} | 时间: {s['date']}{Colors.END}")

        if s.get('snippet'):
            snippet = s['snippet'][:150].replace('\n', ' ')
            print(f"     {Colors.DIM}...{snippet}...{Colors.END}")

        print(f"     {Colors.CYAN}ID: {s['id']}{Colors.END}")
        print()

def cmd_view(args):
    """查看对话详情"""
    if not args:
        print(f"{Colors.RED}错误: 请提供会话 ID{Colors.END}")
        print("用法: python cli.py view <session-id>")
        print("提示: 使用 'python cli.py list' 或 'python cli.py search <keyword>' 查看 ID")
        return

    session_id = args[0]

    # 查找对应的项目
    sessions, _ = get_all_sessions()
    target = None

    for s in sessions:
        if s['id'].startswith(session_id) or s['id'] == session_id:
            target = s
            break

    if not target:
        print(f"{Colors.RED}错误: 未找到会话 ID '{session_id}'{Colors.END}")
        return

    print_header(f"对话详情 / Conversation: {target['title'][:40]}")
    print(f"{Colors.DIM}项目: {target['project_name']} | 时间: {target['date']}{Colors.END}\n")

    messages = get_conversation(target['project'], target['id'])

    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')

        if role == 'user':
            role_str = f"{Colors.GREEN}User{Colors.END}"
        elif role == 'assistant':
            role_str = f"{Colors.BLUE}Assistant{Colors.END}"
        elif role == 'system':
            role_str = f"{Colors.YELLOW}System{Colors.END}"
        elif role == 'summary':
            role_str = f"{Colors.CYAN}Summary{Colors.END}"
        else:
            role_str = role

        print(f"{Colors.BOLD}{role_str}:{Colors.END}")
        print(f"{Colors.DIM}{content[:500]}{Colors.END}")
        print()

def cmd_projects(args):
    """列出所有项目"""
    print_header("项目列表 / Projects")

    if not CLAUDE_PROJECTS.exists():
        print(f"{Colors.YELLOW}未找到 Claude 项目目录{Colors.END}")
        print(f"  期望路径: {CLAUDE_PROJECTS}")
        return

    projects = {}
    for project_dir in CLAUDE_PROJECTS.iterdir():
        if project_dir.is_dir():
            # 统计会话数
            session_count = len(list(project_dir.glob("*.jsonl")))
            projects[project_dir.name] = session_count

    if not projects:
        print(f"{Colors.YELLOW}没有找到任何项目{Colors.END}")
        return

    print(f"{Colors.CYAN}共 {len(projects)} 个项目:{Colors.END}\n")

    # 按会话数排序
    sorted_projects = sorted(projects.items(), key=lambda x: x[1], reverse=True)

    for project, count in sorted_projects:
        print(f"  {Colors.BOLD}{project}{Colors.END} ({count} 个会话)")

    # Web 导出
    web_export = Path.home() / ".claude" / "web_export"
    if web_export.exists():
        print(f"\n  {Colors.GREEN}[Web] claude.ai 导出{Colors.END}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print(f"\n{Colors.DIM}提示: 第一次使用会自动构建搜索索引，可能需要几秒钟{Colors.END}")
        return

    # 初始化缓存
    print(f"{Colors.DIM}[*] 构建搜索索引...{Colors.END}", end='', flush=True)
    build_content_cache()
    print(f" {Colors.GREEN}完成{Colors.END}\n")

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    commands = {
        'list': cmd_list,
        'ls': cmd_list,
        'search': cmd_search,
        'find': cmd_search,
        'view': cmd_view,
        'show': cmd_view,
        'cat': cmd_view,
        'projects': cmd_projects,
        'proj': cmd_projects,
    }

    if command in commands:
        commands[command](args)
    else:
        print(f"{Colors.RED}错误: 未知命令 '{command}'{Colors.END}")
        print(f"\n可用命令: {', '.join(commands.keys())}")

if __name__ == '__main__':
    main()
