"""
Inter-Agent Communication System - Message passing and coordination between agents
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Callable, Awaitable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class MessageType(Enum):
    """Message types for agent communication"""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    ERROR_REPORT = "error_report"
    HEARTBEAT = "heartbeat"
    SHUTDOWN = "shutdown"
    COORDINATION = "coordination"


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Message:
    """Inter-agent message structure"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.TASK_REQUEST
    priority: MessagePriority = MessagePriority.NORMAL
    sender_id: str = ""
    recipient_id: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reply_to: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "priority": self.priority.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "reply_to": self.reply_to,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        msg = cls()
        msg.id = data["id"]
        msg.type = MessageType(data["type"])
        msg.priority = MessagePriority(data["priority"])
        msg.sender_id = data["sender_id"]
        msg.recipient_id = data["recipient_id"]
        msg.payload = data["payload"]
        msg.timestamp = datetime.fromisoformat(data["timestamp"])
        msg.reply_to = data.get("reply_to")
        if data.get("expires_at"):
            msg.expires_at = datetime.fromisoformat(data["expires_at"])
        return msg


class MessageBus:
    """Central message bus for agent communication"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Message], Awaitable[None]]]] = {}
        self.message_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.running = False
        self.processor_task: Optional[asyncio.Task] = None
        
    async def start(self) -> None:
        """Start the message bus"""
        if self.running:
            return
            
        self.running = True
        self.processor_task = asyncio.create_task(self._process_messages())
        
    async def stop(self) -> None:
        """Stop the message bus"""
        self.running = False
        if self.processor_task:
            self.processor_task.cancel()
            try:
                await self.processor_task
            except asyncio.CancelledError:
                pass
                
    async def _process_messages(self) -> None:
        """Process messages from the queue"""
        while self.running:
            try:
                # Get next message (priority, timestamp, message)
                priority, timestamp, message = await asyncio.wait_for(
                    self.message_queue.get(), timeout=1.0
                )
                
                await self._deliver_message(message)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                
    async def _deliver_message(self, message: Message) -> None:
        """Deliver message to subscribers"""
        recipient_id = message.recipient_id
        
        if recipient_id in self.subscribers:
            # Deliver to specific recipient
            subscribers = self.subscribers[recipient_id]
        elif "*" in self.subscribers:
            # Deliver to broadcast subscribers
            subscribers = self.subscribers["*"]
        else:
            # No subscribers found
            return
            
        # Deliver message to all subscribers
        for callback in subscribers:
            try:
                await callback(message)
            except Exception as e:
                print(f"Error delivering message to subscriber: {e}")
                
    async def send_message(self, message: Message) -> None:
        """Send a message through the bus"""
        # Check if message has expired
        if message.expires_at and datetime.utcnow() > message.expires_at:
            return
            
        # Add to priority queue
        # Lower priority number = higher priority
        priority = (4 - message.priority.value, message.timestamp)
        await self.message_queue.put((priority, message.timestamp, message))
        
    def subscribe(self, agent_id: str, callback: Callable[[Message], Awaitable[None]]) -> None:
        """Subscribe an agent to receive messages"""
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(callback)
        
    def unsubscribe(self, agent_id: str, callback: Optional[Callable[[Message], Awaitable[None]]] = None) -> None:
        """Unsubscribe from messages"""
        if agent_id not in self.subscribers:
            return
            
        if callback:
            # Remove specific callback
            if callback in self.subscribers[agent_id]:
                self.subscribers[agent_id].remove(callback)
        else:
            # Remove all callbacks for agent
            del self.subscribers[agent_id]


class AgentCommunicator:
    """Communication interface for individual agents"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.pending_requests: Dict[str, asyncio.Future] = {}
        
    async def initialize(self) -> None:
        """Initialize communication for this agent"""
        # Subscribe to messages for this agent
        self.message_bus.subscribe(self.agent_id, self._handle_message)
        
    async def _handle_message(self, message: Message) -> None:
        """Handle incoming messages"""
        if message.reply_to and message.reply_to in self.pending_requests:
            # This is a response to a previous request
            future = self.pending_requests[message.reply_to]
            if not future.done():
                future.set_result(message)
                
    async def send_request(self, recipient_id: str, request_data: Dict[str, Any],
                          timeout: float = 30.0) -> Message:
        """Send a request and wait for response"""
        request_msg = Message(
            type=MessageType.TASK_REQUEST,
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            payload=request_data
        )
        
        # Create future for response
        response_future = asyncio.Future()
        self.pending_requests[request_msg.id] = response_future
        
        try:
            # Send request
            await self.message_bus.send_message(request_msg)
            
            # Wait for response
            response = await asyncio.wait_for(response_future, timeout=timeout)
            return response
            
        finally:
            # Cleanup
            if request_msg.id in self.pending_requests:
                del self.pending_requests[request_msg.id]
                
    async def send_response(self, request_message: Message, 
                           response_data: Dict[str, Any]) -> None:
        """Send a response to a request"""
        response_msg = Message(
            type=MessageType.TASK_RESPONSE,
            sender_id=self.agent_id,
            recipient_id=request_message.sender_id,
            payload=response_data,
            reply_to=request_message.id
        )
        
        await self.message_bus.send_message(response_msg)
        
    async def broadcast_status(self, status_data: Dict[str, Any]) -> None:
        """Broadcast status update to all agents"""
        status_msg = Message(
            type=MessageType.STATUS_UPDATE,
            sender_id=self.agent_id,
            recipient_id="*",  # Broadcast
            payload=status_data
        )
        
        await self.message_bus.send_message(status_msg)
        
    async def report_error(self, error_data: Dict[str, Any]) -> None:
        """Report an error to the system"""
        error_msg = Message(
            type=MessageType.ERROR_REPORT,
            priority=MessagePriority.HIGH,
            sender_id=self.agent_id,
            recipient_id="system",
            payload=error_data
        )
        
        await self.message_bus.send_message(error_msg)
        
    async def send_heartbeat(self) -> None:
        """Send heartbeat to indicate agent is alive"""
        heartbeat_msg = Message(
            type=MessageType.HEARTBEAT,
            priority=MessagePriority.LOW,
            sender_id=self.agent_id,
            recipient_id="system",
            payload={"status": "alive", "timestamp": datetime.utcnow().isoformat()}
        )
        
        await self.message_bus.send_message(heartbeat_msg)
        
    def cleanup(self) -> None:
        """Clean up communication resources"""
        self.message_bus.unsubscribe(self.agent_id)
        
        # Cancel pending requests
        for future in self.pending_requests.values():
            if not future.done():
                future.cancel()
        self.pending_requests.clear()


