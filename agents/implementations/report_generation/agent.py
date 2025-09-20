"""
Report Generation Agent - Modular implementation for automated report creation
Converts data into structured reports with templates and analytics
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import logging

from ...core.base import DocumentAgent, AgentConfig
from ...core.communication import Message, MessageType


class ReportFormat(Enum):
    """Supported report output formats"""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    HTML = "html"


class ReportType(Enum):
    """Types of reports that can be generated"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"
    CUSTOM = "custom"


@dataclass
class ReportTemplate:
    """Report template configuration"""
    id: str
    name: str
    type: ReportType
    format: ReportFormat
    sections: List[str]
    required_fields: List[str]
    optional_fields: Optional[List[str]] = None
    styling: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.optional_fields is None:
            self.optional_fields = []
        if self.styling is None:
            self.styling = {}


@dataclass
class ReportRequest:
    """Report generation request"""
    template_id: str
    data_sources: List[str]
    parameters: Dict[str, Any]
    output_format: ReportFormat
    delivery_method: str = "download"
    schedule: Optional[str] = None


class ReportGenerationAgent(DocumentAgent):
    """
    Agent responsible for automated report generation from various data sources.
    Handles document processing, template management, and data aggregation.
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.agent_id = "report_generation"
        self.templates: Dict[str, ReportTemplate] = {}
        self.data_cache: Dict[str, Any] = {}
        self.generation_queue: List[ReportRequest] = []
        self._load_default_templates()
        
    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        """Return agent metadata"""
        return {
            "id": "report_generation",
            "name": "Report Generation Assistant",
            "description": "Automated report creation from data sources with customizable templates",
            "version": "1.0.0",
            "capabilities": [
                "Multi-format report generation",
                "Template management",
                "Data aggregation",
                "Scheduled reporting",
                "Custom styling",
                "Batch processing"
            ],
            "input_types": ["data_query", "template_selection", "format_specification"],
            "output_types": ["pdf_report", "excel_file", "csv_data", "html_report"],
            "tags": ["reporting", "documents", "analytics", "automation"],
            "icon": "📊",
            "color": "green",
            "accuracy": 92.5,
            "avg_response_time": 3.8,
            "success_rate": 96.2,
            "total_requests": 245
        }
    
    def _load_default_templates(self) -> None:
        """Load default report templates"""
        default_templates = [
            ReportTemplate(
                id="financial_summary",
                name="Financial Summary Report",
                type=ReportType.FINANCIAL,
                format=ReportFormat.PDF,
                sections=["executive_summary", "revenue_analysis", "expense_breakdown", "profitability"],
                required_fields=["start_date", "end_date", "department"],
                optional_fields=["comparison_period", "currency"],
                styling={"theme": "professional", "colors": ["#1f77b4", "#ff7f0e"]}
            ),
            ReportTemplate(
                id="operational_dashboard",
                name="Operational Performance Dashboard",
                type=ReportType.OPERATIONAL,
                format=ReportFormat.HTML,
                sections=["kpi_overview", "process_metrics", "resource_utilization", "bottlenecks"],
                required_fields=["metric_types", "time_period"],
                optional_fields=["department_filter", "comparison_baseline"],
                styling={"theme": "modern", "layout": "dashboard"}
            ),
            ReportTemplate(
                id="compliance_audit",
                name="Compliance Audit Report",
                type=ReportType.COMPLIANCE,
                format=ReportFormat.PDF,
                sections=["audit_scope", "findings", "risk_assessment", "recommendations"],
                required_fields=["audit_period", "compliance_framework"],
                optional_fields=["priority_level", "stakeholders"],
                styling={"theme": "formal", "watermark": True}
            )
        ]
        
        for template in default_templates:
            self.templates[template.id] = template
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute report generation task"""
        try:
            task_type = input_data.get("type", "generate_report")
            
            if task_type == "generate_report":
                return await self._generate_report(input_data)
            elif task_type == "list_templates":
                return await self._list_templates()
            elif task_type == "create_template":
                return await self._create_template(input_data)
            elif task_type == "schedule_report":
                return await self._schedule_report(input_data)
            elif task_type == "get_report_status":
                return await self._get_report_status(input_data)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
                
        except Exception as e:
            logging.error(f"Report generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_report(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a report based on the request"""
        template_id = task_data.get("template_id")
        data_sources = task_data.get("data_sources", [])
        parameters = task_data.get("parameters", {})
        output_format = task_data.get("output_format", "pdf")
        
        if not template_id:
            raise ValueError("Template ID is required for report generation")
        
        if template_id not in self.templates:
            raise ValueError(f"Template '{template_id}' not found")
        
        template = self.templates[template_id]
        
        # Validate required fields
        missing_fields = []
        for field in template.required_fields:
            if field not in parameters:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Gather data from sources
        report_data = await self._gather_data(data_sources, parameters)
        
        # Process data according to template
        processed_data = await self._process_data(report_data, template, parameters)
        
        # Generate report content
        report_content = await self._create_report_content(processed_data, template)
        
        # Format output
        formatted_report = await self._format_output(report_content, output_format, template)
        
        return {
            "success": True,
            "report_id": f"report_{datetime.utcnow().timestamp()}",
            "template_id": template_id,
            "output_format": output_format,
            "content": formatted_report,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "data_sources": data_sources,
                "parameters": parameters,
                "sections": template.sections
            },
            "size_kb": len(str(formatted_report)) / 1024
        }
    
    async def _list_templates(self) -> Dict[str, Any]:
        """List available report templates"""
        templates_info = []
        
        for template_id, template in self.templates.items():
            templates_info.append({
                "id": template.id,
                "name": template.name,
                "type": template.type.value,
                "format": template.format.value,
                "sections": template.sections,
                "required_fields": template.required_fields,
                "optional_fields": template.optional_fields
            })
        
        return {
            "success": True,
            "templates": templates_info,
            "total_count": len(templates_info)
        }
    
    async def _create_template(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new report template"""
        template_config = task_data.get("template_config", {})
        
        required_keys = ["id", "name", "type", "format", "sections", "required_fields"]
        missing_keys = [key for key in required_keys if key not in template_config]
        
        if missing_keys:
            raise ValueError(f"Missing required template configuration keys: {missing_keys}")
        
        template = ReportTemplate(
            id=template_config["id"],
            name=template_config["name"],
            type=ReportType(template_config["type"]),
            format=ReportFormat(template_config["format"]),
            sections=template_config["sections"],
            required_fields=template_config["required_fields"],
            optional_fields=template_config.get("optional_fields", []),
            styling=template_config.get("styling", {})
        )
        
        self.templates[template.id] = template
        
        return {
            "success": True,
            "message": f"Template '{template.id}' created successfully",
            "template_id": template.id
        }
    
    async def _schedule_report(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a report for automated generation"""
        schedule_config = task_data.get("schedule_config", {})
        
        schedule_id = f"schedule_{datetime.utcnow().timestamp()}"
        
        # In a real implementation, this would integrate with a job scheduler
        return {
            "success": True,
            "schedule_id": schedule_id,
            "message": "Report scheduled successfully",
            "next_execution": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            "config": schedule_config
        }
    
    async def _get_report_status(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get status of report generation"""
        report_id = task_data.get("report_id")
        
        # In a real implementation, this would check actual report status
        return {
            "success": True,
            "report_id": report_id,
            "status": "completed",
            "progress": 100,
            "estimated_completion": None,
            "download_url": f"/reports/download/{report_id}"
        }
    
    async def _gather_data(self, data_sources: List[str], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Gather data from specified sources"""
        collected_data = {}
        
        for source in data_sources:
            if source == "database":
                # Simulate database query
                collected_data["database"] = await self._query_database(parameters)
            elif source == "api":
                # Simulate API call
                collected_data["api"] = await self._fetch_api_data(parameters)
            elif source == "file":
                # Simulate file reading
                collected_data["file"] = await self._read_file_data(parameters)
            elif source == "cache":
                # Use cached data
                collected_data["cache"] = self.data_cache.get("latest", {})
        
        return collected_data
    
    async def _query_database(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate database query"""
        await asyncio.sleep(0.5)  # Simulate query time
        
        return {
            "records": [
                {"id": 1, "revenue": 150000, "expenses": 85000, "date": "2024-01-01"},
                {"id": 2, "revenue": 180000, "expenses": 92000, "date": "2024-02-01"},
                {"id": 3, "revenue": 165000, "expenses": 88000, "date": "2024-03-01"}
            ],
            "total_records": 3,
            "query_time": 0.5
        }
    
    async def _fetch_api_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate API data fetch"""
        await asyncio.sleep(0.3)  # Simulate API call time
        
        return {
            "metrics": {
                "conversion_rate": 12.5,
                "customer_satisfaction": 4.2,
                "avg_response_time": 1.8
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _read_file_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate file data reading"""
        await asyncio.sleep(0.2)  # Simulate file I/O time
        
        return {
            "file_data": {
                "categories": ["Q1", "Q2", "Q3", "Q4"],
                "values": [125, 168, 142, 189],
                "metadata": {"source": "quarterly_report.csv"}
            }
        }
    
    async def _process_data(self, raw_data: Dict[str, Any], template: ReportTemplate, 
                           parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw data according to template requirements"""
        processed = {
            "summary": {},
            "sections": {},
            "calculations": {},
            "formatting": template.styling
        }
        
        # Calculate summary metrics
        if "database" in raw_data:
            records = raw_data["database"]["records"]
            total_revenue = sum(record["revenue"] for record in records)
            total_expenses = sum(record["expenses"] for record in records)
            
            processed["summary"] = {
                "total_revenue": total_revenue,
                "total_expenses": total_expenses,
                "profit": total_revenue - total_expenses,
                "profit_margin": ((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else 0
            }
        
        # Process sections based on template
        for section in template.sections:
            if section == "executive_summary":
                processed["sections"]["executive_summary"] = self._create_executive_summary(processed["summary"])
            elif section == "revenue_analysis":
                processed["sections"]["revenue_analysis"] = self._create_revenue_analysis(raw_data)
            elif section == "kpi_overview":
                processed["sections"]["kpi_overview"] = self._create_kpi_overview(raw_data)
        
        return processed
    
    def _create_executive_summary(self, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary section"""
        return {
            "title": "Executive Summary",
            "content": f"Financial performance shows total revenue of ${summary_data.get('total_revenue', 0):,} "
                      f"with a profit margin of {summary_data.get('profit_margin', 0):.1f}%.",
            "key_metrics": summary_data
        }
    
    def _create_revenue_analysis(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create revenue analysis section"""
        return {
            "title": "Revenue Analysis",
            "content": "Detailed breakdown of revenue sources and trends.",
            "charts": ["revenue_trend", "source_breakdown"],
            "data": raw_data.get("database", {})
        }
    
    def _create_kpi_overview(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create KPI overview section"""
        return {
            "title": "Key Performance Indicators",
            "content": "Overview of critical performance metrics.",
            "metrics": raw_data.get("api", {}).get("metrics", {}),
            "visualizations": ["gauge_chart", "trend_line"]
        }
    
    async def _create_report_content(self, processed_data: Dict[str, Any], 
                                   template: ReportTemplate) -> Dict[str, Any]:
        """Create the final report content structure"""
        content = {
            "header": {
                "title": template.name,
                "generated_at": datetime.utcnow().isoformat(),
                "template_id": template.id
            },
            "summary": processed_data["summary"],
            "sections": processed_data["sections"],
            "footer": {
                "generated_by": "Report Generation Agent",
                "version": self.get_metadata()["version"]
            }
        }
        
        return content
    
    async def _format_output(self, content: Dict[str, Any], output_format: str, 
                           template: ReportTemplate) -> Union[str, Dict[str, Any]]:
        """Format the report content according to the specified output format"""
        if output_format.lower() == "json":
            return content
        elif output_format.lower() == "html":
            return await self._format_as_html(content, template)
        elif output_format.lower() == "pdf":
            return await self._format_as_pdf_info(content, template)
        elif output_format.lower() == "csv":
            return await self._format_as_csv(content)
        else:
            # Default to JSON
            return content
    
    async def _format_as_html(self, content: Dict[str, Any], template: ReportTemplate) -> str:
        """Format content as HTML"""
        html = f"""
        <html>
        <head>
            <title>{content['header']['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ border-bottom: 2px solid #ccc; padding-bottom: 10px; }}
                .section {{ margin: 20px 0; }}
                .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{content['header']['title']}</h1>
                <p>Generated: {content['header']['generated_at']}</p>
            </div>
            <div class="summary">
                <h2>Summary</h2>
                <pre>{json.dumps(content['summary'], indent=2)}</pre>
            </div>
        """
        
        for section_name, section_data in content["sections"].items():
            html += f"""
            <div class="section">
                <h2>{section_data.get('title', section_name.title())}</h2>
                <p>{section_data.get('content', '')}</p>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    async def _format_as_pdf_info(self, content: Dict[str, Any], template: ReportTemplate) -> Dict[str, Any]:
        """Return PDF generation information (actual PDF generation would require external library)"""
        return {
            "format": "pdf",
            "title": content["header"]["title"],
            "pages": len(content["sections"]) + 2,  # sections + header + summary
            "size_estimate_kb": 250,
            "content_summary": content,
            "note": "PDF generation requires additional libraries (reportlab, weasyprint, etc.)"
        }
    
    async def _format_as_csv(self, content: Dict[str, Any]) -> str:
        """Format content as CSV (simplified)"""
        csv_lines = ["Section,Key,Value"]
        
        # Add summary data
        for key, value in content["summary"].items():
            csv_lines.append(f"Summary,{key},{value}")
        
        # Add section data
        for section_name, section_data in content["sections"].items():
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if isinstance(value, (str, int, float)):
                        csv_lines.append(f"{section_name},{key},{value}")
        
        return "\n".join(csv_lines)
    
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