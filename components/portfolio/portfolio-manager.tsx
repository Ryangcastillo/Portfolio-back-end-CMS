'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog'
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { 
  Plus, 
  Edit, 
  Trash2, 
  Save, 
  User, 
  BarChart3, 
  Wrench, 
  FolderOpen,
  Briefcase,
  MessageCircle,
  Eye
} from 'lucide-react'
import { toast } from 'sonner'

const PortfolioManager = () => {
  const [profileData, setProfileData] = useState(null)
  const [skills, setSkills] = useState([])
  const [projects, setProjects] = useState([])
  const [stats, setStats] = useState([])
  const [categories, setCategories] = useState([])
  const [experience, setExperience] = useState([])
  const [testimonials, setTestimonials] = useState([])
  const [loading, setLoading] = useState(true)
  const [editingItem, setEditingItem] = useState(null)
  const [dialogOpen, setDialogOpen] = useState(false)

  // Form states for different sections
  const [profileForm, setProfileForm] = useState({})
  const [skillForm, setSkillForm] = useState({})
  const [projectForm, setProjectForm] = useState({})

  useEffect(() => {
    fetchAllData()
  }, [])

  const fetchAllData = async () => {
    try {
      setLoading(true)
      
      // Fetch all portfolio data from admin endpoints
      const [profileRes, skillsRes, projectsRes, statsRes, categoriesRes, experienceRes, testimonialsRes] = 
        await Promise.all([
          fetch('/api/admin/portfolio/profile', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }),
          fetch('/api/admin/portfolio/skills', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }),
          fetch('/api/admin/portfolio/projects', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }),
          fetch('/api/admin/portfolio/stats', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }),
          fetch('/api/admin/portfolio/categories', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }),
          fetch('/api/admin/portfolio/experience', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }),
          fetch('/api/admin/portfolio/testimonials', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } })
        ])

      if (profileRes.ok) setProfileData(await profileRes.json())
      if (skillsRes.ok) setSkills(await skillsRes.json())
      if (projectsRes.ok) setProjects(await projectsRes.json())
      if (statsRes.ok) setStats(await statsRes.json())
      if (categoriesRes.ok) setCategories(await categoriesRes.json())
      if (experienceRes.ok) setExperience(await experienceRes.json())
      if (testimonialsRes.ok) setTestimonials(await testimonialsRes.json())

    } catch (error) {
      console.error('Error fetching data:', error)
      toast.error('Failed to load portfolio data')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveProfile = async (formData) => {
    try {
      const response = await fetch('/api/admin/portfolio/profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        const updatedProfile = await response.json()
        setProfileData(updatedProfile)
        toast.success('Profile updated successfully')
      } else {
        toast.error('Failed to update profile')
      }
    } catch (error) {
      console.error('Error saving profile:', error)
      toast.error('Failed to update profile')
    }
  }

  const handleSaveSkill = async (formData) => {
    try {
      const method = editingItem ? 'PUT' : 'POST'
      const url = editingItem 
        ? `/api/admin/portfolio/skills/${editingItem.id}`
        : '/api/admin/portfolio/skills'

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        await fetchAllData() // Refresh data
        setDialogOpen(false)
        setEditingItem(null)
        setSkillForm({})
        toast.success(`Skill ${editingItem ? 'updated' : 'created'} successfully`)
      } else {
        toast.error(`Failed to ${editingItem ? 'update' : 'create'} skill`)
      }
    } catch (error) {
      console.error('Error saving skill:', error)
      toast.error(`Failed to ${editingItem ? 'update' : 'create'} skill`)
    }
  }

  const handleDeleteItem = async (type, id) => {
    if (!confirm('Are you sure you want to delete this item?')) return

    try {
      const response = await fetch(`/api/admin/portfolio/${type}/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.ok) {
        await fetchAllData() // Refresh data
        toast.success('Item deleted successfully')
      } else {
        toast.error('Failed to delete item')
      }
    } catch (error) {
      console.error('Error deleting item:', error)
      toast.error('Failed to delete item')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Portfolio Management</h2>
          <p className="text-muted-foreground">Manage your portfolio content for the public website</p>
        </div>
        <Button onClick={() => window.open('/api/public/homepage-data', '_blank')} variant="outline">
          <Eye className="h-4 w-4 mr-2" />
          Preview Public Data
        </Button>
      </div>

      <Tabs defaultValue="profile" className="space-y-4">
        <TabsList>
          <TabsTrigger value="profile"><User className="h-4 w-4 mr-2" />Profile</TabsTrigger>
          <TabsTrigger value="stats"><BarChart3 className="h-4 w-4 mr-2" />Stats</TabsTrigger>
          <TabsTrigger value="skills"><Wrench className="h-4 w-4 mr-2" />Skills</TabsTrigger>
          <TabsTrigger value="projects"><FolderOpen className="h-4 w-4 mr-2" />Projects</TabsTrigger>
          <TabsTrigger value="experience"><Briefcase className="h-4 w-4 mr-2" />Experience</TabsTrigger>
          <TabsTrigger value="testimonials"><MessageCircle className="h-4 w-4 mr-2" />Testimonials</TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <CardDescription>Main profile details displayed on your portfolio</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="full_name">Full Name</Label>
                  <Input
                    id="full_name"
                    value={profileForm.full_name || profileData?.full_name || ''}
                    onChange={(e) => setProfileForm({...profileForm, full_name: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="title">Professional Title</Label>
                  <Input
                    id="title"
                    value={profileForm.title || profileData?.title || ''}
                    onChange={(e) => setProfileForm({...profileForm, title: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="years_experience">Years of Experience</Label>
                  <Input
                    id="years_experience"
                    type="number"
                    value={profileForm.years_experience || profileData?.years_experience || ''}
                    onChange={(e) => setProfileForm({...profileForm, years_experience: parseInt(e.target.value)})}
                  />
                </div>
                <div>
                  <Label htmlFor="availability_status">Availability Status</Label>
                  <Input
                    id="availability_status"
                    value={profileForm.availability_status || profileData?.availability_status || ''}
                    onChange={(e) => setProfileForm({...profileForm, availability_status: e.target.value})}
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="bio_description">Bio Description</Label>
                <Textarea
                  id="bio_description"
                  rows={4}
                  value={profileForm.bio_description || profileData?.bio_description || ''}
                  onChange={(e) => setProfileForm({...profileForm, bio_description: e.target.value})}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={profileForm.email || profileData?.email || ''}
                    onChange={(e) => setProfileForm({...profileForm, email: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="location">Location</Label>
                  <Input
                    id="location"
                    value={profileForm.location || profileData?.location || ''}
                    onChange={(e) => setProfileForm({...profileForm, location: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="linkedin_url">LinkedIn URL</Label>
                  <Input
                    id="linkedin_url"
                    value={profileForm.linkedin_url || profileData?.linkedin_url || ''}
                    onChange={(e) => setProfileForm({...profileForm, linkedin_url: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="github_url">GitHub URL</Label>
                  <Input
                    id="github_url"
                    value={profileForm.github_url || profileData?.github_url || ''}
                    onChange={(e) => setProfileForm({...profileForm, github_url: e.target.value})}
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button onClick={() => handleSaveProfile(profileForm)}>
                  <Save className="h-4 w-4 mr-2" />
                  Save Profile
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Skills Tab */}
        <TabsContent value="skills">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Skills Management</CardTitle>
                  <CardDescription>Manage your skills and expertise areas</CardDescription>
                </div>
                <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                  <DialogTrigger asChild>
                    <Button onClick={() => { setEditingItem(null); setSkillForm({}) }}>
                      <Plus className="h-4 w-4 mr-2" />
                      Add Skill
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>{editingItem ? 'Edit' : 'Add'} Skill</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                      <div>
                        <Label htmlFor="skill_title">Title</Label>
                        <Input
                          id="skill_title"
                          value={skillForm.title || ''}
                          onChange={(e) => setSkillForm({...skillForm, title: e.target.value})}
                        />
                      </div>
                      <div>
                        <Label htmlFor="skill_description">Description</Label>
                        <Textarea
                          id="skill_description"
                          value={skillForm.description || ''}
                          onChange={(e) => setSkillForm({...skillForm, description: e.target.value})}
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <Label htmlFor="projects_count">Projects Count</Label>
                          <Input
                            id="projects_count"
                            value={skillForm.projects_count || ''}
                            onChange={(e) => setSkillForm({...skillForm, projects_count: e.target.value})}
                            placeholder="e.g., 15+ projects"
                          />
                        </div>
                        <div>
                          <Label htmlFor="impact_metric">Impact Metric</Label>
                          <Input
                            id="impact_metric"
                            value={skillForm.impact_metric || ''}
                            onChange={(e) => setSkillForm({...skillForm, impact_metric: e.target.value})}
                            placeholder="e.g., $500K+ savings"
                          />
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="is_featured"
                          checked={skillForm.is_featured || false}
                          onCheckedChange={(checked) => setSkillForm({...skillForm, is_featured: checked})}
                        />
                        <Label htmlFor="is_featured">Featured Skill</Label>
                      </div>
                    </div>
                    <DialogFooter>
                      <Button onClick={() => handleSaveSkill(skillForm)}>
                        {editingItem ? 'Update' : 'Create'} Skill
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Title</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Projects</TableHead>
                    <TableHead>Impact</TableHead>
                    <TableHead>Featured</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {skills.map((skill) => (
                    <TableRow key={skill.id}>
                      <TableCell className="font-medium">{skill.title}</TableCell>
                      <TableCell>
                        {skill.category && <Badge variant="outline">{skill.category}</Badge>}
                      </TableCell>
                      <TableCell>{skill.projects_count}</TableCell>
                      <TableCell>{skill.impact_metric}</TableCell>
                      <TableCell>
                        {skill.is_featured && <Badge>Featured</Badge>}
                      </TableCell>
                      <TableCell>
                        <div className="flex space-x-2">
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => {
                              setEditingItem(skill)
                              setSkillForm(skill)
                              setDialogOpen(true)
                            }}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => handleDeleteItem('skills', skill.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Add other tabs similarly... */}
      </Tabs>
    </div>
  )
}

export default PortfolioManager