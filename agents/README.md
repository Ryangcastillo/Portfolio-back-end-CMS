# 🤖 Modular AI Agents System

A comprehensive, modular AI agent architecture designed for reusability across projects and platforms.

## 📁 Directory Structure

```
agents/
├── core/                    # Core agent infrastructure
│   ├── base.py             # Base agent class and interfaces
│   ├── registry.py         # Agent discovery and management
│   ├── communication.py    # Inter-agent messaging
│   └── lifecycle.py        # Agent lifecycle management
├── implementations/         # Concrete agent implementations
│   ├── procurement/        # Procurement Assistant Agent
│   ├── reporting/          # Report Generation Agent
│   ├── expense/            # Expense Approval Agent
│   ├── orchestration/      # Multi-Agent Orchestration
│   └── contract/           # Contract Analysis Agent
├── config/                 # Configuration management
│   ├── agents.yaml         # Agent configurations
│   ├── providers.yaml      # LLM provider settings
│   └── environments.yaml   # Environment-specific configs
├── utils/                  # Shared utilities
│   ├── llm_providers.py   # LLM integrations
│   ├── vector_db.py       # Vector database utilities
│   ├── monitoring.py      # Performance monitoring
│   └── security.py        # Security utilities
├── types/                  # TypeScript/Python type definitions
│   ├── agent.types.ts     # Agent interface definitions
│   ├── message.types.ts   # Message passing types
│   └── config.types.ts    # Configuration types
└── examples/              # Usage examples and integration guides
    ├── node-integration.js # Node.js integration example
    ├── python-usage.py    # Python usage example
    └── api-integration.md # API integration guide
```

## 🚀 Key Features

### **Cross-Platform Compatibility**
- **Python Backend**: Full agent implementations with async support
- **Node.js/TypeScript**: JavaScript bindings and API integrations
- **REST API**: HTTP endpoints for any language/platform
- **Docker**: Containerized deployments for any environment

### **Modular Design**
- **Plugin Architecture**: Easy to add new agents
- **Configuration-Driven**: YAML-based configuration management
- **Provider Agnostic**: Support multiple LLM providers (OpenAI, Anthropic, etc.)
- **Database Flexible**: Works with any vector database or storage system

### **Enterprise Features**
- **Agent Registry**: Centralized discovery and management
- **Health Monitoring**: Real-time performance tracking
- **Security Layer**: API key management and access control
- **Scaling Support**: Horizontal scaling with load balancing

## 📊 Current Agent Implementations

| Agent | Type | Status | Primary Use Case |
|-------|------|---------|------------------|
| Procurement Assistant | Conversational AI | Production | Vendor inquiries & support |
| Report Generation | Document Automation | Production | Automated business reporting |
| Expense Approval | Process Automation | Pilot | Expense claim processing |
| Multi-Agent Orchestration | Agent Coordination | Development | Complex workflow management |
| Contract Analysis | Document Intelligence | Beta | Legal document review |

## 🔧 Usage Examples

### **Python Integration**
```python
from agents.core.registry import AgentRegistry
from agents.implementations.procurement import ProcurementAgent

# Initialize registry
registry = AgentRegistry()

# Load agent
procurement_agent = registry.get_agent('procurement_assistant')

# Execute task
result = await procurement_agent.process_query(
    "What's the status of vendor approval for TechCorp?"
)
```

### **Node.js Integration**
```javascript
import { AgentRegistry } from './agents/core/registry.js';

const registry = new AgentRegistry();
const reportAgent = await registry.getAgent('report_generation');

const report = await reportAgent.generateReport({
    type: 'monthly_sales',
    dateRange: { start: '2025-08-01', end: '2025-08-31' }
});
```

### **REST API Usage**
```bash
# Query any agent via HTTP
curl -X POST http://localhost:8000/agents/procurement_assistant/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me pending vendor applications"}'

# Get agent status and metrics
curl http://localhost:8000/agents/status
```

## 📈 Benefits

### **For Current CMS Project**
- Clean separation of AI logic from UI components
- Reusable agents across frontend, backend, and CLI tools
- Easier testing and maintenance

### **For Future Projects**
- Drop-in agent system for any new application
- Standardized AI integration patterns
- Shared configuration and monitoring across projects

### **For Team Development**
- Clear interfaces and documentation
- Independent development of agents
- Consistent deployment and scaling patterns

## 🛠️ Next Steps

1. **Migration Strategy**: Gradually move agents from Frontend/AIAgents.jsx
2. **API Integration**: Connect with existing backend/routers/ai_assistant.py
3. **Configuration Setup**: Environment-specific agent configurations
4. **Documentation**: Complete API reference and integration guides