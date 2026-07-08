"""
Phase36: Rollback & Safety Runbook
生成回滚和安全操作手册
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json


@dataclass
class RollbackSection:
    section_id: str
    title: str
    description: str
    commands: List[str]
    notes: str = ""


@dataclass
class RollbackRunbookResult:
    schema_version: str = "v1"
    generated_at: str = ""
    
    sections: List[RollbackSection] = field(default_factory=list)
    
    contains_pause_resume: bool = False
    contains_disable_rss: bool = False
    
    status: str = "runbook_generated"
    section_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "sections": [
                {
                    "section_id": s.section_id,
                    "title": s.title,
                    "description": s.description,
                    "commands": s.commands,
                    "notes": s.notes
                }
                for s in self.sections
            ],
            "contains_pause_resume": self.contains_pause_resume,
            "contains_disable_rss": self.contains_disable_rss,
            "status": self.status,
            "section_count": self.section_count
        }


def build_rollback_safety_runbook() -> RollbackRunbookResult:
    """构建回滚和安全 runbook"""
    
    result = RollbackRunbookResult(
        generated_at=datetime.now().isoformat()
    )
    
    result.sections = [
        RollbackSection(
            section_id="pause_runtime",
            title="如何暂停 Runtime",
            description="暂停 Mac mini Runtime 定时任务",
            commands=[
                "python3 scripts/runtime_control.py pause",
                "# 确认状态",
                "python3 scripts/runtime_control.py status"
            ],
            notes="暂停后 Runtime 不执行定时任务，但可手动运行"
        ),
        RollbackSection(
            section_id="resume_runtime",
            title="如何恢复 Runtime",
            description="恢复 Mac mini Runtime 定时任务",
            commands=[
                "python3 scripts/runtime_control.py resume",
                "# 确认状态",
                "python3 scripts/runtime_control.py status"
            ],
            notes="恢复后 Runtime 恢复定时任务执行"
        ),
        RollbackSection(
            section_id="disable_rss",
            title="如何停用真实 RSS 源",
            description="停用本地真实 RSS 源配置",
            commands=[
                "# 清空 .env.rss",
                "echo 'GEEKPARK_RSS_URL=' > .env.rss",
                "echo 'OFFICIAL_AI_RSS_URL=' >> .env.rss",
                "# 确认未启用",
                "cat .env.rss"
            ],
            notes="停用后 RSS ingest 将使用 mock 数据或 dry-run"
        ),
        RollbackSection(
            section_id="delete_outputs",
            title="如何删除本地 RSS 运行产物",
            description="删除本地 RSS 运行产生的日志和输出",
            commands=[
                "rm -f 同行资本市场内容系统/10_logs/*rss-ingest*",
                "rm -f 同行资本市场内容系统/10_logs/*rss-clean*",
                "rm -f 同行资本市场内容系统/10_logs/*rss-intelligence*",
                "# 确认删除",
                "ls 同行资本市场内容系统/10_logs/*rss* 2>/dev/null || echo '已删除'"
            ],
            notes="不删除源码和配置文件"
        ),
        RollbackSection(
            section_id="check_secret",
            title="如何确认没有 secret 入库",
            description="检查 Git 中是否包含 RSS secret",
            commands=[
                "git status --short",
                "# 搜索可能泄漏的 URL",
                "grep -r 'https://' --include='*.json' --include='*.yaml' --include='*.md' 同行资本市场内容系统/10_logs/",
                "# 检查 .env.rss 是否被忽略",
                "cat .gitignore | grep '.env.rss'"
            ],
            notes="如有泄漏，立即删除并从 Git 历史中移除"
        ),
        RollbackSection(
            section_id="dry_run",
            title="如何回到 dry-run",
            description="恢复到云端 dry-run 模式",
            commands=[
                "# 确认 .env.rss 已清空",
                "cat .env.rss",
                "# 运行 dry-run pipeline",
                "make phase36-daily",
                "make phase35-daily",
                "make phase34a-daily",
                "make wechat-workbench"
            ],
            notes="Dry-run 不依赖真实 RSS 和 Runtime"
        ),
        RollbackSection(
            section_id="rollback_commit",
            title="如何回滚到上一个 commit",
            description="Git 回滚操作",
            commands=[
                "# 查看最近 commit",
                "git log --oneline -5",
                "# 回滚到上一个 commit（保留改动）",
                "git reset --soft HEAD~1",
                "# 或回滚到指定 commit",
                "git reset --hard <commit-hash>",
                "# 强制推送到远程（谨慎）",
                "git push --force origin main"
            ],
            notes="谨慎使用 --force，仅在必要时执行"
        ),
        RollbackSection(
            section_id="stop_observation",
            title="什么情况必须停止观察",
            description="需要立即停止观察的情况",
            commands=[
                "# 立即暂停 Runtime",
                "python3 scripts/runtime_control.py pause",
                "# 清空 RSS 配置",
                "echo '' > .env.rss",
                "# 检查泄漏",
                "git status --short"
            ],
            notes="""
