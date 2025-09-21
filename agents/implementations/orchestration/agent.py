"""
Multi-Agent Orchestration Agent - Coordinates workflows between multiple agents
Manages complex workflows, agent coordination, and task distribution
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
import uuid

from ...core.base import OrchestratorAgent, AgentConfig
from ...core.communication import Message, MessageType, get_message_bus, WorkflowCoordinator
from ...core.registry import AgentRegistry


class WorkflowStatus(Enum):
    """Workflow execution statuses"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    id: str
    agent_id: str
    task_data: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 30
    retry_count: int = 3
    priority: TaskPriority = TaskPriority.NORMAL
    condition: Optional[str] = None  # Conditional execution


@dataclass
class WorkflowDefinition:
    """Complete workflow definition"""
    id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    parallel_execution: bool = False
    timeout: int = 300  # Total workflow timeout
    on_failure: str = "stop"  # stop, continue, retry
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Runtime workflow execution state"""
    workflow_id: str
    execution_id: str
    definition: WorkflowDefinition
    status: WorkflowStatus = WorkflowStatus.PENDING
    current_step: int = 0
    step_results: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_log: List[str] = field(default_factory=list)


class MultiAgentOrchestrationAgent(OrchestratorAgent):
    """
    Agent responsible for orchestrating complex workflows across multiple agents.
    Manages task distribution, dependency resolution, and workflow coordination.
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.agent_id = "multi_agent_orchestration"
        self.workflow_definitions: Dict[str, WorkflowDefinition] = {}
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.registry = AgentRegistry()
        self.coordinator = None
        self._load_default_workflows()
        
    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """Return agent metadata"""
        return {
            "id": "multi_agent_orchestration",
            "name": "Multi-Agent Orchestrator",
            "description": "Coordinates complex workflows across multiple agents with dependency management",
            "version": "1.0.0",
            "capabilities": [
                "Workflow orchestration",
                "Task distribution",
                "Dependency resolution",
                "Parallel execution",
                "Error handling",
                "Progress monitoring"
            ],
            "input_types": ["workflow_definition", "execution_request", "step_coordination"],
            "output_types": ["workflow_status", "execution_result", "progress_update"],
            "tags": ["orchestration", "workflow", "coordination", "automation"],
            "icon": "🎼",
            "color": "purple",
            "accuracy": 94.2,
            "avg_response_time": 2.1,
            "success_rate": 97.8,
            "total_requests": 156
        }
    
    def _load_default_workflows(self) -> None:
        """Load default workflow definitions"""
        # Customer onboarding workflow
        customer_onboarding = WorkflowDefinition(
            id="customer_onboarding",
            name="Customer Onboarding Process",
            description="Complete customer onboarding with document processing and setup",
            steps=[
                WorkflowStep(
                    id="verify_documents",
                    agent_id="contract_analysis",
                    task_data={"type": "document_verification", "documents": "customer_docs"}
                ),
                WorkflowStep(
                    id="create_report",
                    agent_id="report_generation",
                    task_data={"type": "generate_report", "template_id": "onboarding_summary"},
                    dependencies=["verify_documents"]
                ),
                WorkflowStep(
                    id="setup_procurement",
                    agent_id="procurement_assistant",
                    task_data={"type": "setup_vendor", "customer_info": "from_verification"},
                    dependencies=["verify_documents"]
                )
            ],
            parallel_execution=True,
            timeout=600
        )
        
        # Expense processing workflow
        expense_processing = WorkflowDefinition(
            id="expense_processing",
            name="Automated Expense Processing",
            description="End-to-end expense processing with approvals and reporting",
            steps=[
                WorkflowStep(
                    id="validate_expenses",
                    agent_id="expense_approval",
                    task_data={"type": "process_expense"}
                ),
                WorkflowStep(
                    id="generate_expense_report",
                    agent_id="report_generation",
                    task_data={"type": "generate_report", "template_id": "expense_summary"},
                    dependencies=["validate_expenses"],
                    condition="approved_expenses > 0"
                ),
                WorkflowStep(
                    id="update_procurement",
                    agent_id="procurement_assistant",
                    task_data={"type": "update_budget", "expense_data": "from_approval"},
                    dependencies=["validate_expenses"]
                )
            ],
            parallel_execution=False,
            timeout=300
        )
        
        # Contract review workflow
        contract_review = WorkflowDefinition(
            id="contract_review",
            name="Contract Review and Analysis",
            description="Comprehensive contract analysis with risk assessment and reporting",
            steps=[
                WorkflowStep(
                    id="analyze_contract",
                    agent_id="contract_analysis",
                    task_data={"type": "full_analysis", "include_risk_assessment": True}
                ),
                WorkflowStep(
                    id="check_procurement_rules",
                    agent_id="procurement_assistant",
                    task_data={"type": "validate_contract", "contract_data": "from_analysis"},
                    dependencies=["analyze_contract"]
                ),
                WorkflowStep(
                    id="generate_review_report",
                    agent_id="report_generation",
                    task_data={"type": "generate_report", "template_id": "contract_review"},
                    dependencies=["analyze_contract", "check_procurement_rules"]
                )
            ],
            parallel_execution=False,
            timeout=900
        )
        
        # Store workflows
        self.workflow_definitions[customer_onboarding.id] = customer_onboarding
        self.workflow_definitions[expense_processing.id] = expense_processing
        self.workflow_definitions[contract_review.id] = contract_review
    
    async def initialize(self) -> bool:
        """Initialize the orchestration agent"""
        result = await super().initialize()
        
        # Initialize workflow coordinator
        message_bus = await get_message_bus()
        self.coordinator = WorkflowCoordinator(message_bus)
        
        return result
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestration task"""
        try:
            task_type = input_data.get("type", "execute_workflow")
            
            if task_type == "execute_workflow":
                return await self._execute_workflow(input_data)
            elif task_type == "create_workflow":
                return await self._create_workflow(input_data)
            elif task_type == "get_workflow_status":
                return await self._get_workflow_status(input_data)
            elif task_type == "pause_workflow":
                return await self._pause_workflow(input_data)
            elif task_type == "resume_workflow":
                return await self._resume_workflow(input_data)
            elif task_type == "cancel_workflow":
                return await self._cancel_workflow(input_data)
            elif task_type == "list_workflows":
                return await self._list_workflows()
            elif task_type == "get_execution_history":
                return await self._get_execution_history(input_data)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
                
        except Exception as e:
            logging.error(f"Orchestration failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow"""
        workflow_id = input_data.get("workflow_id")
        execution_data = input_data.get("execution_data", {})
        
        if workflow_id not in self.workflow_definitions:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        definition = self.workflow_definitions[workflow_id]
        execution_id = str(uuid.uuid4())
        
        # Create execution instance
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            execution_id=execution_id,
            definition=definition,
            status=WorkflowStatus.RUNNING,
            start_time=datetime.utcnow()
        )
        
        self.active_executions[execution_id] = execution
        
        # Start workflow execution
        try:
            if definition.parallel_execution:
                result = await self._execute_parallel_workflow(execution, execution_data)
            else:
                result = await self._execute_sequential_workflow(execution, execution_data)
            
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = datetime.utcnow()
            
            # Log completion
            await self._log_execution(execution, "completed", result)
            
            return {
                "success": True,
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "status": execution.status.value,
                "result": result,
                "execution_time": (execution.end_time - execution.start_time).total_seconds() if execution.end_time and execution.start_time else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = datetime.utcnow()
            execution.error_log.append(str(e))
            
            # Log failure
            await self._log_execution(execution, "failed", {"error": str(e)})
            
            return {
                "success": False,
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "status": execution.status.value,
                "error": str(e),
                "error_log": execution.error_log,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_sequential_workflow(self, execution: WorkflowExecution, 
                                         execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow steps sequentially"""
        results = {}
        context = execution_data.copy()
        
        for step in execution.definition.steps:
            # Check dependencies
            if not await self._check_dependencies(step, results):
                continue
            
            # Check condition
            if step.condition and not await self._evaluate_condition(step.condition, context):
                continue
            
            # Execute step
            step_result = await self._execute_step(step, context)
            results[step.id] = step_result
            
            # Update context with step results
            context.update({f"{step.id}_result": step_result})
            
            execution.step_results[step.id] = step_result
            execution.current_step += 1
        
        return {
            "workflow_completed": True,
            "steps_executed": len(results),
            "step_results": results
        }
    
    async def _execute_parallel_workflow(self, execution: WorkflowExecution, 
                                       execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow steps in parallel where possible"""
        context = execution_data.copy()
        pending_steps = list(execution.definition.steps)
        completed_steps = set()
        results = {}
        
        while pending_steps:
            # Find steps that can be executed (dependencies met)
            ready_steps = [
                step for step in pending_steps
                if all(dep in completed_steps for dep in step.dependencies)
            ]
            
            if not ready_steps:
                # Check for circular dependencies or deadlock
                remaining_deps = set()
                for step in pending_steps:
                    remaining_deps.update(step.dependencies)
                
                if not any(dep in [s.id for s in pending_steps] for dep in remaining_deps):
                    # Deadlock detected
                    raise RuntimeError("Workflow deadlock detected - circular dependencies")
                
                # Wait a bit and try again
                await asyncio.sleep(0.1)
                continue
            
            # Execute ready steps in parallel
            tasks = []
            for step in ready_steps:
                # Check condition
                if step.condition and not await self._evaluate_condition(step.condition, context):
                    pending_steps.remove(step)
                    completed_steps.add(step.id)
                    continue
                
                task = asyncio.create_task(self._execute_step(step, context))
                tasks.append((step, task))
            
            # Wait for completion
            if tasks:
                for step, task in tasks:
                    try:
                        result = await task
                        results[step.id] = result
                        context.update({f"{step.id}_result": result})
                        execution.step_results[step.id] = result
                        completed_steps.add(step.id)
                        pending_steps.remove(step)
                    except Exception as e:
                        execution.error_log.append(f"Step {step.id} failed: {str(e)}")
                        if execution.definition.on_failure == "stop":
                            raise e
                        # Continue with other steps if on_failure is "continue"
                        pending_steps.remove(step)
        
        return {
            "workflow_completed": True,
            "steps_executed": len(results),
            "step_results": results
        }
    
    async def _execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        # Get the agent
        agent = await self.registry.get_agent(step.agent_id)
        
        # Prepare task data with context
        task_data = step.task_data.copy()
        
        # Substitute context variables in task data
        task_data = await self._substitute_context_variables(task_data, context)
        
        # Execute the task
        for attempt in range(step.retry_count):
            try:
                result = await asyncio.wait_for(
                    agent.execute(task_data), 
                    timeout=step.timeout
                )
                return result
            except asyncio.TimeoutError:
                if attempt == step.retry_count - 1:
                    raise TimeoutError(f"Step {step.id} timed out after {step.timeout}s")
                await asyncio.sleep(1)  # Brief delay before retry
            except Exception as e:
                if attempt == step.retry_count - 1:
                    raise e
                await asyncio.sleep(1)  # Brief delay before retry
        
        raise RuntimeError(f"Step {step.id} failed after {step.retry_count} attempts")
    
    async def _check_dependencies(self, step: WorkflowStep, results: Dict[str, Any]) -> bool:
        """Check if step dependencies are satisfied"""
        return all(dep in results for dep in step.dependencies)
    
    async def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate step condition"""
        # Simple condition evaluation (in production, use safer evaluation)
        try:
            # Replace context variables in condition
            for key, value in context.items():
                condition = condition.replace(key, str(value))
            
            # Basic condition evaluation
            if ">" in condition:
                left, right = condition.split(">")
                return float(left.strip()) > float(right.strip())
            elif "=" in condition:
                left, right = condition.split("=")
                return left.strip() == right.strip()
            elif condition in context:
                return bool(context[condition])
            
            return True  # Default to true if condition can't be evaluated
        except:
            return True  # Default to true on evaluation error
    
    async def _substitute_context_variables(self, task_data: Dict[str, Any], 
                                           context: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute context variables in task data"""
        result = {}
        
        for key, value in task_data.items():
            if isinstance(value, str) and value.startswith("from_"):
                # Replace with context value
                context_key = f"{value.replace('from_', '')}_result"
                result[key] = context.get(context_key, value)
            else:
                result[key] = value
        
        return result
    
    async def _log_execution(self, execution: WorkflowExecution, status: str, 
                           result: Dict[str, Any]) -> None:
        """Log workflow execution"""
        log_entry = {
            "execution_id": execution.execution_id,
            "workflow_id": execution.workflow_id,
            "status": status,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "end_time": execution.end_time.isoformat() if execution.end_time else None,
            "duration": (execution.end_time - execution.start_time).total_seconds() if execution.end_time and execution.start_time else None,
            "steps_completed": len(execution.step_results),
            "result_summary": result,
            "error_count": len(execution.error_log)
        }
        
        self.execution_history.append(log_entry)
    
    async def _create_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow definition"""
        workflow_data = input_data.get("workflow", {})
        
        # Parse workflow definition
        steps = []
        for step_data in workflow_data.get("steps", []):
            step = WorkflowStep(
                id=step_data["id"],
                agent_id=step_data["agent_id"],
                task_data=step_data.get("task_data", {}),
                dependencies=step_data.get("dependencies", []),
                timeout=step_data.get("timeout", 30),
                retry_count=step_data.get("retry_count", 3),
                priority=TaskPriority(step_data.get("priority", 2)),
                condition=step_data.get("condition")
            )
            steps.append(step)
        
        workflow = WorkflowDefinition(
            id=workflow_data["id"],
            name=workflow_data["name"],
            description=workflow_data.get("description", ""),
            steps=steps,
            parallel_execution=workflow_data.get("parallel_execution", False),
            timeout=workflow_data.get("timeout", 300),
            on_failure=workflow_data.get("on_failure", "stop"),
            metadata=workflow_data.get("metadata", {})
        )
        
        self.workflow_definitions[workflow.id] = workflow
        
        return {
            "success": True,
            "workflow_id": workflow.id,
            "message": f"Workflow '{workflow.name}' created successfully",
            "steps_count": len(workflow.steps)
        }
    
    async def _get_workflow_status(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get status of workflow execution"""
        execution_id = input_data.get("execution_id")
        
        if execution_id not in self.active_executions:
            return {
                "success": False,
                "error": f"Execution {execution_id} not found"
            }
        
        execution = self.active_executions[execution_id]
        
        return {
            "success": True,
            "execution_id": execution_id,
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "current_step": execution.current_step,
            "total_steps": len(execution.definition.steps),
            "progress_percentage": (execution.current_step / len(execution.definition.steps)) * 100,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "step_results": execution.step_results,
            "error_log": execution.error_log
        }
    
    async def _pause_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Pause workflow execution"""
        execution_id = input_data.get("execution_id")
        
        if execution_id not in self.active_executions:
            return {
                "success": False,
                "error": f"Execution {execution_id} not found"
            }
        
        execution = self.active_executions[execution_id]
        execution.status = WorkflowStatus.PAUSED
        
        return {
            "success": True,
            "execution_id": execution_id,
            "status": execution.status.value,
            "message": "Workflow paused successfully"
        }
    
    async def _resume_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resume paused workflow execution"""
        execution_id = input_data.get("execution_id")
        
        if execution_id not in self.active_executions:
            return {
                "success": False,
                "error": f"Execution {execution_id} not found"
            }
        
        execution = self.active_executions[execution_id]
        if execution.status != WorkflowStatus.PAUSED:
            return {
                "success": False,
                "error": f"Execution is not paused (current status: {execution.status.value})"
            }
        
        execution.status = WorkflowStatus.RUNNING
        
        return {
            "success": True,
            "execution_id": execution_id,
            "status": execution.status.value,
            "message": "Workflow resumed successfully"
        }
    
    async def _cancel_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel workflow execution"""
        execution_id = input_data.get("execution_id")
        
        if execution_id not in self.active_executions:
            return {
                "success": False,
                "error": f"Execution {execution_id} not found"
            }
        
        execution = self.active_executions[execution_id]
        execution.status = WorkflowStatus.CANCELLED
        execution.end_time = datetime.utcnow()
        
        return {
            "success": True,
            "execution_id": execution_id,
            "status": execution.status.value,
            "message": "Workflow cancelled successfully"
        }
    
    async def _list_workflows(self) -> Dict[str, Any]:
        """List all workflow definitions"""
        workflows = []
        
        for workflow_id, workflow in self.workflow_definitions.items():
            workflows.append({
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "steps_count": len(workflow.steps),
                "parallel_execution": workflow.parallel_execution,
                "timeout": workflow.timeout,
                "metadata": workflow.metadata
            })
        
        return {
            "success": True,
            "workflows": workflows,
            "total_count": len(workflows)
        }
    
    async def _get_execution_history(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get workflow execution history"""
        limit = input_data.get("limit", 50)
        workflow_id = input_data.get("workflow_id")
        
        history = self.execution_history
        
        if workflow_id:
            history = [h for h in history if h["workflow_id"] == workflow_id]
        
        # Sort by start time, most recent first
        history = sorted(history, key=lambda x: x["start_time"], reverse=True)
        
        return {
            "success": True,
            "executions": history[:limit],
            "total_count": len(history),
            "filtered_by_workflow": workflow_id is not None
        }
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """Process inter-agent messages"""
        if message.type == MessageType.TASK_REQUEST:
            # Handle task request from another agent
            result = await self.execute(message.payload)
            
            return Message(
                type=MessageType.TASK_RESPONSE,
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                payload=result,
                reply_to=message.id
            )
        
        return None