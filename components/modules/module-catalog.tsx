"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, Download, Star, Users, Zap } from "lucide-react"
import { apiClient } from "@/lib/api-client"
import { ModuleInstallDialog } from "./module-install-dialog"

interface AvailableModule {
  name: string
  display_name: string
  description: string
  version: string
  category: string
  features: string[]
  required_config: string[]
  api_requirements: string[]
}

const moduleIcons: Record<string, string> = {
  google_analytics: "📊",
  seo_optimizer: "🔍",
  social_media: "📱",
  email_marketing: "📧",
  backup_manager: "💾",
}

const categoryColors: Record<string, string> = {
  Analytics: "bg-chart-1 text-white",
  SEO: "bg-chart-2 text-black",
  Marketing: "bg-chart-3 text-white",
  Utilities: "bg-chart-4 text-black",
}

export function ModuleCatalog() {
  const [modules, setModules] = useState<AvailableModule[]>([])
  const [filteredModules, setFilteredModules] = useState<AvailableModule[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [installModule, setInstallModule] = useState<AvailableModule | null>(null)

  useEffect(() => {
    loadAvailableModules()
  }, [])

  useEffect(() => {
    filterModules()
  }, [modules, searchTerm, categoryFilter])

  const loadAvailableModules = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getAvailableModules()
      if (response.data) {
        setModules(response.data)
      }
    } catch (error) {
      console.error("Error loading available modules:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const filterModules = () => {
    let filtered = modules

    if (searchTerm) {
      filtered = filtered.filter(
        (module) =>
          module.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          module.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
          module.features.some((feature) => feature.toLowerCase().includes(searchTerm.toLowerCase())),
      )
    }

    if (categoryFilter !== "all") {
      filtered = filtered.filter((module) => module.category === categoryFilter)
    }

    setFilteredModules(filtered)
  }

  const categories = Array.from(new Set(modules.map((m) => m.category)))

  if (isLoading) {
    return <div className="text-center py-8">Loading module catalog...</div>
  }

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Browse Modules</CardTitle>
          <CardDescription>Discover and install modules to extend your CMS functionality</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search modules..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-full sm:w-48">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Module Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Modules</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{modules.length}</div>
          </CardContent>
        </Card>

        {categories.slice(0, 3).map((category) => (
          <Card key={category}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{category}</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{modules.filter((m) => m.category === category).length}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Module Grid */}
      {filteredModules.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-lg font-medium mb-2">No Modules Found</h3>
            <p className="text-muted-foreground">Try adjusting your search terms or filters</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredModules.map((module) => (
            <Card key={module.name} className="relative hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <div className="text-2xl">{moduleIcons[module.name] || "🔧"}</div>
                    <div className="flex-1">
                      <CardTitle className="text-lg">{module.display_name}</CardTitle>
                      <CardDescription className="mt-1">{module.description}</CardDescription>
                    </div>
                  </div>
                  <Badge className={categoryColors[module.category] || "bg-muted"}>{module.category}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Features */}
                <div>
                  <h4 className="text-sm font-medium mb-2">Features</h4>
                  <div className="flex flex-wrap gap-1">
                    {module.features.slice(0, 3).map((feature, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {feature}
                      </Badge>
                    ))}
                    {module.features.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{module.features.length - 3} more
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Requirements */}
                {module.api_requirements.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium mb-2">Requirements</h4>
                    <div className="text-sm text-muted-foreground">Requires: {module.api_requirements.join(", ")}</div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center gap-2">
                    <Star className="h-4 w-4 text-chart-2" />
                    <span className="text-sm text-muted-foreground">v{module.version}</span>
                  </div>
                  <Button onClick={() => setInstallModule(module)} className="gap-2">
                    <Download className="h-4 w-4" />
                    Install
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Install Dialog */}
      {installModule && (
        <ModuleInstallDialog
          module={installModule}
          open={!!installModule}
          onOpenChange={(open) => !open && setInstallModule(null)}
          onInstall={() => {
            setInstallModule(null)
            // Optionally refresh or show success message
          }}
        />
      )}
    </div>
  )
}
