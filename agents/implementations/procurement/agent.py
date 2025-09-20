"""
Procurement Assistant Agent - Conversational AI for vendor inquiries and procurement guidance

Converted from Frontend/AIAgents.jsx to modular architecture
"""

import asyncio
from typing import Dict, Any, Optional, List
import openai
from datetime import datetime

from ...core.base import (
    ConversationalAgent, 
    AgentConfig, 
    AgentCategory, 
    AgentStatus,
    AgentMetrics,
    BusinessImpact,
    TechnicalSpec
)


class ProcurementAgent(ConversationalAgent):
    """
    Intelligent chatbot for automating vendor inquiries and procurement process guidance
    
    Features:
    - Natural language query processing
    - Document retrieval and search
    - Process workflow guidance  
    - Multi-language support
    - Integration with procurement systems
    - Escalation to human agents
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.openai_client = None
        self.vector_db_client = None
        self.procurement_knowledge_base = []
        self.escalation_threshold = 0.7  # Confidence threshold for human escalation
        
    async def initialize(self) -> bool:
        """Initialize the procurement assistant with required services"""
        try:
            # Initialize OpenAI client
            # In production, get API key from environment/config
            # self.openai_client = openai.AsyncOpenAI(api_key="your-api-key")
            
            # Initialize vector database (Pinecone)
            # In production, connect to actual Pinecone instance
            # self.vector_db_client = PineconeClient(...)
            
            # Load procurement knowledge base
            await self._load_knowledge_base()
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize ProcurementAgent: {e}")
            return False
            
    async def _load_knowledge_base(self) -> None:
        """Load procurement processes and vendor information"""
        # In production, this would load from actual data sources
        self.procurement_knowledge_base = [
            {
                "topic": "vendor_approval_process",
                "content": "Vendor approval requires: 1) Business registration, 2) Insurance certificates, 3) Reference checks, 4) Financial verification",
                "keywords": ["vendor", "approval", "registration", "insurance"]
            },
            {
                "topic": "purchase_order_workflow", 
                "content": "Purchase orders follow: 1) Request approval, 2) Budget verification, 3) Vendor selection, 4) PO generation, 5) Delivery tracking",
                "keywords": ["purchase order", "PO", "workflow", "approval"]
            },
            {
                "topic": "contract_negotiation",
                "content": "Contract negotiations include: pricing terms, delivery schedules, quality standards, payment terms, and termination clauses",
                "keywords": ["contract", "negotiation", "pricing", "terms"]
            }
        ]
        
    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a natural language procurement query"""
        context = context or {}
        
        # Retrieve relevant knowledge
        relevant_docs = await self._retrieve_documents(query)
        
        # Generate response using LLM
        response = await self._generate_response(query, relevant_docs, context)
        
        # Check if escalation is needed
        if await self._should_escalate(query, response):
            response = await self._handle_escalation(query, response)
            
        return response
        
    async def _retrieve_documents(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents from knowledge base"""
        # Simple keyword matching for demo - in production use vector search
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.procurement_knowledge_base:
            score = sum(1 for keyword in doc["keywords"] if keyword in query_lower)
            if score > 0:
                relevant_docs.append({**doc, "relevance_score": score})
                
        # Sort by relevance
        relevant_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_docs[:3]  # Top 3 most relevant
        
    async def _generate_response(self, query: str, docs: List[Dict[str, Any]], 
                                context: Dict[str, Any]) -> str:
        """Generate response using OpenAI GPT-4"""
        
        # Build context from retrieved documents
        doc_context = "\n".join([
            f"- {doc['topic']}: {doc['content']}" 
            for doc in docs
        ])
        
        # In production, use actual OpenAI API
        system_prompt = """You are a helpful procurement assistant. Use the provided context to answer questions about vendor management, purchase orders, and procurement processes. If you don't have enough information, say so and suggest contacting the procurement team."""
        
        user_prompt = f"""
        Query: {query}
        
        Relevant Information:
        {doc_context}
        
        Additional Context: {context.get('additional_info', 'None')}
        
        Please provide a helpful response:
        """
        
        # Mock response for demo - replace with actual OpenAI call
        if "vendor approval" in query.lower():
            return "To get vendor approval, you'll need to submit: 1) Business registration documents, 2) Insurance certificates, 3) Three business references, and 4) Financial verification. The approval process typically takes 5-7 business days. Would you like me to send you the vendor application form?"
            
        elif "purchase order" in query.lower() or "po" in query.lower():
            return "The purchase order process involves several steps: request approval, budget verification, vendor selection, PO generation, and delivery tracking. Each PO requires manager approval for amounts over $1,000. What specific aspect of the PO process would you like help with?"
            
        elif "contract" in query.lower():
            return "Contract negotiations typically cover pricing terms, delivery schedules, quality standards, payment terms, and termination clauses. All contracts over $10,000 require legal review. Would you like me to connect you with our contracts team?"
            
        else:
            return f"I understand you're asking about: {query}. While I don't have specific information on this topic, I can connect you with our procurement specialists who can provide detailed assistance. Would you like me to create a support ticket?"
            
    async def _should_escalate(self, query: str, response: str) -> bool:
        """Determine if the query should be escalated to human agents"""
        
        # Escalation triggers
        escalation_keywords = [
            "urgent", "emergency", "complaint", "legal", "dispute", 
            "contract issue", "payment problem", "quality issue"
        ]
        
        # Check for escalation keywords
        query_lower = query.lower()
        for keyword in escalation_keywords:
            if keyword in query_lower:
                return True
                
        # Check if response indicates uncertainty
        uncertainty_phrases = [
            "i don't have", "not sure", "contact", "specialist", 
            "support ticket", "human agent"
        ]
        
        response_lower = response.lower()
        for phrase in uncertainty_phrases:
            if phrase in response_lower:
                return True
                
        return False
        
    async def _handle_escalation(self, query: str, response: str) -> str:
        """Handle escalation to human agents"""
        escalation_note = "\n\n🔄 **Escalation Notice**: This query has been flagged for human review. A procurement specialist will contact you within 2 hours during business hours."
        
        # In production, create actual support ticket
        await self._create_support_ticket(query, response)
        
        return response + escalation_note
        
    async def _create_support_ticket(self, query: str, ai_response: str) -> str:
        """Create a support ticket for human follow-up"""
        ticket_id = f"PROC-{datetime.now().strftime('%Y%m%d')}-{hash(query) % 10000:04d}"
        
        # In production, integrate with actual ticketing system
        ticket_data = {
            "id": ticket_id,
            "type": "procurement_inquiry",
            "priority": "normal",
            "query": query,
            "ai_response": ai_response,
            "created_at": datetime.now().isoformat(),
            "status": "open"
        }
        
        # Mock ticket creation
        print(f"Support ticket created: {ticket_id}")
        
        return ticket_id
        
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for procurement queries"""
        required_fields = ["query"]
        
        for field in required_fields:
            if field not in input_data:
                return False
                
        # Validate query is a string and not empty
        query = input_data["query"]
        if not isinstance(query, str) or len(query.strip()) == 0:
            return False
            
        # Check query length (prevent abuse)
        if len(query) > 1000:
            return False
            
        return True
        
    async def cleanup(self) -> None:
        """Clean up resources"""
        if self.openai_client:
            await self.openai_client.close()
            
        if self.vector_db_client:
            # Close vector DB connections
            pass
            
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return [
            "Natural language query processing",
            "Document retrieval and search", 
            "Process workflow guidance",
            "Multi-language support",
            "Integration with procurement systems",
            "Escalation to human agents"
        ]
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get current agent metrics"""
        return {
            "accuracy": 92,
            "response_time": "< 2 seconds",
            "satisfaction": 88,
            "automation": 75
        }
        
    def get_business_impact(self) -> Dict[str, Any]:
        """Get business impact metrics"""
        return {
            "primary": "60% faster response times",
            "metrics": [
                "24/7 availability",
                "75% query automation", 
                "40 hours weekly time savings",
                "Improved vendor satisfaction"
            ]
        }


def create_procurement_agent_config() -> AgentConfig:
    """Factory function to create procurement agent configuration"""
    return AgentConfig(
        id="procurement_assistant",
        title="Procurement Assistant Chatbot",
        category=AgentCategory.CONVERSATIONAL_AI,
        description="Intelligent chatbot automating vendor inquiries and procurement process guidance with natural language processing and document retrieval capabilities.",
        purpose="Reduce response times for vendor inquiries and provide 24/7 support for procurement processes, freeing up human resources for strategic tasks.",
        capabilities=[
            "Natural language query processing",
            "Document retrieval and search",
            "Process workflow guidance", 
            "Multi-language support",
            "Integration with procurement systems",
            "Escalation to human agents"
        ],
        technologies=["OpenAI GPT-4", "LangChain", "React", "Node.js", "Pinecone", "Docker"],
        status=AgentStatus.READY,
        year="2024",
        complexity="High",
        technical_details=TechnicalSpec(
            llm="OpenAI GPT-4",
            framework="LangChain", 
            vector_db="Pinecone",
            deployment="Docker + Kubernetes",
            integration="REST APIs"
        ),
        metrics=AgentMetrics(
            accuracy=92.0,
            response_time="< 2 seconds",
            satisfaction=88.0,
            automation_rate=75.0
        ),
        business_impact=BusinessImpact(
            primary_metric="60% faster response times",
            secondary_metrics=[
                "24/7 availability",
                "75% query automation",
                "40 hours weekly time savings", 
                "Improved vendor satisfaction"
            ]
        )
    )


# Factory function for easy agent creation
async def create_procurement_agent() -> ProcurementAgent:
    """Create and initialize a procurement agent instance"""
    config = create_procurement_agent_config()
    agent = ProcurementAgent(config)
    await agent.start()
    return agent