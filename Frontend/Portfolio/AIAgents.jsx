import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Bot, 
  MessageSquare, 
  FileText, 
  Workflow, 
  Network,
  Zap,
  CheckCircle,
  Clock,
  Users,
  TrendingUp,
  Cpu,
  Brain,
  Settings,
  ArrowRight
} from 'lucide-react'

const AIAgents = () => {
  const [selectedAgent, setSelectedAgent] = useState(null)

  const aiProjects = [
    {
      id: 1,
      title: "Procurement Assistant Chatbot",
      category: "Conversational AI",
      description: "Intelligent chatbot automating vendor inquiries and procurement process guidance with natural language processing and document retrieval capabilities.",
      purpose: "Reduce response times for vendor inquiries and provide 24/7 support for procurement processes, freeing up human resources for strategic tasks.",
      capabilities: [
        "Natural language query processing",
        "Document retrieval and search",
        "Process workflow guidance",
        "Multi-language support",
        "Integration with procurement systems",
        "Escalation to human agents"
      ],
      technicalDetails: {
        llm: "OpenAI GPT-4",
        framework: "LangChain",
        vectorDb: "Pinecone",
        deployment: "Docker + Kubernetes",
        integration: "REST APIs"
      },
      metrics: {
        accuracy: 92,
        responseTime: "< 2 seconds",
        satisfaction: 88,
        automation: 75
      },
      businessImpact: {
        primary: "60% faster response times",
        metrics: [
          "24/7 availability",
          "75% query automation",
          "40 hours weekly time savings",
          "Improved vendor satisfaction"
        ]
      },
      technologies: ["OpenAI GPT-4", "LangChain", "React", "Node.js", "Pinecone", "Docker"],
      status: "Production",
      year: "2024",
      complexity: "High"
    },
    {
      id: 2,
      title: "Automated Report Generation Agent",
      category: "Document Automation",
      description: "AI agent that automatically generates comprehensive business reports from data sources with narrative generation and professional formatting.",
      purpose: "Eliminate manual report creation processes, ensure consistency in reporting, and enable real-time insights generation from multiple data sources.",
      capabilities: [
        "Multi-source data extraction",
        "Automated analysis and insights",
        "Natural language narrative generation",
        "Professional report formatting",
        "Scheduled report delivery",
        "Custom template support"
      ],
      technicalDetails: {
        llm: "OpenAI GPT-3.5 Turbo",
        dataProcessing: "Pandas + NumPy",
        reporting: "ReportLab + Jinja2",
        scheduling: "Apache Airflow",
        storage: "AWS S3"
      },
      metrics: {
        accuracy: 95,
        timeReduction: 85,
        consistency: 98,
        satisfaction: 91
      },
      businessImpact: {
        primary: "85% time reduction",
        metrics: [
          "Weekly automated reports",
          "Consistent formatting",
          "Real-time data insights",
          "Reduced human error"
        ]
      },
      technologies: ["Python", "OpenAI API", "Pandas", "ReportLab", "Apache Airflow", "AWS"],
      status: "Production",
      year: "2023",
      complexity: "Medium"
    },
    {
      id: 3,
      title: "Expense Approval Workflow Agent",
      category: "Process Automation",
      description: "Intelligent agent for expense claim processing with document analysis, policy compliance checking, and automated routing logic.",
      purpose: "Streamline expense approval processes, ensure policy compliance, and reduce manual review time while maintaining accuracy and audit trails.",
      capabilities: [
        "Receipt OCR and data extraction",
        "Policy compliance validation",
        "Intelligent routing logic",
        "Anomaly detection",
        "Approval workflow automation",
        "Audit trail generation"
      ],
      technicalDetails: {
        ocr: "Google Cloud Vision API",
        ruleEngine: "Python Rules Engine",
        workflow: "Temporal.io",
        storage: "PostgreSQL",
        monitoring: "Prometheus"
      },
      metrics: {
        accuracy: 94,
        processing: "< 30 seconds",
        compliance: 99,
        automation: 80
      },
      businessImpact: {
        primary: "80% process automation",
        metrics: [
          "30-second processing time",
          "99% policy compliance",
          "Reduced approval delays",
          "Complete audit trails"
        ]
      },
      technologies: ["Python", "Google Cloud Vision", "Temporal.io", "PostgreSQL", "FastAPI"],
      status: "Pilot",
      year: "2024",
      complexity: "High"
    },
    {
      id: 4,
      title: "Multi-Agent Data Pipeline Orchestration",
      category: "Agent Orchestration",
      description: "Coordinated system of AI agents managing complex data processing tasks with task distribution, error handling, and result aggregation.",
      purpose: "Enable scalable, fault-tolerant data processing through intelligent agent coordination, reducing manual intervention and improving reliability.",
      capabilities: [
        "Dynamic task distribution",
        "Agent health monitoring",
        "Automatic error recovery",
        "Load balancing",
        "Result aggregation",
        "Performance optimization"
      ],
      technicalDetails: {
        orchestration: "CrewAI",
        containerization: "Docker Swarm",
        monitoring: "Grafana + Prometheus",
        messageQueue: "Redis",
        database: "MongoDB"
      },
      metrics: {
        reliability: 99.5,
        scalability: "10x throughput",
        efficiency: 90,
        recovery: "< 5 minutes"
      },
      businessImpact: {
        primary: "10x processing throughput",
        metrics: [
          "99.5% system reliability",
          "Automatic error recovery",
          "Scalable architecture",
          "Reduced operational overhead"
        ]
      },
      technologies: ["CrewAI", "Docker", "Redis", "MongoDB", "Grafana", "Python"],
      status: "Development",
      year: "2024",
      complexity: "Very High"
    },
    {
      id: 5,
      title: "Intelligent Contract Analysis Agent",
      category: "Document Intelligence",
      description: "AI agent for automated contract review, risk assessment, and compliance checking with natural language understanding and legal knowledge.",
      purpose: "Accelerate contract review processes, identify potential risks and compliance issues, and provide consistent analysis across all contract types.",
      capabilities: [
        "Contract clause extraction",
        "Risk assessment scoring",
        "Compliance checking",
        "Comparison analysis",
        "Key terms identification",
        "Legal recommendation generation"
      ],
      technicalDetails: {
        llm: "Claude-3 Sonnet",
        vectorDb: "Weaviate",
        nlp: "spaCy + Transformers",
        api: "FastAPI",
        frontend: "Streamlit"
      },
      metrics: {
        accuracy: 89,
        coverage: 95,
        speed: "10x faster",
        consistency: 97
      },
      businessImpact: {
        primary: "10x faster review",
        metrics: [
          "89% accuracy in risk detection",
          "Consistent analysis standards",
          "Reduced legal review time",
          "Improved compliance scores"
        ]
      },
      technologies: ["Claude-3", "Weaviate", "spaCy", "FastAPI", "Streamlit", "Python"],
      status: "Beta",
      year: "2024",
      complexity: "High"
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'Production': return 'bg-green-500'
      case 'Pilot': return 'bg-yellow-500'
      case 'Beta': return 'bg-blue-500'
      case 'Development': return 'bg-purple-500'
      default: return 'bg-gray-500'
    }
  }

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Conversational AI': return MessageSquare
      case 'Document Automation': return FileText
      case 'Process Automation': return Workflow
      case 'Agent Orchestration': return Network
      case 'Document Intelligence': return Brain
      default: return Bot
    }
  }

  const getComplexityColor = (complexity) => {
    switch (complexity) {
      case 'Very High': return 'text-red-600'
      case 'High': return 'text-red-500'
      case 'Medium': return 'text-yellow-500'
      case 'Low': return 'text-green-500'
      default: return 'text-gray-500'
    }
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl lg:text-5xl font-bold mb-6">
            AI Agent Development & Orchestration
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto mb-8">
            Cutting-edge AI agent systems that automate complex business processes, 
            from conversational interfaces to multi-agent orchestration workflows. 
            Each solution demonstrates advanced AI implementation and measurable business impact.
          </p>
          
          {/* AI Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">5</div>
              <div className="text-sm text-muted-foreground">AI Agents</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">92%</div>
              <div className="text-sm text-muted-foreground">Avg Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">80%</div>
              <div className="text-sm text-muted-foreground">Process Automation</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">24/7</div>
              <div className="text-sm text-muted-foreground">Availability</div>
            </div>
          </div>
        </div>

        {/* AI Projects */}
        <div className="space-y-8 mb-16">
          {aiProjects.map((project) => {
            const IconComponent = getCategoryIcon(project.category)
            const isExpanded = selectedAgent === project.id
            
            return (
              <Card key={project.id} className="overflow-hidden">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                        <IconComponent className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2 mb-1">
                          <Badge variant="secondary">{project.category}</Badge>
                          <div className={`w-2 h-2 rounded-full ${getStatusColor(project.status)}`} />
                          <span className="text-xs text-muted-foreground">{project.status}</span>
                        </div>
                        <CardTitle className="text-xl">{project.title}</CardTitle>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="text-sm text-muted-foreground mb-1">{project.year}</div>
                      <div className={`text-xs font-medium ${getComplexityColor(project.complexity)}`}>
                        {project.complexity} Complexity
                      </div>
                    </div>
                  </div>
                  
                  <CardDescription className="text-sm leading-relaxed mt-3">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-6">
                  {/* Performance Metrics */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-lg">
                    {Object.entries(project.metrics).map(([key, value]) => (
                      <div key={key} className="text-center">
                        <div className="text-2xl font-bold text-primary">
                          {typeof value === 'number' ? `${value}%` : value}
                        </div>
                        <div className="text-xs text-muted-foreground capitalize">
                          {key.replace(/([A-Z])/g, ' $1')}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Business Impact */}
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <TrendingUp className="w-4 h-4 text-green-500" />
                      <span className="font-medium text-green-600 dark:text-green-400">
                        {project.businessImpact.primary}
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {project.businessImpact.metrics.map((metric, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm">
                          <CheckCircle className="w-3 h-3 text-green-500" />
                          <span className="text-muted-foreground">{metric}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Key Capabilities */}
                  <div>
                    <h4 className="font-medium text-sm mb-3">AI Capabilities</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {project.capabilities.slice(0, 4).map((capability, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm">
                          <Bot className="w-3 h-3 text-blue-500 flex-shrink-0" />
                          <span className="text-muted-foreground">{capability}</span>
                        </div>
                      ))}
                    </div>
                    {project.capabilities.length > 4 && (
                      <div className="text-xs text-muted-foreground mt-2">
                        +{project.capabilities.length - 4} more capabilities
                      </div>
                    )}
                  </div>

                  {/* Technologies */}
                  <div>
                    <h4 className="font-medium text-sm mb-3">Technology Stack</h4>
                    <div className="flex flex-wrap gap-2">
                      {project.technologies.map((tech) => (
                        <Badge key={tech} variant="outline" className="text-xs">
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Expand/Collapse Button */}
                  <Button
                    variant="ghost"
                    className="w-full"
                    onClick={() => setSelectedAgent(isExpanded ? null : project.id)}
                  >
                    {isExpanded ? 'Hide Technical Details' : 'View Technical Architecture'}
                    <Settings className="w-4 h-4 ml-2" />
                  </Button>

                  {/* Expanded Technical Details */}
                  {isExpanded && (
                    <div className="space-y-6 pt-6 border-t border-border">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Purpose & Approach */}
                        <div>
                          <h4 className="font-medium mb-3 flex items-center">
                            <Brain className="w-4 h-4 mr-2 text-blue-500" />
                            Purpose & Approach
                          </h4>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {project.purpose}
                          </p>
                        </div>

                        {/* Technical Architecture */}
                        <div>
                          <h4 className="font-medium mb-3 flex items-center">
                            <Cpu className="w-4 h-4 mr-2 text-purple-500" />
                            Technical Architecture
                          </h4>
                          <div className="space-y-2">
                            {Object.entries(project.technicalDetails).map(([key, value]) => (
                              <div key={key} className="flex justify-between text-sm">
                                <span className="text-muted-foreground capitalize">
                                  {key.replace(/([A-Z])/g, ' $1')}:
                                </span>
                                <span className="font-medium">{value}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* All Capabilities */}
                      <div>
                        <h4 className="font-medium mb-3 flex items-center">
                          <Zap className="w-4 h-4 mr-2 text-yellow-500" />
                          Complete Capability Set
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {project.capabilities.map((capability, index) => (
                            <div key={index} className="flex items-center space-x-2 text-sm">
                              <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                              <span className="text-muted-foreground">{capability}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* AI Development Methodology */}
        <section className="py-16 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-950/20 dark:to-blue-950/20 rounded-2xl mb-16">
          <div className="max-w-5xl mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">AI Agent Development Process</h2>
              <p className="text-muted-foreground">
                Systematic approach to building reliable, scalable AI agent systems
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Brain className="w-8 h-8 text-blue-500" />
                </div>
                <h3 className="font-semibold mb-3">Design & Planning</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Requirements analysis</div>
                  <div>Architecture design</div>
                  <div>Technology selection</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Settings className="w-8 h-8 text-purple-500" />
                </div>
                <h3 className="font-semibold mb-3">Development</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Agent implementation</div>
                  <div>Integration testing</div>
                  <div>Performance optimization</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-green-500" />
                </div>
                <h3 className="font-semibold mb-3">Testing & Validation</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Accuracy validation</div>
                  <div>Edge case testing</div>
                  <div>User acceptance</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-orange-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-8 h-8 text-orange-500" />
                </div>
                <h3 className="font-semibold mb-3">Deploy & Monitor</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Production deployment</div>
                  <div>Performance monitoring</div>
                  <div>Continuous improvement</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Future AI Initiatives */}
        <section className="text-center">
          <h2 className="text-3xl font-bold mb-6">Future AI Initiatives</h2>
          <p className="text-muted-foreground mb-8 max-w-3xl mx-auto">
            Exploring advanced AI capabilities and emerging technologies to solve 
            increasingly complex business challenges
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="p-6 text-center">
              <Network className="w-12 h-12 text-blue-500 mx-auto mb-4" />
              <h3 className="font-semibold mb-2">Multi-Modal AI</h3>
              <p className="text-sm text-muted-foreground">
                Integrating text, image, and audio processing for comprehensive document analysis
              </p>
            </Card>
            
            <Card className="p-6 text-center">
              <Workflow className="w-12 h-12 text-purple-500 mx-auto mb-4" />
              <h3 className="font-semibold mb-2">Autonomous Workflows</h3>
              <p className="text-sm text-muted-foreground">
                Self-optimizing business processes that adapt and improve over time
              </p>
            </Card>
            
            <Card className="p-6 text-center">
              <Users className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <h3 className="font-semibold mb-2">Human-AI Collaboration</h3>
              <p className="text-sm text-muted-foreground">
                Seamless integration of AI capabilities with human expertise and decision-making
              </p>
            </Card>
          </div>
        </section>
      </div>
    </div>
  )
}

export default AIAgents

