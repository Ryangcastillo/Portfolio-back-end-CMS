"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { apiClient } from "@/lib/api-client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { 
  Github, 
  ExternalLink, 
  Mail, 
  Linkedin, 
  Globe, 
  Calendar,
  MapPin,
  Star,
  ArrowLeft
} from "lucide-react"

interface Project {
  id: number
  title: string
  description: string
  technologies: string[]
  github_url?: string
  demo_url?: string
  image_url?: string
  start_date?: string
  end_date?: string
  featured: boolean
}

interface Skill {
  id: number
  name: string
  category: string
  level: number
  years_of_experience?: number
}

interface Experience {
  id: number
  company: string
  position: string
  description: string
  start_date: string
  end_date?: string
  location?: string
  is_current: boolean
}

interface PortfolioSummary {
  name: string
  title: string
  bio: string
  email: string
  linkedin_url?: string
  github_url?: string
  website_url?: string
  resume_url?: string
}

export default function PortfolioPage() {
  const [summary, setSummary] = useState<PortfolioSummary | null>(null)
  const [projects, setProjects] = useState<Project[]>([])
  const [skills, setSkills] = useState<Skill[]>([])
  const [experience, setExperience] = useState<Experience[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPortfolioData()
  }, [])

  const fetchPortfolioData = async () => {
    try {
      setLoading(true)
      
      // Fetch all portfolio data using API client
      const [summaryResult, projectsResult, skillsResult, experienceResult] = await Promise.all([
        apiClient.getPortfolioSummary(),
        apiClient.getPortfolioProjects(),
        apiClient.getPortfolioSkills(),
        apiClient.getPortfolioExperience()
      ])

      if (summaryResult.data) setSummary(summaryResult.data)
      if (projectsResult.data) setProjects(projectsResult.data)
      if (skillsResult.data) setSkills(skillsResult.data)
      if (experienceResult.data) setExperience(experienceResult.data)
    } catch (error) {
      console.error("Failed to fetch portfolio data:", error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", { 
      year: "numeric", 
      month: "short" 
    })
  }

  const getSkillsByCategory = (category: string) => {
    return skills.filter(skill => skill.category === category)
  }

  const renderSkillLevel = (level: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star 
        key={i} 
        className={`h-4 w-4 ${i < level ? "fill-yellow-400 text-yellow-400" : "text-gray-300"}`} 
      />
    ))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading portfolio...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2 text-muted-foreground hover:text-foreground">
            <ArrowLeft className="h-4 w-4" />
            <span>Back to CMS</span>
          </Link>
          <div className="flex items-center space-x-4">
            {summary?.resume_url && (
              <Button variant="outline" asChild>
                <a href={summary.resume_url} target="_blank" rel="noopener noreferrer">
                  Download Resume
                </a>
              </Button>
            )}
            <Button asChild>
              <a href={`mailto:${summary?.email}`}>
                Get in Touch
              </a>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-4xl text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-foreground mb-6">
            {summary?.name || "Your Name"}
          </h1>
          <p className="text-2xl text-primary mb-6">
            {summary?.title || "Full Stack Developer"}
          </p>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            {summary?.bio || "Passionate developer building amazing web applications."}
          </p>
          
          {/* Social Links */}
          <div className="flex justify-center space-x-4 mb-8">
            {summary?.email && (
              <Button size="sm" variant="outline" asChild>
                <a href={`mailto:${summary.email}`} className="flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <span>Email</span>
                </a>
              </Button>
            )}
            {summary?.github_url && (
              <Button size="sm" variant="outline" asChild>
                <a href={summary.github_url} target="_blank" rel="noopener noreferrer" className="flex items-center space-x-2">
                  <Github className="h-4 w-4" />
                  <span>GitHub</span>
                </a>
              </Button>
            )}
            {summary?.linkedin_url && (
              <Button size="sm" variant="outline" asChild>
                <a href={summary.linkedin_url} target="_blank" rel="noopener noreferrer" className="flex items-center space-x-2">
                  <Linkedin className="h-4 w-4" />
                  <span>LinkedIn</span>
                </a>
              </Button>
            )}
            {summary?.website_url && (
              <Button size="sm" variant="outline" asChild>
                <a href={summary.website_url} target="_blank" rel="noopener noreferrer" className="flex items-center space-x-2">
                  <Globe className="h-4 w-4" />
                  <span>Website</span>
                </a>
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Featured Projects Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-12">Featured Projects</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {projects.filter(p => p.featured).map((project) => (
              <Card key={project.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start mb-2">
                    <CardTitle className="text-lg">{project.title}</CardTitle>
                    <Badge variant="secondary">Featured</Badge>
                  </div>
                  <CardDescription className="line-clamp-3">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {project.technologies.slice(0, 3).map((tech) => (
                      <Badge key={tech} variant="outline" className="text-xs">
                        {tech}
                      </Badge>
                    ))}
                    {project.technologies.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{project.technologies.length - 3} more
                      </Badge>
                    )}
                  </div>
                  <div className="flex space-x-2">
                    {project.github_url && (
                      <Button size="sm" variant="outline" asChild>
                        <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                          <Github className="h-4 w-4 mr-1" />
                          Code
                        </a>
                      </Button>
                    )}
                    {project.demo_url && (
                      <Button size="sm" asChild>
                        <a href={project.demo_url} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="h-4 w-4 mr-1" />
                          Demo
                        </a>
                      </Button>
                    )}
                  </div>
                  {project.start_date && (
                    <div className="flex items-center text-sm text-muted-foreground mt-4">
                      <Calendar className="h-4 w-4 mr-1" />
                      {formatDate(project.start_date)}
                      {project.end_date ? ` - ${formatDate(project.end_date)}` : " - Present"}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
          
          {projects.filter(p => !p.featured).length > 0 && (
            <div className="text-center mt-8">
              <Button variant="outline">
                View All Projects ({projects.length})
              </Button>
            </div>
          )}
        </div>
      </section>

      {/* Skills Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-12">Technical Skills</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {["Frontend", "Backend", "Database", "DevOps"].map((category) => {
              const categorySkills = getSkillsByCategory(category)
              if (categorySkills.length === 0) return null
              
              return (
                <Card key={category}>
                  <CardHeader>
                    <CardTitle className="text-lg">{category}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {categorySkills.map((skill) => (
                        <div key={skill.id}>
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-sm font-medium">{skill.name}</span>
                            {skill.years_of_experience && (
                              <span className="text-xs text-muted-foreground">
                                {skill.years_of_experience}y
                              </span>
                            )}
                          </div>
                          <div className="flex space-x-1">
                            {renderSkillLevel(skill.level)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Experience Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-3xl font-bold text-center mb-12">Work Experience</h2>
          <div className="space-y-8">
            {experience.map((exp, index) => (
              <Card key={exp.id}>
                <CardContent className="pt-6">
                  <div className="flex flex-col md:flex-row md:justify-between md:items-start mb-4">
                    <div>
                      <h3 className="text-xl font-semibold">{exp.position}</h3>
                      <p className="text-lg text-primary">{exp.company}</p>
                    </div>
                    <div className="flex flex-col md:text-right text-sm text-muted-foreground">
                      <div className="flex items-center md:justify-end">
                        <Calendar className="h-4 w-4 mr-1" />
                        {formatDate(exp.start_date)} - {exp.is_current ? "Present" : (exp.end_date ? formatDate(exp.end_date) : "Present")}
                      </div>
                      {exp.location && (
                        <div className="flex items-center md:justify-end mt-1">
                          <MapPin className="h-4 w-4 mr-1" />
                          {exp.location}
                        </div>
                      )}
                    </div>
                  </div>
                  <p className="text-muted-foreground">{exp.description}</p>
                  {index < experience.length - 1 && <Separator className="mt-6" />}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center max-w-2xl">
          <h2 className="text-3xl font-bold mb-6">Let's Work Together</h2>
          <p className="text-lg text-muted-foreground mb-8">
            I'm always interested in new opportunities and interesting projects. 
            Let's discuss how we can bring your ideas to life.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <a href={`mailto:${summary?.email}`}>
                <Mail className="h-4 w-4 mr-2" />
                Get in Touch
              </a>
            </Button>
            {summary?.resume_url && (
              <Button size="lg" variant="outline" asChild>
                <a href={summary.resume_url} target="_blank" rel="noopener noreferrer">
                  Download Resume
                </a>
              </Button>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}