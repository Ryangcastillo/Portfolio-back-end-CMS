"""
Base Agent Architecture - Core interfaces and abstract classes for all AI agents
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
import time
import uuid
from datetime import datetime


class AgentStatus(Enum):
    """Agent lifecycle status"""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running" 
    ERROR = "error"
    STOPPED = "stopped"


class AgentCategory(Enum):
    """Agent categories for classification"""
    CONVERSATIONAL_AI = "conversational_ai"
    DOCUMENT_AUTOMATION = "document_automation"
    PROCESS_AUTOMATION = "process_automation"
    AGENT_ORCHESTRATION = "agent_orchestration"
    DOCUMENT_INTELLIGENCE = "document_intelligence"


@dataclass
class AgentMetrics:
    """Performance and operational metrics for agents"""
    accuracy: Optional[float] = None
    response_time: Optional[str] = None
    satisfaction: Optional[float] = None
    automation_rate: Optional[float] = None
    reliability: Optional[float] = None
    throughput: Optional[str] = None
    recovery_time: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass 
class BusinessImpact:
    """Business impact metrics and KPIs"""
    primary_metric: str
    secondary_metrics: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary": self.primary_metric,
            "metrics": self.secondary_metrics
        }


@dataclass
class TechnicalSpec:
    """Technical implementation details"""
    llm: Optional[str] = None
    framework: Optional[str] = None
    vector_db: Optional[str] = None
    deployment: Optional[str] = None
    integration: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class AgentConfig:
    """Complete agent configuration"""
    id: str
    title: str
    category: AgentCategory
    description: str
    purpose: str
    capabilities: List[str]
    technologies: List[str]
    status: AgentStatus
    year: str
    complexity: str
    technical_details: TechnicalSpec
    metrics: AgentMetrics
    business_impact: BusinessImpact
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category.value,
            "description": self.description,
            "purpose": self.purpose,
            "capabilities": self.capabilities,
            "technologies": self.technologies,
            "status": self.status.value,
            "year": self.year,
            "complexity": self.complexity,
            "technicalDetails": self.technical_details.to_dict(),
            "metrics": self.metrics.to_dict(),
            "businessImpact": self.business_impact.to_dict()
        }


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents
    Provides common functionality and enforces interface compliance
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.INITIALIZING
        self.instance_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.last_activity = None
        self._running_tasks: List[asyncio.Task] = []
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent with required resources"""
        pass
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
        
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data format and requirements"""
        pass
        
    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources when agent is stopped"""
        pass
    
    async def start(self) -> bool:
        """Start the agent"""
        try:
            if await self.initialize():
                self.status = AgentStatus.READY
                return True
            return False
        except Exception as e:
            self.status = AgentStatus.ERROR
            raise e
    
    async def stop(self) -> None:
        """Stop the agent and clean up resources"""
        self.status = AgentStatus.STOPPED
        
        # Cancel running tasks
        for task in self._running_tasks:
            if not task.done():
                task.cancel()
                
        await self.cleanup()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent processing with error handling and metrics"""
        if self.status != AgentStatus.READY:
            raise RuntimeError(f"Agent {self.config.id} is not ready (status: {self.status})")
            
        # Validate input
        if not await self.validate_input(input_data):
            raise ValueError("Invalid input data format")
            
        # Track execution
        start_time = time.time()
        self.status = AgentStatus.RUNNING
        self.last_activity = datetime.utcnow()
        
        try:
            result = await self.process(input_data)
            execution_time = time.time() - start_time
            
            # Add execution metadata
            result["_metadata"] = {
                "agent_id": self.config.id,
                "instance_id": self.instance_id,
                "execution_time": execution_time,
                "timestamp": self.last_activity.isoformat()
            }
            
            self.status = AgentStatus.READY
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            raise e
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics"""
        return {
            "id": self.config.id,
            "title": self.config.title,
            "category": self.config.category.value,
            "status": self.status.value,
            "instance_id": self.instance_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "running_tasks": len(self._running_tasks),
            "metrics": self.config.metrics.to_dict()
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.config.to_dict()


class ConversationalAgent(BaseAgent):
    """Base class for conversational AI agents"""
    
    @abstractmethod
    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a natural language query"""
        pass
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process conversational input"""
        query = input_data.get("query", "")
        context = input_data.get("context", {})
        
        response = await self.process_query(query, context)
        
        return {
            "response": response,
            "query": query,
            "agent_type": "conversational"
        }


class DocumentAgent(BaseAgent):
    """Base class for document processing agents"""
    
    @abstractmethod
    async def process_document(self, document: Any, options: Dict[str, Any]) -> Dict[str, Any]:
        """Process a document and return results"""
        pass
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process document input"""
        document = input_data.get("document")
        options = input_data.get("options", {})
        
        result = await self.process_document(document, options)
        
        return {
            **result,
            "agent_type": "document_processor"
        }


class WorkflowAgent(BaseAgent):
    """Base class for workflow and process automation agents"""
    
    @abstractmethod
    async def execute_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow process"""
        pass
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process workflow input"""
        workflow_result = await self.execute_workflow(input_data)
        
        return {
            **workflow_result,
            "agent_type": "workflow_processor"
        }


class OrchestratorAgent(BaseAgent):
    """Base class for multi-agent orchestration"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.managed_agents: Dict[str, BaseAgent] = {}
        
    @abstractmethod
    async def coordinate_agents(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple agents for complex tasks"""
        pass
        
    async def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent for orchestration"""
        self.managed_agents[agent.config.id] = agent
        
    async def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent"""
        if agent_id in self.managed_agents:
            await self.managed_agents[agent_id].stop()
            del self.managed_agents[agent_id]
            
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process orchestration input"""
        result = await self.coordinate_agents(input_data)
        
        return {
            **result,
            "agent_type": "orchestrator",
            "managed_agents": list(self.managed_agents.keys())
        }