from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from .editorial_style_guide import EditorialStyleGuide, load_editorial_style_guide
from .narrative_frameworks import NarrativeFramework, load_narrative_frameworks


@dataclass
class PromptBuildResult:
    prompt: str
    style_guide_injected: bool
    framework_injected: bool
    title_policy_injected: bool
    ai_taste_guard_injected: bool

    def to_dict(self) -> Dict:
        return asdict(self)


class EditorialPromptBuilder:
    def __init__(self):
        self.style_guide = load_editorial_style_guide()
        self.frameworks = load_narrative_frameworks()

    def build_editorial_prompt(
        self,
        base_prompt: str,
        framework_id: Optional[str] = None,
        topic_title: str = "",
    ) -> PromptBuildResult:
        components = []

        components.append("# 编辑风格指南")
        components.append(f"读者画像: {', '.join(self.style_guide.reader_profile.core_readers)}")
        components.append(f"写作原则: {', '.join(self.style_guide.writing_principles)}")
        components.append(f"推荐语气: {', '.join(self.style_guide.tone.preferred)}")
        components.append(f"避免语气: {', '.join(self.style_guide.tone.discouraged)}")
        components.append(f"必备章节: {', '.join(self.style_guide.must_have_sections)}")

        style_guide_injected = True

        framework_injected = False
        if framework_id:
            framework = next((f for f in self.frameworks if f.framework_id == framework_id), None)
            if framework:
                components.append(f"\n# 叙事框架: {framework.name}")
                components.append(f"适用主题类型: {', '.join(framework.applicable_topic_types)}")
                components.append(f"目的: {framework.purpose}")
                components.append(f"章节顺序: {', '.join(framework.section_sequence)}")
                components.append(f"开头策略: {framework.opening_strategy}")
                components.append(f"证据策略: {framework.evidence_strategy}")
                components.append(f"反方观点策略: {framework.counterargument_strategy}")
                components.append(f"结尾策略: {framework.closing_strategy}")
                framework_injected = True

        components.append("\n# 标题生成策略")
        components.append("标题长度: 16-32字")
        components.append("必备元素: 核心事件/实体、差异化角度、明确读者价值")
        components.append("禁用模式: 震惊、一文看懂、彻底改变、颠覆一切等营销号表达")
        components.append("角度变体: 反常识、产业影响、产品策略、投资判断、方法论、风险提示")
        title_policy_injected = True

        components.append("\n# AI味表达拦截")
        components.append("避免使用: 值得关注、未来可期、赋能、重塑格局、革命性、引领未来等")
        components.append("要求: 使用具体判断替代空泛表达")
        components.append("要求: 避免过度形容词和营销号表达方式")
        ai_taste_guard_injected = True

        components.append(f"\n# 主题")
        components.append(f"主题标题: {topic_title}")

        components.append(f"\n# 原始指令")
        components.append(base_prompt)

        full_prompt = "\n".join(components)

        return PromptBuildResult(
            prompt=full_prompt,
            style_guide_injected=style_guide_injected,
            framework_injected=framework_injected,
            title_policy_injected=title_policy_injected,
            ai_taste_guard_injected=ai_taste_guard_injected,
        )

    def build_review_prompt(self, content_type: str = "draft") -> PromptBuildResult:
        base_prompt = f"""作为专业编辑，请审查以下{content_type}，重点关注：
1. 判断强度：核心判断是否明确、有依据
2. 证据密度：是否有足够的证据支持判断
3. 叙事流畅度：段落衔接和逻辑递进是否流畅
4. AI味：是否包含禁用的AI味表达
5. 标题质量：标题是否清晰、有差异化角度
6. 风险清晰度：风险因素是否明确表达

请提供具体的修改建议和质量评分。"""

        return self.build_editorial_prompt(base_prompt)


def build_editorial_prompt(
    base_prompt: str,
    framework_id: Optional[str] = None,
    topic_title: str = "",
) -> PromptBuildResult:
    builder = EditorialPromptBuilder()
    return builder.build_editorial_prompt(base_prompt, framework_id, topic_title)


def build_review_prompt(content_type: str = "draft") -> PromptBuildResult:
    builder = EditorialPromptBuilder()
    return builder.build_review_prompt(content_type)