以下情况必须立即停止：
- RSS secret 泄漏到 Git
- auto_publish 被意外启用
- OpenClaw 被意外修改
- 系统产生大量错误或异常输出
- 发现安全漏洞或合规问题
"""
        )
    ]
    
    # 标记特性
    result.contains_pause_resume = True
    result.contains_disable_rss = True
    result.section_count = len(result.sections)
    result.status = "runbook_generated"
    
    return result


def save_rollback_runbook(result: RollbackRunbookResult, output_dir: Path) -> Dict[str, str]:
    """保存回滚 runbook"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON
    dated_json = output_dir / f"{result.generated_at[:10].replace('-', '')}__rollback-safety-runbook.json"
    latest_json = output_dir / "latest_rollback_safety_runbook.json"
    
    json_data = result.to_dict()
    
    with open(dated_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    with open(latest_json, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Markdown (主要输出)
    md_content = _generate_rollback_runbook_md(result)
    
    dated_md = output_dir / f"{result.generated_at[:10].replace('-', '')}__rollback-safety-runbook.md"
    latest_md = output_dir / "latest_rollback_safety_runbook.md"
    
    with open(dated_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    with open(latest_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 同时写入 docs
    docs_dir = output_dir.parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    docs_md = docs_dir / "LOCAL_PRODUCTION_ROLLBACK_AND_SAFETY_RUNBOOK.md"
    with open(docs_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return {
        "dated_json": str(dated_json),
        "latest_json": str(latest_json),
        "dated_md": str(dated_md),
        "latest_md": str(latest_md),
        "docs_md": str(docs_md)
    }


def _generate_rollback_runbook_md(result: RollbackRunbookResult) -> str:
    """生成 Markdown 报告"""
    
    md = f"""# Local Production Rollback & Safety Runbook

## 概述

- **生成时间**: {result.generated_at}
- **状态**: {result.status}
- **章节总数**: {result.section_count}

---

"""
    
    for section in result.sections:
        md += f"## {section.section_id}. {section.title}\n\n"
        md += f"{section.description}\n\n"
        md += "**命令**:\n\n```bash\n"
        for cmd in section.commands:
            md += f"{cmd}\n"
        md += "```\n\n"
        if section.notes:
            md += f"**备注**: {section.notes}\n\n"
        md += "---\n\n"
    
    md += """
## 安全检查清单

执行回滚后，确认以下检查：

- [ ] Runtime 已暂停
- [ ] .env.rss 已清空
- [ ] RSS 运行产物已删除
- [ ] Git 中无 secret 泄漏
- [ ] .env.rss 在 .gitignore 中
- [ ] auto_publish 已禁用
- [ ] OpenClaw 未修改

---

**Phase36** | Local Production Rollback & Safety Runbook
"""
    
    return md