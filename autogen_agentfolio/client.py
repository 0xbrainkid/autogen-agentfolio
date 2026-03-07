"""Synchronous AgentFolio API client for AutoGen tools."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import HTTPError


_BASE = "https://agentfolio.bot"


class AgentFolioClient:
    """Thin wrapper around the AgentFolio REST API (no external deps beyond stdlib)."""

    def __init__(self, base_url: str = _BASE, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get(self, path: str) -> Any:
        url = f"{self.base_url}{path}"
        req = Request(url, headers={"Accept": "application/json"})
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        try:
            with urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as exc:
            return {"error": exc.code, "message": exc.reason}

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Fetch a single agent profile."""
        return self._get(f"/api/v1/agents/{agent_id}")

    def search_agents(
        self,
        query: Optional[str] = None,
        skill: Optional[str] = None,
        min_trust: int = 0,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search agents by keyword/skill with optional trust floor."""
        params = [f"limit={limit}"]
        if query:
            params.append(f"q={query}")
        if skill:
            params.append(f"skill={skill}")
        if min_trust > 0:
            params.append(f"minTrust={min_trust}")
        qs = "&".join(params)
        data = self._get(f"/api/v1/agents?{qs}")
        return data if isinstance(data, list) else data.get("agents", [data])

    def get_trust(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed trust breakdown for an agent."""
        profile = self.get_agent(agent_id)
        if "error" in profile:
            return profile
        return {
            "agent_id": agent_id,
            "name": profile.get("name"),
            "trust_score": profile.get("trustScore", 0),
            "tier": profile.get("tier", 0),
            "verifications": profile.get("verifications", {}),
        }

    def marketplace_jobs(self, status: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """List marketplace jobs."""
        data = self._get(f"/api/v1/marketplace/jobs?status={status}&limit={limit}")
        return data if isinstance(data, list) else data.get("jobs", [data])
