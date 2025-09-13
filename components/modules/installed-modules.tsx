"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { MoreHorizontal, Settings, Trash2, CheckCircle, AlertCircle } from "lucide-react"
import { apiClient } from "@/lib/api-client"
import { ModuleConfigDialog } from "./module-config-dialog"

interface InstalledModule {
  id: number
  name: string
  description: string
  version: string
  is_active: boolean
  has_api_keys: boolean
  created_at: string
  updated_at?: string
}

const moduleIcons: Record<string, string> = {
  google_analytics: "📊",
  seo_optimizer: "🔍",
  social_media: "📱",
  email_marketing: "📧",
  backup_manager: "💾",
}

export function InstalledModules() {
  const [modules, setModules] = useState<InstalledModule[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [configModule, setConfigModule] = useState<InstalledModule | null>(null)

  useEffect(() => {
    loadInstalledModules()
  }, [])

  const loadInstalledModules = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getInstalledModules()
      if (response.data) {
        setModules(response.data)
      }
    } catch (error) {
      console.error("Error loading installed modules:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleToggleModule = async (moduleId: number, isActive: boolean) => {
    try {
      if (isActive) {
        await apiClient.activateModule(moduleId)
      } else {
        await apiClient.deactivateModule(moduleId)
      }
      await loadInstalledModules()
    } catch (error) {
      console.error("Error toggling module:", error)
    }
  }

  const handleUninstallModule = async (moduleId: number) => {
    if (!confirm("Are you sure you want to uninstall this module? This action cannot be undone.")) {
      return
    }

    try {
      await apiClient.uninstallModule(moduleId)
      await loadInstalledModules()
    } catch (error) {
      console.error("Error uninstalling module:", error)
    }
  }

  const getModuleStatus = (module: InstalledModule) => {
    if (!module.has_api_keys && requiresApiKeys(module.name)) {
      return { status: "needs_config", label: "Needs Configuration", color: "bg-chart-2 text-black" }
    }
    if (module.is_active) {
      return { status: "active", label: "Active", color: "bg-chart-1 text-white" }
    }
    return { status: "inactive", label: "Inactive", color: "bg-muted text-muted-foreground" }
  }

  const requiresApiKeys = (moduleName: string) => {
    return ["google_analytics", "seo_optimizer", "social_media", "email_marketing"].includes(moduleName)
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading installed modules...</div>
  }

  return (
    <div className="space-y-6">
      {modules.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <div className="text-6xl mb-4">📦</div>
            <h3 className="text-lg font-medium mb-2">No Modules Installed</h3>
            <p className="text-muted-foreground mb-4">Browse the module catalog to add functionality to your CMS</p>
            <Button>Browse Catalog</Button>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Status Overview */}
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Modules</CardTitle>
                <CheckCircle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{modules.length}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Modules</CardTitle>
                <CheckCircle className="h-4 w-4 text-chart-1" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{modules.filter((m) => m.is_active).length}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Need Configuration</CardTitle>
                <AlertCircle className="h-4 w-4 text-chart-2" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {modules.filter((m) => !m.has_api_keys && requiresApiKeys(m.name)).length}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Modules that need configuration */}
          {modules.some((m) => !m.has_api_keys && requiresApiKeys(m.name)) && (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Some modules require configuration before they can be activated. Click the settings icon to configure
                them.
              </AlertDescription>
            </Alert>
          )}

          {/* Module Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {modules.map((module) => {
              const status = getModuleStatus(module)
              return (
                <Card key={module.id} className="relative">
                  <CardHeader className="flex flex-row items-start justify-between space-y-0">
                    <div className="flex items-start gap-3">
                      <div className="text-2xl">{moduleIcons[module.name] || "🔧"}</div>
                      <div className="flex-1">
                        <CardTitle className="text-lg">
                          {module.name.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                        </CardTitle>
                        <CardDescription className="mt-1">{module.description}</CardDescription>
                      </div>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => setConfigModule(module)}>
                          <Settings className="h-4 w-4 mr-2" />
                          Configure
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleUninstallModule(module.id)} className="text-destructive">
                          <Trash2 className="h-4 w-4 mr-2" />
                          Uninstall
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Badge className={status.color}>{status.label}</Badge>
                      <span className="text-sm text-muted-foreground">v{module.version}</span>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Switch
                          checked={module.is_active}
                          onCheckedChange={(checked) => handleToggleModule(module.id, checked)}
                          disabled={!module.has_api_keys && requiresApiKeys(module.name)}
                        />
                        <span className="text-sm">{module.is_active ? "Active" : "Inactive"}</span>
                      </div>
                      <Button variant="outline" size="sm" onClick={() => setConfigModule(module)} className="gap-2">
                        <Settings className="h-3 w-3" />
                        Configure
                      </Button>
                    </div>

                    {status.status === "needs_config" && (
                      <div className="text-sm text-chart-2 flex items-center gap-2">
                        <AlertCircle className="h-3 w-3" />
                        Configuration required
                      </div>
                    )}
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </>
      )}

      {/* Configuration Dialog */}
      {configModule && (
        <ModuleConfigDialog
          module={configModule}
          open={!!configModule}
          onOpenChange={(open) => !open && setConfigModule(null)}
          onSave={loadInstalledModules}
        />
      )}
    </div>
  )
}
