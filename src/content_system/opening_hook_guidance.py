from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class OpeningHookGuidance:
    hook_strategy: str
    opening_question: str
    first_paragraph_guidance: str
    avoid_opening_patterns: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


class OpeningHookGenerator:
    def __init__(self):
        self.marketing_patterns = [
            "震惊", "你绝对想不到", "揭秘", "深度解析", "独家",
            "必看", "收藏", "干货", "吐血整理", "重磅",
            "刷屏", "爆了", "炸裂", "神级", "逆天",
        ]

    def generate_opening_hook(
        self,
        topic_title: str,
        framework_name: Optional[str] = None,
    ) -> OpeningHookGuidance:
        strategies = {
            "新闻解读框架": "开门见山",
            "产品策略分析框架": "从产品变化切入",
            "行业趋势分析框架": "描述趋势现象",
            "投资框架分析": "从投资事件引出",
            "技术路线分析框架": "描述技术变化",
            "竞争格局分析框架": "描述竞争变化",
            "商业模式分析框架": "描述模式变化",
        }

        hook_strategy = strategies.get(framework_name, "开门见山")

        opening_questions = {
            "开门见山": f"{topic_title}背后的核心逻辑是什么？",
            "从产品变化切入": f"{topic_title}的产品决策背后有何战略意图？",
            "描述趋势现象": f"{topic_title}这一趋势是真趋势还是短期噪音？",
            "从投资事件引出": f"{topic_title}的投资价值如何判断？",
            "描述技术变化": f"{topic_title}的技术路线选择是否合理？",
            "描述竞争变化": f"{topic_title}将如何改变竞争格局？",
            "描述模式变化": f"{topic_title}的商业模式是否可持续？",
        }

        opening_question = opening_questions.get(hook_strategy, f"{topic_title}值得关注的核心是什么？")

        first_paragraph_guidance = (
            f"用一句话概括{topic_title}的核心判断，"
            "然后引用1-2个关键证据支持这一判断，"
            "避免使用夸张形容词和营销号表达。"
        )

        return OpeningHookGuidance(
            hook_strategy=hook_strategy,
            opening_question=opening_question,
            first_paragraph_guidance=first_paragraph_guidance,
            avoid_opening_patterns=self.marketing_patterns,
        )

    def check_marketing_style(self, text: str) -> Dict:
        hits = []
        for pattern in self.marketing_patterns:
            if pattern in text:
                hits.append(pattern)

        return {
            "has_marketing_style": len(hits) > 0,
            "marketing_pattern_hits": hits,
            "suggestion": "删除营销号表达方式，改用专业、克制的开头",
        }


def generate_opening_hook(
    topic_title: str,
    framework_name: Optional[str] = None,
) -> OpeningHookGuidance:
    generator = OpeningHookGenerator()
    return generator.generate_opening_hook(topic_title, framework_name)


def check_marketing_style(text: str) -> Dict:
    generator = OpeningHookGenerator()
    return generator.check_marketing_style(text)
