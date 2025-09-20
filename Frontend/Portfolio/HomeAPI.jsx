import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Download, ArrowRight, BarChart3, Brain } from 'lucide-react'
import { Link } from 'react-router-dom'
import ProfileHero from '../components/ProfileHero'
import SkillsGrid from '../components/SkillsGrid'
import ProjectsGrid from '../components/ProjectsGrid'
import portfolioAPI from '../services/portfolioAPI'

const Home = () => {
  const [homepageData, setHomepageData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchHomepageData = async () => {
      try {
        setLoading(true)
        const data = await portfolioAPI.getHomepageData()
        setHomepageData(data)
      } catch (err) {
        console.error('Failed to fetch homepage data:', err)
        setError(err.message)
        
        // Fallback to hardcoded data if API fails
        setHomepageData({
          profile: {
            full_name: "Ryan Castillo",
            title: "Data Analyst",
            bio_description: "Transforming business challenges into actionable insights through advanced analytics and AI innovation. 8+ years of experience delivering measurable business value through data-driven solutions.",
            availability_status: "Available for New Opportunities",
            location: "Auckland, New Zealand",
            resume_url: "/resume.pdf"
          },
          stats: [
            { id: 1, metric_value: "8+", metric_name: "Years Experience" },
            { id: 2, metric_value: "$500K+", metric_name: "Cost Savings" },
            { id: 3, metric_value: "50+", metric_name: "Projects Delivered" }
          ],
          featured_skills: [
            {
              id: 1,
              title: "Data Analysis & Visualization",
              description: "Power BI, SQL, Advanced Excel, Statistical Analysis",
              icon_name: "BarChart3",
              color_gradient: "from-blue-500 to-blue-600",
              projects_count: "15+ projects",
              impact_metric: "$500K+ savings",
              category: "Analytics"
            },
            {
              id: 2,
              title: "Business Intelligence & Reporting",
              description: "SAP FICO, Dynamics 365, ETL processes, Dashboard development",
              icon_name: "Database",
              color_gradient: "from-green-500 to-green-600",
              projects_count: "20+ dashboards",
              impact_metric: "98% data quality"
            },
            {
              id: 3,
              title: "Process Improvement & Automation",
              description: "Agile methodologies, PowerApps, Workflow optimization, Vendor management",
              icon_name: "Cog",
              color_gradient: "from-purple-500 to-purple-600",
              projects_count: "10+ processes",
              impact_metric: "40% efficiency gain"
            },
            {
              id: 4,
              title: "Emerging AI & Machine Learning",
              description: "Python, Predictive analytics, AI agent development, Automation workflows",
              icon_name: "Brain",
              color_gradient: "from-orange-500 to-orange-600",
              projects_count: "5+ AI models",
              impact_metric: "85% accuracy"
            }
          ],
          featured_projects: [
            {
              id: 1,
              title: "Procurement Analytics Dashboard",
              short_description: "Comprehensive Power BI dashboard analyzing supplier performance and identifying cost optimization opportunities across multiple business units.",
              impact_metric: "$200K annual savings",
              technologies: ["Power BI", "SQL", "SAP FICO"],
              category: { name: "Data Analysis" },
              link: "/data-analysis"
            },
            {
              id: 2,
              title: "Predictive Maintenance Model",
              short_description: "Machine learning model predicting equipment failures 2 weeks in advance, enabling proactive maintenance scheduling and reducing downtime.",
              impact_metric: "85% prediction accuracy",
              technologies: ["Python", "Scikit-learn", "Pandas"],
              category: { name: "Machine Learning" },
              link: "/machine-learning"
            },
            {
              id: 3,
              title: "AI-Powered Process Automation",
              short_description: "Intelligent chatbot system for automating vendor inquiries and procurement process guidance, improving response times and accuracy.",
              impact_metric: "60% faster responses",
              technologies: ["OpenAI API", "React", "Node.js"],
              category: { name: "AI Agents" },
              link: "/ai-agents"
            }
          ]
        })
      } finally {
        setLoading(false)
      }
    }

    fetchHomepageData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (error && !homepageData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Failed to Load Content</h2>
          <p className="text-muted-foreground mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </div>
    )
  }

  const { profile, stats, featured_skills, featured_projects } = homepageData

  return (
    <div className="min-h-screen">
      {/* Hero Section - Now using ProfileHero component */}
      <ProfileHero profile={profile} stats={stats} />

      {/* Skills Section - Now using SkillsGrid component */}
      <SkillsGrid 
        skills={featured_skills}
        title="Core Expertise"
        description="Combining technical proficiency with business acumen to deliver data-driven solutions that create measurable impact"
      />

      {/* Projects Section - Now using ProjectsGrid component */}
      <ProjectsGrid
        projects={featured_projects}
        title="Featured Projects"
        description="Showcasing impactful solutions that demonstrate expertise in data analysis, machine learning, and process automation"
      />

      {/* Call to Action Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
              Ready to Transform Your Business with Data?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Let's discuss how advanced analytics and AI can drive measurable results for your organization. 
              From strategy to implementation, I deliver solutions that create lasting impact.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary" className="bg-white text-blue-600 hover:bg-blue-50">
                <span>Get In Touch</span>
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="border-white text-white hover:bg-white hover:text-blue-600"
                onClick={() => window.open(profile?.resume_url || '/resume.pdf', '_blank')}
              >
                <Download className="w-4 h-4 mr-2" />
                <span>Download Resume</span>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* API Status Indicator (for development) */}
      {error && (
        <div className="fixed bottom-4 right-4 bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-2 rounded-lg shadow-lg">
          <p className="text-sm font-medium">⚠️ Using fallback data</p>
          <p className="text-xs">CMS API unavailable</p>
        </div>
      )}
    </div>
  )
}

export default Home