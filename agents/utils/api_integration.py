"""
Frontend API Integration - Bridge between modular agents and React frontend
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from ..core.registry import AgentRegistry
from ..core.communication import get_message_bus, Message, MessageType


@dataclass
class AgentTaskRequest:
    agent_id: str
    task_data: Dict[str, Any]
    priority: int = 2  # Normal priority
    timeout: float = 30.0


@dataclass
class AgentTaskResponse:
    task_id: str
    agent_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class AgentAPIBridge:
    """Bridge between modular agents and frontend applications"""
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        
    async def list_agents(self) -> Dict[str, Any]:
        """List all available agents with their metadata"""
        try:
            agents_info = []
            agents = await self.registry.list_agents()
            
            for agent_data in agents:
                agents_info.append({
                    "id": agent_data.get("id"),
                    "name": agent_data.get("name", agent_data.get("id")),
                    "description": agent_data.get("description", ""),
                    "version": agent_data.get("version", "1.0.0"),
                    "capabilities": agent_data.get("capabilities", []),
                    "tags": agent_data.get("tags", []),
                    "status": "available"
                })
            
            return {
                "agents": agents_info,
                "total_count": len(agents_info)
            }
            
        except Exception as e:
            return {"error": f"Failed to list agents: {str(e)}"}
    
    async def execute_agent_task(self, request: AgentTaskRequest) -> AgentTaskResponse:
        """Execute a task with a specific agent"""
        task_id = f"{request.agent_id}_{datetime.utcnow().timestamp()}"
        start_time = datetime.utcnow()
        
        try:
            # Check if agent exists
            available_agents = await self.registry.list_agents()
            agent_exists = any(agent.get("id") == request.agent_id for agent in available_agents)
            
            if not agent_exists:
                return AgentTaskResponse(
                    task_id=task_id,
                    agent_id=request.agent_id,
                    status="failed",
                    error=f"Agent '{request.agent_id}' not found"
                )
            
            # Get agent instance
            agent = await self.registry.get_agent(request.agent_id)
            
            # Execute task
            result = await agent.execute(request.task_data)
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentTaskResponse(
                task_id=task_id,
                agent_id=request.agent_id,
                status="completed",
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentTaskResponse(
                task_id=task_id,
                agent_id=request.agent_id,
                status="failed",
                error=str(e),
                execution_time=execution_time
            )
    
    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status and health information for an agent"""
        try:
            # Check if agent exists
            available_agents = await self.registry.list_agents()
            agent_data = next((agent for agent in available_agents if agent.get("id") == agent_id), None)
            
            if not agent_data:
                return {"error": f"Agent '{agent_id}' not found"}
            
            return {
                "agent_id": agent_id,
                "status": "active",
                "health": "healthy",
                "last_active": datetime.utcnow(),
                "metrics": agent_data.get("metrics", {})
            }
            
        except Exception as e:
            return {"error": f"Failed to get agent status: {str(e)}"}
    
    async def execute_workflow(self, workflow_id: str, steps: List[Dict[str, Any]], 
                             metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a multi-agent workflow"""
        try:
            if metadata is None:
                metadata = {}
                
            # Validate all agents in workflow exist
            available_agents = await self.registry.list_agents()
            available_agent_ids = [agent.get("id") for agent in available_agents]
            
            for step in steps:
                agent_id = step.get("agent_id")
                if not agent_id or agent_id not in available_agent_ids:
                    return {
                        "error": f"Invalid agent '{agent_id}' in workflow step"
                    }
            
            # Execute workflow steps
            results = []
            for i, step in enumerate(steps):
                agent_id = step["agent_id"]
                task_data = step.get("task_data", {})
                
                # Execute step
                request = AgentTaskRequest(
                    agent_id=agent_id,
                    task_data=task_data
                )
                
                response = await self.execute_agent_task(request)
                
                results.append({
                    "step": i,
                    "agent_id": agent_id,
                    "result": asdict(response),
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                # Stop if step failed
                if response.status == "failed":
                    break
            
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "steps_count": len(results),
                "results": results,
                "completed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e)
            }
    
    async def get_legacy_agents_metadata(self) -> Dict[str, Any]:
        """
        Get agent metadata in the format expected by the legacy AIAgents.jsx component.
        This provides backward compatibility while transitioning to the modular system.
        """
        try:
            agents_data = {}
            available_agents = await self.registry.list_agents()
            
            # Map modular agents to legacy format
            for agent_data in available_agents:
                agent_id = agent_data.get("id")
                
                # Convert to legacy format
                agents_data[agent_id] = {
                    "id": agent_id,
                    "name": agent_data.get("name", agent_id),
                    "description": agent_data.get("description", ""),
                    "icon": agent_data.get("icon", "🤖"),
                    "color": agent_data.get("color", "blue"),
                    "metrics": {
                        "accuracy": agent_data.get("accuracy", 85.0),
                        "response_time": agent_data.get("avg_response_time", 1.2),
                        "success_rate": agent_data.get("success_rate", 94.0),
                        "total_requests": agent_data.get("total_requests", 150)
                    },
                    "capabilities": agent_data.get("capabilities", []),
                    "status": "active",
                    "last_updated": datetime.utcnow().isoformat()
                }
            
            return {"agents": agents_data}
            
        except Exception as e:
            return {"error": f"Failed to get legacy metadata: {str(e)}"}
    
    def to_json(self, data: Any) -> str:
        """Convert data to JSON string with datetime handling"""
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        return json.dumps(data, default=json_serializer)


# Singleton instance for easy access
_api_bridge: Optional[AgentAPIBridge] = None


def get_api_bridge() -> AgentAPIBridge:
    """Get the global API bridge instance"""
    global _api_bridge
    if _api_bridge is None:
        _api_bridge = AgentAPIBridge()
    return _api_bridge


# Convenience functions for direct use
async def list_available_agents() -> Dict[str, Any]:
    """List all available agents"""
    bridge = get_api_bridge()
    return await bridge.list_agents()


async def execute_agent(agent_id: str, task_data: Dict[str, Any]) -> AgentTaskResponse:
    """Execute a task with an agent"""
    bridge = get_api_bridge()
    request = AgentTaskRequest(agent_id=agent_id, task_data=task_data)
    return await bridge.execute_agent_task(request)


async def get_agent_info(agent_id: str) -> Dict[str, Any]:
    """Get information about a specific agent"""
    bridge = get_api_bridge()
    return await bridge.get_agent_status(agent_id)


# Example usage functions for testing
async def example_usage():
    """Example of how to use the API bridge"""
    bridge = get_api_bridge()
    
    # List all agents
    agents = await bridge.list_agents()
    print("Available agents:", bridge.to_json(agents))
    
    # Execute a task
    if agents.get("agents"):
        first_agent = agents["agents"][0]
        agent_id = first_agent["id"]
        
        request = AgentTaskRequest(
            agent_id=agent_id,
            task_data={"query": "Test task"}
        )
        
        response = await bridge.execute_agent_task(request)
        print("Task response:", bridge.to_json(asdict(response)))
    
    # Get legacy format for frontend
    legacy_data = await bridge.get_legacy_agents_metadata()
    print("Legacy format:", bridge.to_json(legacy_data))


if __name__ == "__main__":
    # Run example usage
    asyncio.run(example_usage())