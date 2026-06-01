import time
from typing import Callable, Optional, Dict, List
from .customer_feedback_agent import CustomerFeedbackAgent
from .market_research_agent import MarketResearchAgent
from .competitor_analysis_agent import CompetitorAnalysisAgent
from .swot_analysis_agent import SWOTAnalysisAgent
from .feature_prioritization_agent import FeaturePrioritizationAgent
from .strategy_recommendation_agent import StrategyRecommendationAgent
from .executive_report_agent import ExecutiveReportAgent


class Orchestrator:
    """
    Coordinates all specialized agents in a sequential pipeline.
    Each agent's output feeds into the context for downstream agents.

    Pipeline order:
      1. Customer Feedback Agent    — voice of customer
      2. Market Research Agent      — market intelligence
      3. Competitor Analysis Agent  — competitive landscape
      4. SWOT Analysis Agent        — synthesized position
      5. Feature Prioritization     — what to build next
      6. Strategy Recommendation    — how to win
      7. Executive Report Agent     — board-ready summary
    """

    AGENT_PIPELINE = [
        ("customer_feedback", "Customer Feedback Agent", "Analyzing customer sentiment and pain points..."),
        ("market_research", "Market Research Agent", "Extracting market trends and opportunities..."),
        ("competitor_analysis", "Competitor Analysis Agent", "Assessing competitive landscape..."),
        ("swot_analysis", "SWOT Analysis Agent", "Synthesizing SWOT from all findings..."),
        ("feature_prioritization", "Feature Prioritization Agent", "Prioritizing features and improvements..."),
        ("strategy_recommendations", "Strategy Recommendation Agent", "Generating strategic roadmap..."),
        ("executive_summary", "Executive Report Agent", "Crafting executive summary..."),
    ]

    def __init__(self):
        self.agents = {
            "customer_feedback": CustomerFeedbackAgent(),
            "market_research": MarketResearchAgent(),
            "competitor_analysis": CompetitorAnalysisAgent(),
            "swot_analysis": SWOTAnalysisAgent(),
            "feature_prioritization": FeaturePrioritizationAgent(),
            "strategy_recommendations": StrategyRecommendationAgent(),
            "executive_summary": ExecutiveReportAgent(),
        }

    def run(
        self,
        data: str,
        progress_callback: Optional[Callable[[str, str, int, int], None]] = None,
    ) -> Dict[str, str]:
        """
        Execute the full analysis pipeline.

        Args:
            data: Combined text from all uploaded documents.
            progress_callback: Called as (agent_key, status_msg, current_step, total_steps).

        Returns:
            Dict mapping agent keys to their output strings.
        """
        results: Dict[str, str] = {}
        total = len(self.AGENT_PIPELINE)

        for step, (key, name, status_msg) in enumerate(self.AGENT_PIPELINE, 1):
            if progress_callback:
                progress_callback(key, f"[{step}/{total}] {status_msg}", step, total)

            try:
                prior_context = self._build_context(results)
                output = self._run_agent(key, data, prior_context)
                results[key] = output
            except Exception as e:
                results[key] = f"[Error in {name}: {str(e)}]"

        return results

    def _run_agent(self, key: str, data: str, prior_context: str) -> str:
        agent_map = {
            "customer_feedback": lambda: self.agents["customer_feedback"].run(data),
            "market_research": lambda: self.agents["market_research"].run(data),
            "competitor_analysis": lambda: self.agents["competitor_analysis"].run(data, prior_context),
            "swot_analysis": lambda: self.agents["swot_analysis"].run(data, prior_context),
            "feature_prioritization": lambda: self.agents["feature_prioritization"].run(data, prior_context),
            "strategy_recommendations": lambda: self.agents["strategy_recommendations"].run(data, prior_context),
            "executive_summary": lambda: self.agents["executive_summary"].run(prior_context),
        }
        return agent_map[key]()

    def _build_context(self, results: Dict[str, str]) -> str:
        """Build a condensed context string from all completed agent results."""
        if not results:
            return ""
        parts = []
        labels = {
            "customer_feedback": "Customer Feedback Analysis",
            "market_research": "Market Research",
            "competitor_analysis": "Competitor Analysis",
            "swot_analysis": "SWOT Analysis",
            "feature_prioritization": "Feature Prioritization",
            "strategy_recommendations": "Strategic Recommendations",
        }
        for key, output in results.items():
            label = labels.get(key, key.replace("_", " ").title())
            # Truncate each section to avoid context overflow
            truncated = output[:3000] + ("..." if len(output) > 3000 else "")
            parts.append(f"### {label}\n{truncated}")
        return "\n\n".join(parts)

    def run_single_agent(self, key: str, data: str, existing_results: Dict[str, str]) -> str:
        """Re-run a single agent, useful for regeneration."""
        prior_context = self._build_context({k: v for k, v in existing_results.items() if k != key})
        output = self._run_agent(key, data, prior_context)
        return output

    def get_chat_context(self, results: Dict[str, str], max_chars: int = 15000) -> str:
        """Build a chat context from results for conversational Q&A."""
        full = self._build_context(results)
        if len(full) > max_chars:
            return full[:max_chars] + "\n\n[Context truncated for chat performance]"
        return full
