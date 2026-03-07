"""AutoGen function tools for AgentFolio — identity lookup, trust gating, marketplace.

AutoGen uses plain Python functions registered via `register_for_llm` / `register_for_execution`.
This module provides both standalone functions and a convenience registrar.
"""

from __future__ import annotations

import json
from typing import Annotated, Any, Dict, List, Optional

from autogen_agentfolio.client import AgentFolioClient


_client = AgentFolioClient()


def lookup_agent(
    agent_id: Annotated[str, "AgentFolio agent ID, e.g. 'agent_braingrowth'"],
) -> str:
    """Look up an AI agent's profile on AgentFolio. Returns name, bio, skills, trust score."""
    result = _client.get_agent(agent_id)
    return json.dumps(result, indent=2, default=str)


def search_agents(
    query: Annotated[str, "Search keyword"] = "",
    skill: Annotated[str, "Filter by skill"] = "",
    min_trust: Annotated[int, "Minimum trust score (0-500)"] = 0,
    limit: Annotated[int, "Max results"] = 5,
) -> str:
    """Search the AgentFolio directory for AI agents by keyword, skill, or trust score."""
    results = _client.search_agents(
        query=query or None,
        skill=skill or None,
        min_trust=min_trust,
        limit=limit,
    )
    return json.dumps(results, indent=2, default=str)


def verify_agent_trust(
    agent_id: Annotated[str, "AgentFolio agent ID"],
) -> str:
    """Get detailed trust verification breakdown — score, tier, and all proofs."""
    result = _client.get_trust(agent_id)
    return json.dumps(result, indent=2, default=str)


def trust_gate(
    agent_id: Annotated[str, "Agent ID to check"],
    min_trust: Annotated[int, "Minimum trust score to pass"] = 50,
) -> str:
    """Check whether an agent meets a minimum trust threshold. Returns pass/fail."""
    trust = _client.get_trust(agent_id)
    if "error" in trust:
        return json.dumps(trust)
    score = trust.get("trust_score", 0)
    return json.dumps({
        "agent_id": agent_id,
        "trust_score": score,
        "threshold": min_trust,
        "passed": score >= min_trust,
    })


def marketplace_jobs(
    status: Annotated[str, "Job status filter"] = "open",
    limit: Annotated[int, "Max results"] = 5,
) -> str:
    """Browse open jobs on the AgentFolio marketplace."""
    jobs = _client.marketplace_jobs(status=status, limit=limit)
    return json.dumps(jobs, indent=2, default=str)


def register_agentfolio_tools(assistant, executor) -> None:
    """Convenience: register all AgentFolio functions with an AutoGen AssistantAgent + UserProxyAgent.

    Usage:
        from autogen_agentfolio import register_agentfolio_tools
        register_agentfolio_tools(assistant, user_proxy)
    """
    for fn in [lookup_agent, search_agents, verify_agent_trust, trust_gate, marketplace_jobs]:
        assistant.register_for_llm(description=fn.__doc__)(fn)
        executor.register_for_execution()(fn)
