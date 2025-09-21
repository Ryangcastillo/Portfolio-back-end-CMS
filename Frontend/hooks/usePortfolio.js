import { useState, useEffect } from 'react'
import portfolioAPI, { withErrorHandling } from '../services/portfolioAPI'

// Hook for fetching homepage data
export const useHomepageData = () => {
  const [data, setData] = useState({
    profile: null,
    stats: [],
    featured_skills: [],
    featured_projects: []
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const homepageData = await portfolioAPI.getHomepageData()
        setData(homepageData)
      } catch (err) {
        setError(err)
        console.error('Failed to fetch homepage data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return { data, loading, error, refetch: () => fetchData() }
}

// Hook for fetching skills
export const useSkills = (params = {}) => {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchSkills = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const skillsData = await portfolioAPI.getSkills(params)
        setSkills(skillsData)
      } catch (err) {
        setError(err)
        console.error('Failed to fetch skills:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchSkills()
  }, [JSON.stringify(params)])

  return { skills, loading, error }
}

// Hook for fetching projects
export const useProjects = (params = {}) => {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const projectsData = await portfolioAPI.getProjects(params)
        setProjects(projectsData)
      } catch (err) {
        setError(err)
        console.error('Failed to fetch projects:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchProjects()
  }, [JSON.stringify(params)])

  return { projects, loading, error }
}

// Hook for fetching single project
export const useProject = (projectId) => {
  const [project, setProject] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!projectId) return

    const fetchProject = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const projectData = await portfolioAPI.getProject(projectId)
        setProject(projectData)
      } catch (err) {
        setError(err)
        console.error('Failed to fetch project:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchProject()
  }, [projectId])

  return { project, loading, error }
}

// Hook for fetching experience
export const useExperience = (params = {}) => {
  const [experience, setExperience] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchExperience = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const experienceData = await portfolioAPI.getExperience(params)
        setExperience(experienceData)
      } catch (err) {
        setError(err)
        console.error('Failed to fetch experience:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchExperience()
  }, [JSON.stringify(params)])

  return { experience, loading, error }
}

// Hook for fetching testimonials
export const useTestimonials = (params = {}) => {
  const [testimonials, setTestimonials] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchTestimonials = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const testimonialsData = await portfolioAPI.getTestimonials(params)
        setTestimonials(testimonialsData)
      } catch (err) {
        setError(err)
        console.error('Failed to fetch testimonials:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchTestimonials()
  }, [JSON.stringify(params)])

  return { testimonials, loading, error }
}

// Hook with fallback to hardcoded data for development
export const useHomepageDataWithFallback = () => {
  const { data, loading, error } = useHomepageData()
  
  // Fallback hardcoded data (from original Home.jsx)
  const fallbackData = {
    profile: {
      full_name: "Ryan Castillo",
      title: "Data Analyst",
      bio_description: "Transforming business challenges into actionable insights through advanced analytics and AI innovation. 8+ years of experience delivering measurable business value through data-driven solutions.",
      availability_status: "Available for New Opportunities",
      location: "Auckland, New Zealand",
      years_experience: 8
    },
    stats: [
      { id: 1, metric_name: "Years Experience", metric_value: "8+" },
      { id: 2, metric_name: "Cost Savings", metric_value: "$500K+" },
      { id: 3, metric_name: "Projects Delivered", metric_value: "50+" }
    ],
    featured_skills: [
      {
        id: 1,
        title: "Data Analysis & Visualization",
        description: "Power BI, SQL, Advanced Excel, Statistical Analysis",
        icon_name: "BarChart3",
        color_gradient: "from-blue-500 to-blue-600",
        projects_count: "15+ projects",
        impact_metric: "$500K+ savings"
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
        description: "Comprehensive Power BI dashboard analyzing supplier performance and identifying cost optimization opportunities across multiple business units.",
        impact_metric: "$200K annual savings",
        technologies: ["Power BI", "SQL", "SAP FICO"],
        category: "Data Analysis",
        link: "/data-analysis"
      },
      {
        id: 2,
        title: "Predictive Maintenance Model",
        description: "Machine learning model predicting equipment failures 2 weeks in advance, enabling proactive maintenance scheduling and reducing downtime.",
        impact_metric: "85% prediction accuracy",
        technologies: ["Python", "Scikit-learn", "Pandas"],
        category: "Machine Learning",
        link: "/machine-learning"
      },
      {
        id: 3,
        title: "AI-Powered Process Automation",
        description: "Intelligent chatbot system for automating vendor inquiries and procurement process guidance, improving response times and accuracy.",
        impact_metric: "60% faster responses",
        technologies: ["OpenAI API", "React", "Node.js"],
        category: "AI Agents",
        link: "/ai-agents"
      }
    ]
  }

  // Return API data if available, otherwise fallback data
  if (error || !data.profile) {
    return { 
      data: fallbackData, 
      loading: false, 
      error, 
      usingFallback: true 
    }
  }

  return { 
    data, 
    loading, 
    error, 
    usingFallback: false 
  }
}