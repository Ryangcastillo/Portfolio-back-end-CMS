import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  BarChart3, 
  Database, 
  TrendingUp, 
  Target, 
  ExternalLink,
  Filter,
  Clock,
  DollarSign,
  Users,
  Zap
} from 'lucide-react'

const DataAnalysis = () => {
  const [selectedCategory, setSelectedCategory] = useState('all')

  const projects = [
    {
      id: 1,
      title: "Supplier Performance Analytics Dashboard",
      category: "business-intelligence",
      description: "Comprehensive Power BI dashboard analyzing supplier performance across multiple metrics including delivery times, quality scores, and cost efficiency. Integrated data from SAP FICO and external supplier systems.",
      challenge: "Auckland Transport needed visibility into supplier performance across 200+ vendors with inconsistent data sources and manual reporting processes taking 40+ hours monthly.",
      solution: "Built automated Power BI dashboard with real-time data integration from SAP, SharePoint, and external APIs. Implemented KPI tracking, trend analysis, and predictive scoring.",
      impact: {
        primary: "$200K annual savings",
        metrics: [
          "15% reduction in supplier issues",
          "40 hours monthly time savings",
          "98% data accuracy improvement",
          "Real-time performance monitoring"
        ]
      },
      technologies: ["Power BI", "SQL Server", "SAP FICO", "SharePoint", "DAX"],
      duration: "3 months",
      year: "2023",
      image: "/api/placeholder/600/400"
    },
    {
      id: 2,
      title: "Procurement Spend Analysis & Forecasting",
      category: "predictive-analytics",
      description: "Advanced analytics solution for procurement spend forecasting using historical data, market trends, and seasonal patterns. Enabled proactive budget planning and cost optimization.",
      challenge: "Spark NZ required better spend forecasting accuracy and identification of cost-saving opportunities across $50M annual procurement budget.",
      solution: "Developed predictive models using Python and integrated with Dynamics 365. Created automated reporting with scenario planning and budget variance analysis.",
      impact: {
        primary: "$150K cost savings identified",
        metrics: [
          "25% improvement in forecast accuracy",
          "Early identification of budget overruns",
          "Automated monthly reporting",
          "Strategic sourcing recommendations"
        ]
      },
      technologies: ["Python", "Power BI", "Dynamics 365", "Pandas", "Scikit-learn"],
      duration: "4 months",
      year: "2023",
      image: "/api/placeholder/600/400"
    },
    {
      id: 3,
      title: "Vendor Master Data Optimization",
      category: "data-modeling",
      description: "Comprehensive data cleansing and governance project to eliminate duplicate vendors, standardize data formats, and implement automated quality checks.",
      challenge: "Multiple systems contained 15,000+ vendor records with 30% duplicates, inconsistent naming conventions, and manual data entry errors causing process delays.",
      solution: "Implemented automated data matching algorithms, created standardized data entry workflows using PowerApps, and established ongoing governance processes.",
      impact: {
        primary: "98% data quality achieved",
        metrics: [
          "40% reduction in vendor onboarding time",
          "Eliminated 4,500 duplicate records",
          "Automated quality monitoring",
          "Standardized data governance"
        ]
      },
      technologies: ["PowerApps", "SharePoint", "SQL", "Power Automate", "Excel"],
      duration: "6 months",
      year: "2022",
      image: "/api/placeholder/600/400"
    },
    {
      id: 4,
      title: "Contract Performance Monitoring System",
      category: "business-intelligence",
      description: "Real-time contract performance monitoring system with automated alerts for renewal dates, compliance issues, and performance metrics.",
      challenge: "Manual contract tracking across 500+ contracts led to missed renewals, compliance issues, and lack of performance visibility.",
      solution: "Built comprehensive monitoring system using Power BI and ServiceNow integration with automated workflows and performance scorecards.",
      impact: {
        primary: "Zero missed renewals",
        metrics: [
          "30% improvement in contract compliance",
          "Automated renewal notifications",
          "Performance trend analysis",
          "Risk mitigation protocols"
        ]
      },
      technologies: ["Power BI", "ServiceNow", "Azure DevOps", "Power Automate"],
      duration: "3 months",
      year: "2022",
      image: "/api/placeholder/600/400"
    },
    {
      id: 5,
      title: "Financial Audit Data Analysis",
      category: "data-modeling",
      description: "Automated audit trail generation and anomaly detection system for internal and external audit requirements, reducing manual effort and improving accuracy.",
      challenge: "Quarterly audits required 80+ hours of manual data extraction and analysis from multiple systems with high error rates and delayed reporting.",
      solution: "Created automated data extraction pipelines with anomaly detection algorithms and standardized audit report generation.",
      impact: {
        primary: "60% reduction in audit prep time",
        metrics: [
          "Automated anomaly detection",
          "Standardized audit trails",
          "Improved compliance scores",
          "Real-time data validation"
        ]
      },
      technologies: ["SQL", "Advanced Excel", "Power BI", "VBA", "Python"],
      duration: "2 months",
      year: "2021",
      image: "/api/placeholder/600/400"
    },
    {
      id: 6,
      title: "Transportation Route Optimization",
      category: "process-optimization",
      description: "Data-driven analysis of bus route efficiency using passenger data, traffic patterns, and operational metrics to optimize Auckland Transport routes.",
      challenge: "Inefficient bus routes with low utilization rates and passenger complaints about service frequency and coverage gaps.",
      solution: "Analyzed passenger flow data, traffic patterns, and demographic information to recommend route optimizations and service improvements.",
      impact: {
        primary: "12% improvement in route efficiency",
        metrics: [
          "Better passenger satisfaction scores",
          "Optimized service frequency",
          "Reduced operational costs",
          "Data-driven route planning"
        ]
      },
      technologies: ["Python", "SQL", "GIS Analysis", "Tableau", "R"],
      duration: "5 months",
      year: "2021",
      image: "/api/placeholder/600/400"
    }
  ]

  const categories = [
    { id: 'all', label: 'All Projects', count: projects.length },
    { id: 'business-intelligence', label: 'Business Intelligence', count: projects.filter(p => p.category === 'business-intelligence').length },
    { id: 'predictive-analytics', label: 'Predictive Analytics', count: projects.filter(p => p.category === 'predictive-analytics').length },
    { id: 'data-modeling', label: 'Data Modeling', count: projects.filter(p => p.category === 'data-modeling').length },
    { id: 'process-optimization', label: 'Process Optimization', count: projects.filter(p => p.category === 'process-optimization').length }
  ]

  const filteredProjects = selectedCategory === 'all' 
    ? projects 
    : projects.filter(project => project.category === selectedCategory)

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'business-intelligence': return BarChart3
      case 'predictive-analytics': return TrendingUp
      case 'data-modeling': return Database
      case 'process-optimization': return Zap
      default: return BarChart3
    }
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl lg:text-5xl font-bold mb-6">
            Data Analysis & Business Intelligence
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto mb-8">
            Transforming complex business challenges into actionable insights through 
            advanced analytics, data visualization, and intelligent automation. Each project 
            demonstrates measurable business impact and technical excellence.
          </p>
          
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">$500K+</div>
              <div className="text-sm text-muted-foreground">Total Savings</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">15+</div>
              <div className="text-sm text-muted-foreground">Projects</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">98%</div>
              <div className="text-sm text-muted-foreground">Data Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">8</div>
              <div className="text-sm text-muted-foreground">Years Experience</div>
            </div>
          </div>
        </div>

        {/* Category Filter */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold">Project Portfolio</h2>
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              <Filter className="w-4 h-4" />
              <span>Filter by category</span>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <Button
                key={category.id}
                variant={selectedCategory === category.id ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedCategory(category.id)}
                className="flex items-center space-x-2"
              >
                <span>{category.label}</span>
                <Badge variant="secondary" className="ml-2">
                  {category.count}
                </Badge>
              </Button>
            ))}
          </div>
        </div>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {filteredProjects.map((project) => {
            const IconComponent = getCategoryIcon(project.category)
            return (
              <Card key={project.id} className="group hover:shadow-lg transition-all duration-300">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                        <IconComponent className="w-4 h-4 text-primary" />
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {project.category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </Badge>
                    </div>
                    <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                      <Clock className="w-3 h-3" />
                      <span>{project.duration}</span>
                      <span>•</span>
                      <span>{project.year}</span>
                    </div>
                  </div>
                  
                  <CardTitle className="text-xl group-hover:text-primary transition-colors">
                    {project.title}
                  </CardTitle>
                  <CardDescription className="text-sm leading-relaxed">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-6">
                  {/* Challenge & Solution */}
                  <Tabs defaultValue="overview" className="w-full">
                    <TabsList className="grid w-full grid-cols-3">
                      <TabsTrigger value="overview">Overview</TabsTrigger>
                      <TabsTrigger value="solution">Solution</TabsTrigger>
                      <TabsTrigger value="impact">Impact</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="overview" className="mt-4">
                      <div className="space-y-3">
                        <div>
                          <h4 className="font-medium text-sm mb-2">Challenge</h4>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {project.challenge}
                          </p>
                        </div>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="solution" className="mt-4">
                      <div className="space-y-3">
                        <div>
                          <h4 className="font-medium text-sm mb-2">Technical Solution</h4>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {project.solution}
                          </p>
                        </div>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="impact" className="mt-4">
                      <div className="space-y-3">
                        <div className="flex items-center space-x-2 mb-3">
                          <Target className="w-4 h-4 text-green-500" />
                          <span className="font-medium text-green-600 dark:text-green-400">
                            {project.impact.primary}
                          </span>
                        </div>
                        <div className="grid grid-cols-1 gap-2">
                          {project.impact.metrics.map((metric, index) => (
                            <div key={index} className="flex items-center space-x-2 text-sm">
                              <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                              <span className="text-muted-foreground">{metric}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </TabsContent>
                  </Tabs>
                  
                  {/* Technologies */}
                  <div>
                    <h4 className="font-medium text-sm mb-3">Technologies Used</h4>
                    <div className="flex flex-wrap gap-2">
                      {project.technologies.map((tech) => (
                        <Badge key={tech} variant="outline" className="text-xs">
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  {/* Action Button */}
                  <Button 
                    variant="ghost" 
                    className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
                    onClick={() => {
                      // In a real implementation, this would open a detailed case study
                      alert(`Detailed case study for "${project.title}" would open here.`)
                    }}
                  >
                    <span>View Detailed Case Study</span>
                    <ExternalLink className="w-4 h-4 ml-2" />
                  </Button>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Skills & Tools Section */}
        <section className="mt-20 py-16 bg-muted/30 rounded-2xl">
          <div className="max-w-5xl mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">Technical Expertise</h2>
              <p className="text-muted-foreground">
                Comprehensive toolkit for end-to-end data analysis and business intelligence
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BarChart3 className="w-8 h-8 text-blue-500" />
                </div>
                <h3 className="font-semibold mb-3">Visualization & BI</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Power BI • Tableau</div>
                  <div>Advanced Excel • DAX</div>
                  <div>Dashboard Design</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Database className="w-8 h-8 text-green-500" />
                </div>
                <h3 className="font-semibold mb-3">Data & Systems</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>SQL Server • SAP FICO</div>
                  <div>Dynamics 365 • SharePoint</div>
                  <div>ETL Processes</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="w-8 h-8 text-purple-500" />
                </div>
                <h3 className="font-semibold mb-3">Automation & Analysis</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Python • R</div>
                  <div>Power Automate • PowerApps</div>
                  <div>Statistical Analysis</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default DataAnalysis

