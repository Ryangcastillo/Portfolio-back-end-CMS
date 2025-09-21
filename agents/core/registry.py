"""
Agent Registry - Centralized agent discovery, management, and lifecycle control
"""

import asyncio
import json
import os
from typing import Dict, List, Optional, Type, Any
from pathlib import Path
import importlib.util
import yaml

from .base import BaseAgent, AgentConfig, AgentStatus
from ..utils.monitoring import AgentMonitor


class AgentRegistry:
    """
    Centralized registry for agent discovery, instantiation, and management
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_classes: Dict[str, Type[BaseAgent]] = {}
        self.config_path = config_path or "agents/config/agents.yaml"
        self.monitor = AgentMonitor()
        self._lock = asyncio.Lock()
        
    async def initialize(self) -> None:
        """Initialize the registry and discover available agents"""
        await self._discover_agents()
        await self._load_configurations()
        
    async def _discover_agents(self) -> None:
        """Discover agent implementations from the implementations directory"""
        implementations_path = Path(__file__).parent.parent / "implementations"
        
        if not implementations_path.exists():
            return
            
        for agent_dir in implementations_path.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith('__'):
                await self._load_agent_module(agent_dir)
                
    async def _load_agent_module(self, agent_dir: Path) -> None:
        """Load an agent module from directory"""
        try:
            # Look for main agent file (agent.py or __init__.py)
            agent_file = agent_dir / "agent.py"
            if not agent_file.exists():
                agent_file = agent_dir / "__init__.py"
                
            if not agent_file.exists():
                return
                
            # Import the module
            spec = importlib.util.spec_from_file_location(
                f"agents.implementations.{agent_dir.name}", 
                agent_file
            )
            
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for agent class
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseAgent) and 
                        attr != BaseAgent):
                        
                        agent_id = agent_dir.name
                        self.agent_classes[agent_id] = attr
                        break
                        
        except Exception as e:
            print(f"Error loading agent from {agent_dir}: {e}")
            
    async def _load_configurations(self) -> None:
        """Load agent configurations from YAML file"""
        if not os.path.exists(self.config_path):
            return
            
        try:
            with open(self.config_path, 'r') as f:
                configs = yaml.safe_load(f)
                
            for agent_id, config_data in configs.items():
                if agent_id in self.agent_classes:
                    # Convert config data to AgentConfig object
                    # This would need proper mapping from your YAML structure
                    pass
                    
        except Exception as e:
            print(f"Error loading configurations: {e}")
            
    async def register_agent(self, agent_id: str, agent_class: Type[BaseAgent]) -> None:
        """Manually register an agent class"""
        async with self._lock:
            self.agent_classes[agent_id] = agent_class
            
    async def create_agent(self, agent_id: str, config: AgentConfig) -> BaseAgent:
        """Create an agent instance"""
        if agent_id not in self.agent_classes:
            raise ValueError(f"Agent class '{agent_id}' not found")
            
        agent_class = self.agent_classes[agent_id]
        agent = agent_class(config)
        
        return agent
        
    async def get_agent(self, agent_id: str, auto_start: bool = True) -> BaseAgent:
        """Get or create an agent instance"""
        async with self._lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                if agent.status == AgentStatus.STOPPED:
                    # Restart stopped agent
                    if auto_start:
                        await agent.start()
                return agent
                
            # Create new agent instance
            if agent_id not in self.agent_classes:
                raise ValueError(f"Agent '{agent_id}' not found")
                
            # Load default config for this agent
            config = await self._get_default_config(agent_id)
            agent = await self.create_agent(agent_id, config)
            
            if auto_start:
                await agent.start()
                
            self.agents[agent_id] = agent
            
            # Start monitoring
            await self.monitor.start_monitoring(agent)
            
            return agent
            
    async def _get_default_config(self, agent_id: str) -> AgentConfig:
        """Get default configuration for an agent"""
        # This would load from your config files
        # For now, return a minimal config
        from .base import AgentCategory, AgentMetrics, BusinessImpact, TechnicalSpec
        
        return AgentConfig(
            id=agent_id,
            title=f"{agent_id.replace('_', ' ').title()}",
            category=AgentCategory.CONVERSATIONAL_AI,
            description=f"Agent: {agent_id}",
            purpose="Default agent purpose",
            capabilities=[],
            technologies=[],
            status=AgentStatus.INITIALIZING,
            year="2025",
            complexity="Medium",
            technical_details=TechnicalSpec(),
            metrics=AgentMetrics(),
            business_impact=BusinessImpact("Default metric", [])
        )
        
    async def stop_agent(self, agent_id: str) -> None:
        """Stop a specific agent"""
        async with self._lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                await agent.stop()
                await self.monitor.stop_monitoring(agent_id)
                
    async def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the registry"""
        await self.stop_agent(agent_id)
        async with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
                
    async def list_agents(self) -> List[Dict[str, Any]]:
        """List all available agents"""
        agents_info = []
        
        for agent_id in self.agent_classes.keys():
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agents_info.append(agent.get_status())
            else:
                agents_info.append({
                    "id": agent_id,
                    "title": agent_id.replace('_', ' ').title(),
                    "status": "available",
                    "instance_id": None,
                    "created_at": None,
                    "last_activity": None
                })
                
        return agents_info
        
    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        if agent_id not in self.agents:
            if agent_id in self.agent_classes:
                return {"id": agent_id, "status": "available"}
            else:
                raise ValueError(f"Agent '{agent_id}' not found")
                
        return self.agents[agent_id].get_status()
        
    async def execute_agent(self, agent_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent with input data"""
        agent = await self.get_agent(agent_id)
        return await agent.execute(input_data)
        
    async def broadcast_message(self, message: Dict[str, Any], 
                              target_agents: Optional[List[str]] = None) -> Dict[str, Any]:
        """Broadcast a message to all or specific agents"""
        results = {}
        target_list = target_agents or list(self.agents.keys())
        
        for agent_id in target_list:
            if agent_id in self.agents:
                try:
                    result = await self.agents[agent_id].execute(message)
                    results[agent_id] = {"success": True, "result": result}
                except Exception as e:
                    results[agent_id] = {"success": False, "error": str(e)}
                    
        return results
        
    async def shutdown(self) -> None:
        """Shutdown all agents and clean up"""
        for agent_id in list(self.agents.keys()):
            await self.stop_agent(agent_id)
            
        await self.monitor.shutdown()
        
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents"""
        health_status = {
            "registry_status": "healthy",
            "total_agents": len(self.agent_classes),
            "active_agents": len(self.agents),
            "agents": {}
        }
        
        for agent_id, agent in self.agents.items():
            try:
                status = agent.get_status()
                health_status["agents"][agent_id] = {
                    "status": status["status"],
                    "last_activity": status["last_activity"],
                    "healthy": status["status"] in ["ready", "running"]
                }
            except Exception as e:
                health_status["agents"][agent_id] = {
                    "status": "error",
                    "error": str(e),
                    "healthy": False
                }
                
        return health_status


# Global registry instance
_registry: Optional[AgentRegistry] = None


async def get_registry() -> AgentRegistry:
    """Get the global agent registry instance"""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
        await _registry.initialize()
    return _registry


async def cleanup_registry() -> None:
    """Clean up the global registry"""
    global _registry
    if _registry:
        await _registry.shutdown()
        _registry = None