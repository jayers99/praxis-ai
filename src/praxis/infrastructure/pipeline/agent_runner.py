"""Agent invocation infrastructure for pipeline stages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AgentInvocationResult:
    """Result of invoking a subagent."""

    success: bool
    output: str | None = None
    agent_prompt: str = ""  # For manual invocation
    errors: list[str] | None = None

    def __post_init__(self) -> None:
        if self.errors is None:
            self.errors = []


def invoke_agent(
    agent_type: str,
    prompt: str,
    context_files: list[Path] | None = None,
) -> AgentInvocationResult:
    """
    Invoke a subagent and return its output.

    For now: Returns a structured prompt that the user
    can paste into Claude or run via Task tool.

    Future: Direct Claude API integration.

    Args:
        agent_type: Type of agent (e.g., "researcher", "architect").
        prompt: The task prompt for the agent.
        context_files: Optional list of files to include as context.

    Returns:
        AgentInvocationResult with the agent prompt for manual invocation.
    """
    if context_files is None:
        context_files = []

    # Build context section
    context_section = ""
    if context_files:
        file_list = "\n".join(f"- {f}" for f in context_files)
        context_section = f"""
## Context Files

Read and analyze these files:

{file_list}
"""

    # Build the agent prompt
    agent_prompt = f"""# Agent Task: {agent_type.title()}

{prompt}
{context_section}
## Instructions

Please analyze the context provided and respond with a structured analysis.
"""

    return AgentInvocationResult(
        success=True,
        output=None,  # No actual output - requires manual invocation
        agent_prompt=agent_prompt,
    )


def generate_idas_agent_prompt(corpus_dir: Path) -> str:
    """
    Generate the IDAS agent prompt for analytical synthesis.

    Args:
        corpus_dir: Directory containing the RTC corpus.

    Returns:
        Formatted prompt for the IDAS agent.
    """
    return f"""You are performing Inquiry-Driven Analytical Synthesis (IDAS).

## Your Task

Analyze the corpus at `{corpus_dir}` and produce:

1. **Dominant Themes** - Ranked by relevance to the research goal
2. **Identified Gaps** - What's missing or unclear
3. **Research Questions** - Well-formed questions for specialist investigation
4. **Assumptions** - What we're taking for granted
5. **Constraints** - Limitations or boundaries

## Output Format

Produce a markdown document with clear sections for each of the above.
Use evidence from the corpus to support your analysis.
Flag areas of uncertainty.

## Quality Criteria

- Themes should be specific and actionable
- Research questions should be answerable by specialists
- Assumptions should be explicitly stated, not hidden
- Gaps should inform the next stages of investigation
"""


def generate_sad_dispatch_prompt(
    idas_output: Path,
    specialist_type: str,
) -> str:
    """
    Generate a specialist dispatch prompt for SAD stage.

    Args:
        idas_output: Path to the IDAS output file.
        specialist_type: Type of specialist (e.g., "architect", "security").

    Returns:
        Formatted prompt for the specialist agent.
    """
    return f"""You are a {specialist_type.title()} Specialist.

## Your Task

Review the IDAS analysis at `{idas_output}` and provide expert perspective.

## Scope

- Focus on aspects relevant to your specialty
- Identify risks, opportunities, and recommendations
- Be specific and actionable
- Flag areas outside your expertise

## Output Format

Produce a structured markdown response with:

1. **Key Observations** - What stands out from your perspective
2. **Risks & Concerns** - Issues to address
3. **Recommendations** - Actionable suggestions
4. **Open Questions** - Areas needing clarification

## Constraints

- Stay within your specialty domain
- Don't duplicate analysis from other specialists
- Be concise but thorough
"""


def generate_ccr_challenger_prompt(
    specialist_outputs: list[Path],
    challenger_type: str,
) -> str:
    """
    Generate a CCR challenger prompt for critical review.

    Args:
        specialist_outputs: Paths to specialist output files.
        challenger_type: Type of challenger (e.g., "devil_advocate").

    Returns:
        Formatted prompt for the challenger agent.
    """
    files_list = "\n".join(f"- {f}" for f in specialist_outputs)

    return f"""You are a {challenger_type.replace('_', ' ').title()} Challenger.

## Your Task

Critically review the specialist outputs and challenge their conclusions.

## Files to Review

{files_list}

## Your Role

- Challenge assumptions made by specialists
- Identify potential blind spots
- Propose alternative interpretations
- Stress-test recommendations

## Output Format

Produce a structured critique with:

1. **Challenged Assumptions** - What was taken for granted
2. **Identified Risks** - Overlooked concerns
3. **Alternative Interpretations** - Other ways to read the data
4. **Recommendations** - How to strengthen the analysis

## Important

- Be constructive, not destructive
- Provide evidence for challenges
- Acknowledge valid points while identifying weaknesses
"""
