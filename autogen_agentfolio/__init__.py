"""autogen-agentfolio — Agent identity & trust for AutoGen, powered by AgentFolio."""

from autogen_agentfolio.client import AgentFolioClient
from autogen_agentfolio.tools import (
    lookup_agent,
    search_agents,
    verify_agent_trust,
    trust_gate,
    marketplace_jobs,
    register_agentfolio_tools,
)

__all__ = [
    "AgentFolioClient",
    "lookup_agent",
    "search_agents",
    "verify_agent_trust",
    "trust_gate",
    "marketplace_jobs",
    "register_agentfolio_tools",
]
__version__ = "0.1.0"
