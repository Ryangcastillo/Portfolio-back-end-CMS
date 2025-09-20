"""
Agent Monitoring - Performance tracking and health monitoring for AI agents
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json


@dataclass
class AgentMetric:
    """Single metric measurement"""
    timestamp: datetime
    agent_id: str
    metric_type: str
    value: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass  
class PerformanceSnapshot:
    """Performance snapshot for an agent"""
    agent_id: str
    timestamp: datetime
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    response_time: Optional[float] = None
    success_rate: Optional[float] = None
    error_count: int = 0
    request_count: int = 0


class AgentMonitor:
    """Monitor agent performance and health"""
    
    def __init__(self, max_metrics: int = 1000):
        self.metrics: List[AgentMetric] = []
        self.performance_data: Dict[str, List[PerformanceSnapshot]] = {}
        self.max_metrics = max_metrics
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
    async def start_monitoring(self, agent) -> None:
        """Start monitoring an agent"""
        agent_id = agent.config.id
        
        if agent_id in self.monitoring_tasks:
            return
            
        # Start background monitoring task
        task = asyncio.create_task(self._monitor_agent(agent))
        self.monitoring_tasks[agent_id] = task
        
    async def stop_monitoring(self, agent_id: str) -> None:
        """Stop monitoring an agent"""
        if agent_id in self.monitoring_tasks:
            task = self.monitoring_tasks[agent_id]
            task.cancel()
            del self.monitoring_tasks[agent_id]
            
    async def _monitor_agent(self, agent) -> None:
        """Background monitoring loop for an agent"""
        agent_id = agent.config.id
        
        while True:
            try:
                # Collect performance metrics
                snapshot = await self._collect_metrics(agent)
                
                # Store snapshot
                if agent_id not in self.performance_data:
                    self.performance_data[agent_id] = []
                    
                self.performance_data[agent_id].append(snapshot)
                
                # Keep only recent data
                cutoff = datetime.utcnow() - timedelta(hours=24)
                self.performance_data[agent_id] = [
                    s for s in self.performance_data[agent_id] 
                    if s.timestamp > cutoff
                ]
                
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                await self.record_metric(
                    agent_id, "monitoring_error", str(e)
                )
                await asyncio.sleep(60)  # Back off on errors
                
    async def _collect_metrics(self, agent) -> PerformanceSnapshot:
        """Collect current performance metrics for an agent"""
        return PerformanceSnapshot(
            agent_id=agent.config.id,
            timestamp=datetime.utcnow(),
            # Add actual metric collection here
            cpu_usage=0.0,
            memory_usage=0.0,
            response_time=0.0,
            success_rate=100.0
        )
        
    async def record_metric(self, agent_id: str, metric_type: str, 
                           value: Any, metadata: Dict[str, Any] = None) -> None:
        """Record a custom metric"""
        metric = AgentMetric(
            timestamp=datetime.utcnow(),
            agent_id=agent_id,
            metric_type=metric_type,
            value=value,
            metadata=metadata or {}
        )
        
        self.metrics.append(metric)
        
        # Keep metrics list bounded
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
            
    async def get_agent_metrics(self, agent_id: str, 
                               hours: int = 1) -> Dict[str, Any]:
        """Get recent metrics for an agent"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        # Filter metrics
        agent_metrics = [
            m for m in self.metrics 
            if m.agent_id == agent_id and m.timestamp > cutoff
        ]
        
        # Filter performance data
        performance_snapshots = []
        if agent_id in self.performance_data:
            performance_snapshots = [
                s for s in self.performance_data[agent_id]
                if s.timestamp > cutoff
            ]
            
        return {
            "agent_id": agent_id,
            "timeframe_hours": hours,
            "metric_count": len(agent_metrics),
            "performance_snapshots": len(performance_snapshots),
            "latest_metrics": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "type": m.metric_type,
                    "value": m.value,
                    "metadata": m.metadata
                }
                for m in agent_metrics[-10:]  # Last 10 metrics
            ],
            "performance_summary": await self._summarize_performance(
                performance_snapshots
            )
        }
        
    async def _summarize_performance(self, snapshots: List[PerformanceSnapshot]) -> Dict[str, Any]:
        """Summarize performance data"""
        if not snapshots:
            return {}
            
        response_times = [s.response_time for s in snapshots if s.response_time]
        success_rates = [s.success_rate for s in snapshots if s.success_rate]
        
        return {
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "avg_success_rate": sum(success_rates) / len(success_rates) if success_rates else 0,
            "total_requests": sum(s.request_count for s in snapshots),
            "total_errors": sum(s.error_count for s in snapshots),
            "uptime_percentage": len([s for s in snapshots if s.success_rate and s.success_rate > 0]) / len(snapshots) * 100
        }
        
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        active_agents = len(self.monitoring_tasks)
        total_metrics = len(self.metrics)
        
        # Calculate system-wide metrics
        recent_errors = len([
            m for m in self.metrics 
            if m.metric_type.endswith('_error') and 
            m.timestamp > datetime.utcnow() - timedelta(minutes=15)
        ])
        
        return {
            "status": "healthy" if recent_errors < 10 else "degraded",
            "active_agents": active_agents,
            "total_metrics": total_metrics,
            "recent_errors": recent_errors,
            "monitoring_uptime": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    async def shutdown(self) -> None:
        """Shutdown monitoring system"""
        # Cancel all monitoring tasks
        for task in self.monitoring_tasks.values():
            task.cancel()
            
        # Wait for tasks to complete
        if self.monitoring_tasks:
            await asyncio.gather(
                *self.monitoring_tasks.values(),
                return_exceptions=True
            )
            
        self.monitoring_tasks.clear()
        
    def export_metrics(self, agent_id: Optional[str] = None) -> str:
        """Export metrics to JSON string"""
        if agent_id:
            metrics_to_export = [
                m for m in self.metrics if m.agent_id == agent_id
            ]
        else:
            metrics_to_export = self.metrics
            
        export_data = []
        for metric in metrics_to_export:
            export_data.append({
                "timestamp": metric.timestamp.isoformat(),
                "agent_id": metric.agent_id,
                "metric_type": metric.metric_type,
                "value": metric.value,
                "metadata": metric.metadata
            })
            
        return json.dumps(export_data, indent=2)