class WorkflowCoordinator:
    """Coordinates workflows between multiple agents"""
    
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        
    async def start_workflow(self, workflow_id: str, workflow_config: Dict[str, Any]) -> str:
        """Start a multi-agent workflow"""
        workflow = {
            "id": workflow_id,
            "config": workflow_config,
            "status": "running",
            "started_at": datetime.utcnow(),
            "steps": workflow_config.get("steps", []),
            "current_step": 0,
            "results": {}
        }
        
        self.active_workflows[workflow_id] = workflow
        
        # Start executing steps
        await self._execute_next_step(workflow_id)
        
        return workflow_id
        
    async def _execute_next_step(self, workflow_id: str) -> None:
        """Execute the next step in a workflow"""
        workflow = self.active_workflows[workflow_id]
        steps = workflow["steps"]
        current_step = workflow["current_step"]
        
        if current_step >= len(steps):
            # Workflow completed
            workflow["status"] = "completed"
            workflow["completed_at"] = datetime.utcnow()
            return
            
        step = steps[current_step]
        agent_id = step["agent_id"]
        task_data = step["task_data"]
        
        # Send task to agent
        task_msg = Message(
            type=MessageType.TASK_REQUEST,
            sender_id="workflow_coordinator",
            recipient_id=agent_id,
            payload={
                "workflow_id": workflow_id,
                "step_id": current_step,
                "task_data": task_data
            }
        )
        
        await self.message_bus.send_message(task_msg)
        
    async def handle_step_completion(self, workflow_id: str, step_id: int, 
                                   result: Dict[str, Any]) -> None:
        """Handle completion of a workflow step"""
        if workflow_id not in self.active_workflows:
            return
            
        workflow = self.active_workflows[workflow_id]
        workflow["results"][step_id] = result
        workflow["current_step"] += 1
        
        # Execute next step
        await self._execute_next_step(workflow_id)
        
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow"""
        return self.active_workflows.get(workflow_id)


# Global message bus instance
_message_bus: Optional[MessageBus] = None


async def get_message_bus() -> MessageBus:
    """Get the global message bus instance"""
    global _message_bus
    if _message_bus is None:
        _message_bus = MessageBus()
        await _message_bus.start()
    return _message_bus


async def cleanup_communication() -> None:
    """Clean up communication system"""
    global _message_bus
    if _message_bus:
        await _message_bus.stop()
        _message_bus = None