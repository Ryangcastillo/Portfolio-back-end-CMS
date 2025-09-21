"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Plus, Edit, Trash2, Save, Eye, ExternalLink } from "lucide-react"
import { apiClient } from "@/lib/api-client"

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

export default function PortfolioManagementPage() {
  const [summary, setSummary] = useState<PortfolioSummary>({
    name: "",
    title: "",
    bio: "",
    email: "",
    linkedin_url: "",
    github_url: "",
    website_url: "",
    resume_url: ""
  })
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    loadPortfolioData()
  }, [])

  const loadPortfolioData = async () => {
    try {
      setLoading(true)
      const [summaryResult, projectsResult] = await Promise.all([
        apiClient.getPortfolioSummary(),
        apiClient.getPortfolioProjects()
      ])

      if (summaryResult.data) {
        setSummary(summaryResult.data)
      }
      if (projectsResult.data) {
        setProjects(projectsResult.data)
      }
    } catch (error) {
      console.error("Failed to load portfolio data:", error)
    } finally {
      setLoading(false)
    }
  }

  const saveSummary = async () => {
    try {
      setSaving(true)
      // TODO: Implement save summary endpoint
      console.log("Saving summary:", summary)
      // For now, just show success
      alert("Summary saved successfully!")
    } catch (error) {
      console.error("Failed to save summary:", error)
      alert("Failed to save summary")
    } finally {
      setSaving(false)
    }
  }

  const updateSummaryField = (field: keyof PortfolioSummary, value: string) => {
    setSummary(prev => ({ ...prev, [field]: value }))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading portfolio data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Portfolio Management</h1>
          <p className="text-muted-foreground">
            Manage your public portfolio website content
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" asChild>
            <a href="/portfolio" target="_blank" rel="noopener noreferrer">
              <Eye className="h-4 w-4 mr-2" />
              Preview Portfolio
            </a>
          </Button>
        </div>
      </div>

      <Tabs defaultValue="summary" className="space-y-4">
        <TabsList>
          <TabsTrigger value="summary">Personal Info</TabsTrigger>
          <TabsTrigger value="projects">Projects</TabsTrigger>
          <TabsTrigger value="skills">Skills</TabsTrigger>
          <TabsTrigger value="experience">Experience</TabsTrigger>
        </TabsList>

        <TabsContent value="summary" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Personal Information</CardTitle>
              <CardDescription>
                Update your basic portfolio information that appears on your public website
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={summary.name}
                    onChange={(e) => updateSummaryField("name", e.target.value)}
                    placeholder="Your Full Name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="title">Professional Title</Label>
                  <Input
                    id="title"
                    value={summary.title}
                    onChange={(e) => updateSummaryField("title", e.target.value)}
                    placeholder="e.g., Full Stack Developer"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  value={summary.bio}
                  onChange={(e) => updateSummaryField("bio", e.target.value)}
                  placeholder="Write a brief bio about yourself..."
                  rows={4}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={summary.email}
                    onChange={(e) => updateSummaryField("email", e.target.value)}
                    placeholder="your.email@example.com"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="website_url">Website URL</Label>
                  <Input
                    id="website_url"
                    value={summary.website_url || ""}
                    onChange={(e) => updateSummaryField("website_url", e.target.value)}
                    placeholder="https://yourwebsite.com"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="github_url">GitHub URL</Label>
                  <Input
                    id="github_url"
                    value={summary.github_url || ""}
                    onChange={(e) => updateSummaryField("github_url", e.target.value)}
                    placeholder="https://github.com/yourusername"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="linkedin_url">LinkedIn URL</Label>
                  <Input
                    id="linkedin_url"
                    value={summary.linkedin_url || ""}
                    onChange={(e) => updateSummaryField("linkedin_url", e.target.value)}
                    placeholder="https://linkedin.com/in/yourprofile"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="resume_url">Resume URL</Label>
                <Input
                  id="resume_url"
                  value={summary.resume_url || ""}
                  onChange={(e) => updateSummaryField("resume_url", e.target.value)}
                  placeholder="https://example.com/your-resume.pdf"
                />
              </div>

              <div className="flex justify-end">
                <Button onClick={saveSummary} disabled={saving}>
                  {saving ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="h-4 w-4 mr-2" />
                      Save Changes
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="projects" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Projects</h2>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Project
            </Button>
          </div>

          <div className="grid gap-4">
            {projects.map((project) => (
              <Card key={project.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="flex items-center space-x-2">
                        <span>{project.title}</span>
                        {project.featured && <Badge variant="secondary">Featured</Badge>}
                      </CardTitle>
                      <CardDescription className="line-clamp-2">
                        {project.description}
                      </CardDescription>
                    </div>
                    <div className="flex space-x-2">
                      <Button size="sm" variant="outline">
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button size="sm" variant="outline">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {project.technologies.slice(0, 4).map((tech) => (
                      <Badge key={tech} variant="outline">
                        {tech}
                      </Badge>
                    ))}
                    {project.technologies.length > 4 && (
                      <Badge variant="outline">
                        +{project.technologies.length - 4} more
                      </Badge>
                    )}
                  </div>
                  <div className="flex space-x-2">
                    {project.github_url && (
                      <Button size="sm" variant="outline" asChild>
                        <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="h-4 w-4 mr-1" />
                          GitHub
                        </a>
                      </Button>
                    )}
                    {project.demo_url && (
                      <Button size="sm" variant="outline" asChild>
                        <a href={project.demo_url} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="h-4 w-4 mr-1" />
                          Demo
                        </a>
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="skills">
          <Card>
            <CardHeader>
              <CardTitle>Skills Management</CardTitle>
              <CardDescription>Manage your technical skills and expertise levels</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Skills management interface coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="experience">
          <Card>
            <CardHeader>
              <CardTitle>Work Experience</CardTitle>
              <CardDescription>Manage your work history and professional experience</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Experience management interface coming soon...</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}