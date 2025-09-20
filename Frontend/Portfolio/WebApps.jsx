import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Globe, 
  Calculator, 
  Shield, 
  BarChart3, 
  CheckCircle,
  ExternalLink,
  Code,
  Smartphone,
  Monitor,
  Zap,
  Database,
  Layers
} from 'lucide-react'

const WebApps = () => {
  const [hoveredApp, setHoveredApp] = useState(null)

  const applications = [
    {
      id: 1,
      title: "Procurement ROI Calculator",
      category: "Business Tools",
      description: "Interactive calculator helping businesses evaluate the return on investment of procurement initiatives with real-time calculations and downloadable reports.",
      purpose: "Enable procurement professionals to quickly assess the financial impact of process improvements, technology investments, and strategic sourcing initiatives.",
      features: [
        "Interactive input forms with validation",
        "Real-time ROI calculations",
        "Visual charts and graphs",
        "Downloadable PDF reports",
        "Scenario comparison tools",
        "Mobile-responsive design"
      ],
      techStack: {
        frontend: ["React", "Chart.js", "Tailwind CSS"],
        backend: ["Node.js", "Express"],
        tools: ["Vite", "PDF-lib", "Recharts"]
      },
      highlights: {
        users: "500+ calculations",
        performance: "< 2s load time",
        mobile: "100% responsive",
        accuracy: "99.9% calculation accuracy"
      },
      demoUrl: "#",
      codeUrl: "#",
      status: "Live",
      year: "2024",
      complexity: "Medium"
    },
    {
      id: 2,
      title: "Supplier Risk Assessment Tool",
      category: "Risk Management",
      description: "Comprehensive risk evaluation platform for assessing and scoring supplier risk across multiple dimensions with visual risk matrices and comparison tools.",
      purpose: "Provide procurement teams with a standardized, data-driven approach to evaluate supplier risk and make informed sourcing decisions.",
      features: [
        "Multi-criteria risk scoring",
        "Interactive risk matrix visualization",
        "Supplier comparison dashboard",
        "Historical risk tracking",
        "Automated risk alerts",
        "Export capabilities"
      ],
      techStack: {
        frontend: ["React", "D3.js", "Material-UI"],
        backend: ["Python", "FastAPI"],
        database: ["PostgreSQL"],
        tools: ["Docker", "Plotly"]
      },
      highlights: {
        users: "200+ assessments",
        accuracy: "95% risk prediction",
        features: "15+ risk factors",
        integration: "API-ready"
      },
      demoUrl: "#",
      codeUrl: "#",
      status: "Live",
      year: "2023",
      complexity: "High"
    },
    {
      id: 3,
      title: "Budget Variance Analysis Dashboard",
      category: "Financial Analytics",
      description: "Real-time dashboard for tracking and analyzing budget performance across departments with drill-down capabilities and automated alert systems.",
      purpose: "Give finance teams and department managers instant visibility into budget performance with actionable insights and early warning systems.",
      features: [
        "Real-time budget tracking",
        "Interactive drill-down charts",
        "Automated variance alerts",
        "Department comparisons",
        "Trend analysis",
        "Custom reporting"
      ],
      techStack: {
        frontend: ["React", "Recharts", "Ant Design"],
        backend: ["Node.js", "Express"],
        database: ["MongoDB"],
        tools: ["Socket.io", "Chart.js"]
      },
      highlights: {
        departments: "12 departments",
        updates: "Real-time",
        alerts: "Automated",
        accuracy: "99% data sync"
      },
      demoUrl: "#",
      codeUrl: "#",
      status: "Beta",
      year: "2023",
      complexity: "High"
    },
    {
      id: 4,
      title: "Data Quality Monitoring App",
      category: "Data Management",
      description: "Automated data quality monitoring system with trend analysis, notification systems, and comprehensive quality metrics tracking.",
      purpose: "Ensure data integrity across business systems by continuously monitoring quality metrics and alerting teams to potential issues.",
      features: [
        "Automated quality checks",
        "Real-time monitoring dashboard",
        "Quality trend analysis",
        "Email/SMS notifications",
        "Custom quality rules",
        "Historical reporting"
      ],
      techStack: {
        frontend: ["React", "TypeScript", "Chakra UI"],
        backend: ["Python", "Flask"],
        database: ["PostgreSQL", "Redis"],
        tools: ["Celery", "Pandas"]
      },
      highlights: {
        checks: "50+ quality rules",
        monitoring: "24/7 automated",
        accuracy: "99.9% uptime",
        alerts: "Real-time"
      },
      demoUrl: "#",
      codeUrl: "#",
      status: "Development",
      year: "2024",
      complexity: "High"
    },
    {
      id: 5,
      title: "Contract Lifecycle Tracker",
      category: "Process Management",
      description: "End-to-end contract management system tracking contracts from initiation to renewal with automated workflows and compliance monitoring.",
      purpose: "Streamline contract management processes, ensure compliance, and prevent missed renewals through automated tracking and notifications.",
      features: [
        "Contract lifecycle tracking",
        "Automated renewal reminders",
        "Compliance monitoring",
        "Document management",
        "Approval workflows",
        "Performance analytics"
      ],
      techStack: {
        frontend: ["Vue.js", "Vuetify", "JavaScript"],
        backend: ["Python", "Django"],
        database: ["PostgreSQL"],
        tools: ["Celery", "Redis"]
      },
      highlights: {
        contracts: "500+ tracked",
        automation: "90% automated",
        compliance: "100% tracked",
        renewals: "Zero missed"
      },
      demoUrl: "#",
      codeUrl: "#",
      status: "Pilot",
      year: "2024",
      complexity: "Medium"
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'Live': return 'bg-green-500'
      case 'Beta': return 'bg-yellow-500'
      case 'Pilot': return 'bg-blue-500'
      case 'Development': return 'bg-purple-500'
      default: return 'bg-gray-500'
    }
  }

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Business Tools': return Calculator
      case 'Risk Management': return Shield
      case 'Financial Analytics': return BarChart3
      case 'Data Management': return Database
      case 'Process Management': return Layers
      default: return Globe
    }
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl lg:text-5xl font-bold mb-6">
            Interactive Web Applications
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto mb-8">
            Full-stack web applications demonstrating modern development practices, 
            user-centered design, and practical business solutions. Each application 
            showcases different aspects of web development while solving real-world problems.
          </p>
          
          {/* Development Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">5</div>
              <div className="text-sm text-muted-foreground">Applications</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">3</div>
              <div className="text-sm text-muted-foreground">Live Apps</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">100%</div>
              <div className="text-sm text-muted-foreground">Mobile Ready</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">99%</div>
              <div className="text-sm text-muted-foreground">Uptime</div>
            </div>
          </div>
        </div>

        {/* Applications Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {applications.map((app) => {
            const IconComponent = getCategoryIcon(app.category)
            const isHovered = hoveredApp === app.id
            
            return (
              <Card 
                key={app.id} 
                className={`group transition-all duration-300 hover:shadow-xl ${
                  isHovered ? 'scale-[1.02]' : ''
                }`}
                onMouseEnter={() => setHoveredApp(app.id)}
                onMouseLeave={() => setHoveredApp(null)}
              >
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                        <IconComponent className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <Badge variant="secondary" className="mb-2">
                          {app.category}
                        </Badge>
                        <div className="flex items-center space-x-2">
                          <div className={`w-2 h-2 rounded-full ${getStatusColor(app.status)}`} />
                          <span className="text-xs text-muted-foreground">{app.status}</span>
                          <span className="text-xs text-muted-foreground">•</span>
                          <span className="text-xs text-muted-foreground">{app.year}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <CardTitle className="text-xl group-hover:text-primary transition-colors">
                    {app.title}
                  </CardTitle>
                  <CardDescription className="text-sm leading-relaxed">
                    {app.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-6">
                  {/* Purpose */}
                  <div>
                    <h4 className="font-medium text-sm mb-2">Purpose & Value</h4>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {app.purpose}
                    </p>
                  </div>

                  {/* Key Highlights */}
                  <div className="grid grid-cols-2 gap-4 p-4 bg-muted/30 rounded-lg">
                    {Object.entries(app.highlights).map(([key, value]) => (
                      <div key={key} className="text-center">
                        <div className="text-lg font-bold text-primary">{value}</div>
                        <div className="text-xs text-muted-foreground capitalize">
                          {key.replace(/([A-Z])/g, ' $1')}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Key Features */}
                  <div>
                    <h4 className="font-medium text-sm mb-3">Key Features</h4>
                    <div className="grid grid-cols-1 gap-2">
                      {app.features.slice(0, 4).map((feature, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm">
                          <CheckCircle className="w-3 h-3 text-green-500 flex-shrink-0" />
                          <span className="text-muted-foreground">{feature}</span>
                        </div>
                      ))}
                      {app.features.length > 4 && (
                        <div className="text-xs text-muted-foreground mt-1">
                          +{app.features.length - 4} more features
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Tech Stack */}
                  <div>
                    <h4 className="font-medium text-sm mb-3">Technology Stack</h4>
                    <div className="space-y-2">
                      <div className="flex flex-wrap gap-1">
                        <Badge variant="outline" className="text-xs">Frontend</Badge>
                        {app.techStack.frontend.map((tech) => (
                          <Badge key={tech} variant="secondary" className="text-xs">
                            {tech}
                          </Badge>
                        ))}
                      </div>
                      {app.techStack.backend && (
                        <div className="flex flex-wrap gap-1">
                          <Badge variant="outline" className="text-xs">Backend</Badge>
                          {app.techStack.backend.map((tech) => (
                            <Badge key={tech} variant="secondary" className="text-xs">
                              {tech}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-2 pt-2">
                    <Button 
                      size="sm" 
                      className="flex-1"
                      onClick={() => {
                        // In a real implementation, this would open the live demo
                        alert(`Live demo for "${app.title}" would open here.`)
                      }}
                    >
                      <Globe className="w-4 h-4 mr-2" />
                      Live Demo
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => {
                        // In a real implementation, this would open the code repository
                        alert(`Code repository for "${app.title}" would open here.`)
                      }}
                    >
                      <Code className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Development Approach Section */}
        <section className="py-16 bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-950/20 dark:to-blue-950/20 rounded-2xl">
          <div className="max-w-5xl mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">Development Philosophy</h2>
              <p className="text-muted-foreground">
                Building scalable, maintainable applications with modern best practices
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Smartphone className="w-8 h-8 text-blue-500" />
                </div>
                <h3 className="font-semibold mb-3">Mobile-First Design</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Responsive across all devices</div>
                  <div>Touch-friendly interfaces</div>
                  <div>Progressive Web App features</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="w-8 h-8 text-green-500" />
                </div>
                <h3 className="font-semibold mb-3">Performance Optimized</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Fast loading times</div>
                  <div>Efficient data handling</div>
                  <div>Optimized bundle sizes</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-8 h-8 text-purple-500" />
                </div>
                <h3 className="font-semibold mb-3">Security & Reliability</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Input validation & sanitization</div>
                  <div>Error handling & logging</div>
                  <div>Automated testing</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Tech Stack Overview */}
        <section className="mt-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Technical Expertise</h2>
            <p className="text-muted-foreground">
              Modern web technologies and frameworks used across projects
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card className="text-center p-6">
              <Monitor className="w-8 h-8 text-blue-500 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Frontend</h3>
              <div className="space-y-1 text-sm text-muted-foreground">
                <div>React • Vue.js</div>
                <div>TypeScript • JavaScript</div>
                <div>Tailwind • Material-UI</div>
              </div>
            </Card>
            
            <Card className="text-center p-6">
              <Database className="w-8 h-8 text-green-500 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Backend</h3>
              <div className="space-y-1 text-sm text-muted-foreground">
                <div>Node.js • Python</div>
                <div>Express • FastAPI</div>
                <div>PostgreSQL • MongoDB</div>
              </div>
            </Card>
            
            <Card className="text-center p-6">
              <Layers className="w-8 h-8 text-purple-500 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Tools & DevOps</h3>
              <div className="space-y-1 text-sm text-muted-foreground">
                <div>Docker • Git</div>
                <div>Vite • Webpack</div>
                <div>Jest • Cypress</div>
              </div>
            </Card>
            
            <Card className="text-center p-6">
              <BarChart3 className="w-8 h-8 text-orange-500 mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Visualization</h3>
              <div className="space-y-1 text-sm text-muted-foreground">
                <div>D3.js • Chart.js</div>
                <div>Recharts • Plotly</div>
                <div>Custom dashboards</div>
              </div>
            </Card>
          </div>
        </section>
      </div>
    </div>
  )
}

export default WebApps

