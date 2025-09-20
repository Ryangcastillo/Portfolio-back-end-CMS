import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart3, 
  Brain, 
  Cog, 
  Sparkles, 
  Download, 
  ArrowRight,
  TrendingUp,
  Database,
  Zap,
  Target
} from 'lucide-react'
import { Link } from 'react-router-dom'

const Home = () => {
  const [hoveredSkill, setHoveredSkill] = useState(null)

  const skills = [
    {
      id: 1,
      title: "Data Analysis & Visualization",
      description: "Power BI, SQL, Advanced Excel, Statistical Analysis",
      icon: BarChart3,
      color: "from-blue-500 to-blue-600",
      projects: "15+ projects",
      impact: "$500K+ savings"
    },
    {
      id: 2,
      title: "Business Intelligence & Reporting",
      description: "SAP FICO, Dynamics 365, ETL processes, Dashboard development",
      icon: Database,
      color: "from-green-500 to-green-600",
      projects: "20+ dashboards",
      impact: "98% data quality"
    },
    {
      id: 3,
      title: "Process Improvement & Automation",
      description: "Agile methodologies, PowerApps, Workflow optimization, Vendor management",
      icon: Cog,
      color: "from-purple-500 to-purple-600",
      projects: "10+ processes",
      impact: "40% efficiency gain"
    },
    {
      id: 4,
      title: "Emerging AI & Machine Learning",
      description: "Python, Predictive analytics, AI agent development, Automation workflows",
      icon: Brain,
      color: "from-orange-500 to-orange-600",
      projects: "5+ AI models",
      impact: "85% accuracy"
    }
  ]

  const featuredProjects = [
    {
      id: 1,
      title: "Procurement Analytics Dashboard",
      description: "Comprehensive Power BI dashboard analyzing supplier performance and identifying cost optimization opportunities across multiple business units.",
      impact: "$200K annual savings",
      tech: ["Power BI", "SQL", "SAP FICO"],
      category: "Data Analysis",
      link: "/data-analysis"
    },
    {
      id: 2,
      title: "Predictive Maintenance Model",
      description: "Machine learning model predicting equipment failures 2 weeks in advance, enabling proactive maintenance scheduling and reducing downtime.",
      impact: "85% prediction accuracy",
      tech: ["Python", "Scikit-learn", "Pandas"],
      category: "Machine Learning",
      link: "/machine-learning"
    },
    {
      id: 3,
      title: "AI-Powered Process Automation",
      description: "Intelligent chatbot system for automating vendor inquiries and procurement process guidance, improving response times and accuracy.",
      impact: "60% faster responses",
      tech: ["OpenAI API", "React", "Node.js"],
      category: "AI Agents",
      link: "/ai-agents"
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 bg-gradient-to-br from-background via-background to-muted/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Content */}
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge variant="secondary" className="w-fit">
                  Available for New Opportunities
                </Badge>
                <h1 className="text-4xl lg:text-6xl font-bold tracking-tight">
                  Data Analyst &{' '}
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Process Improvement
                  </span>{' '}
                  Specialist
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl">
                  Transforming business challenges into actionable insights through advanced 
                  analytics and AI innovation. 8+ years of experience delivering measurable 
                  business value through data-driven solutions.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Button size="lg" className="flex items-center space-x-2" asChild>
                  <Link to="/data-analysis">
                    <span>View My Work</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </Button>
                <Button 
                  variant="outline" 
                  size="lg" 
                  className="flex items-center space-x-2"
                  onClick={() => window.open('/resume.pdf', '_blank')}
                >
                  <Download className="w-4 h-4" />
                  <span>Download Resume</span>
                </Button>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8 border-t border-border">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">8+</div>
                  <div className="text-sm text-muted-foreground">Years Experience</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">$500K+</div>
                  <div className="text-sm text-muted-foreground">Cost Savings</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">50+</div>
                  <div className="text-sm text-muted-foreground">Projects Delivered</div>
                </div>
              </div>
            </div>

            {/* Profile Image Placeholder */}
            <div className="flex justify-center lg:justify-end">
              <div className="relative">
                <div className="w-80 h-80 bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20 rounded-2xl flex items-center justify-center border border-border">
                  <div className="text-center space-y-4">
                    <div className="w-24 h-24 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto">
                      <span className="text-white font-bold text-2xl">RC</span>
                    </div>
                    <div>
                      <p className="font-semibold text-lg">Ryan Castillo</p>
                      <p className="text-muted-foreground">Auckland, New Zealand</p>
                    </div>
                  </div>
                </div>
                {/* Floating elements */}
                <div className="absolute -top-4 -right-4 w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center animate-bounce">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -bottom-4 -left-4 w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center animate-bounce" style={{ animationDelay: '0.5s' }}>
                  <Brain className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section className="py-20 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">Core Expertise</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Combining technical proficiency with business acumen to deliver 
              data-driven solutions that create measurable impact
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {skills.map((skill) => {
              const IconComponent = skill.icon
              return (
                <Card 
                  key={skill.id}
                  className={`relative overflow-hidden transition-all duration-300 hover:shadow-lg cursor-pointer ${
                    hoveredSkill === skill.id ? 'scale-105' : ''
                  }`}
                  onMouseEnter={() => setHoveredSkill(skill.id)}
                  onMouseLeave={() => setHoveredSkill(null)}
                >
                  <CardHeader className="pb-3">
                    <div className={`w-12 h-12 bg-gradient-to-r ${skill.color} rounded-lg flex items-center justify-center mb-4`}>
                      <IconComponent className="w-6 h-6 text-white" />
                    </div>
                    <CardTitle className="text-lg">{skill.title}</CardTitle>
                    <CardDescription className="text-sm">
                      {skill.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>{skill.projects}</span>
                      <span className="font-medium text-primary">{skill.impact}</span>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">Featured Projects</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Showcasing real-world applications of data analysis, machine learning, 
              and AI technologies that delivered significant business value
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {featuredProjects.map((project) => (
              <Card key={project.id} className="group hover:shadow-lg transition-all duration-300">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <Badge variant="secondary" className="mb-2">
                      {project.category}
                    </Badge>
                    <TrendingUp className="w-5 h-5 text-green-500" />
                  </div>
                  <CardTitle className="group-hover:text-primary transition-colors">
                    {project.title}
                  </CardTitle>
                  <CardDescription className="text-sm leading-relaxed">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Target className="w-4 h-4 text-green-500" />
                    <span className="text-sm font-medium text-green-600 dark:text-green-400">
                      {project.impact}
                    </span>
                  </div>
                  
                  <div className="flex flex-wrap gap-2">
                    {project.tech.map((tech) => (
                      <Badge key={tech} variant="outline" className="text-xs">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                  
                  <Button 
                    variant="ghost" 
                    className="w-full group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
                    asChild
                  >
                    <Link to={project.link} className="flex items-center justify-center space-x-2">
                      <span>View Details</span>
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="space-y-6">
            <h2 className="text-3xl lg:text-4xl font-bold text-white">
              Ready to Transform Your Data into Insights?
            </h2>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              Let's discuss how my expertise in data analysis, process improvement, 
              and AI can help drive your business forward.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                variant="secondary"
                className="flex items-center space-x-2"
                onClick={() => {
                  // Scroll to chatbot or open contact
                  document.querySelector('[data-chatbot]')?.click()
                }}
              >
                <Sparkles className="w-4 h-4" />
                <span>Start a Conversation</span>
              </Button>
              <Button 
                size="lg" 
                variant="outline"
                className="bg-transparent border-white text-white hover:bg-white hover:text-blue-600"
                onClick={() => window.open('mailto:ryan.castillo@email.com', '_blank')}
              >
                Get in Touch
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home

