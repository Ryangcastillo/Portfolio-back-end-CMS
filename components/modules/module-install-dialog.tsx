"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Download, CheckCircle, AlertCircle, Zap } from "lucide-react"
import { apiClient } from "@/lib/api-client"

interface ModuleInstallDialogProps {
  module: {
    name: string
    display_name: string
    description: string
    version: string
    category: string
    features: string[]
    required_config: string[]
    api_requirements: string[]
  }
  open: boolean
  onOpenChange: (open: boolean) => void
  onInstall: () => void
}

export function ModuleInstallDialog({ module, open, onOpenChange, onInstall }: ModuleInstallDialogProps) {
  const [isInstalling, setIsInstalling] = useState(false)
  const [installStep, setInstallStep] = useState<"confirm" | "installing" | "success">("confirm")

  const handleInstall = async () => {
    setIsInstalling(true)
    setInstallStep("installing")

    try {
      // Simulate installation steps
      await new Promise((resolve) => setTimeout(resolve, 1000))

      const response = await apiClient.installModule(module.name, {
        name: module.name,
        description: module.description,
        version: module.version,
        configuration: {},
        api_keys: {},
      })

      if (response.data) {
        setInstallStep("success")
        setTimeout(() => {
          onInstall()
          onOpenChange(false)
        }, 2000)
      }
    } catch (error) {
      console.error("Error installing module:", error)
      setInstallStep("confirm")
    } finally {
      setIsInstalling(false)
    }
  }

  const renderContent = () => {
    switch (installStep) {
      case "installing":
        return (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <h3 className="text-lg font-medium mb-2">Installing {module.display_name}</h3>
            <p className="text-muted-foreground">Please wait while we install the module...</p>
          </div>
        )

      case "success":
        return (
          <div className="text-center py-8">
            <CheckCircle className="h-12 w-12 text-chart-1 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">Installation Complete!</h3>
            <p className="text-muted-foreground">
              {module.display_name} has been successfully installed. You can now configure it in the installed modules
              section.
            </p>
          </div>
        )

      default:
        return (
          <div className="space-y-6">
            {/* Module Info */}
            <div className="flex items-start gap-4">
              <div className="text-3xl">🔧</div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="text-lg font-medium">{module.display_name}</h3>
                  <Badge>{module.category}</Badge>
                  <Badge variant="outline">v{module.version}</Badge>
                </div>
                <p className="text-muted-foreground">{module.description}</p>
              </div>
            </div>

            <Separator />

            {/* Features */}
            <div>
              <h4 className="font-medium mb-3 flex items-center gap-2">
                <Zap className="h-4 w-4" />
                Features
              </h4>
              <div className="grid gap-2">
                {module.features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-chart-1" />
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Requirements */}
            {(module.required_config.length > 0 || module.api_requirements.length > 0) && (
              <>
                <Separator />
                <div>
                  <h4 className="font-medium mb-3 flex items-center gap-2">
                    <AlertCircle className="h-4 w-4" />
                    Requirements
                  </h4>

                  {module.api_requirements.length > 0 && (
                    <Alert className="mb-3">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        <strong>API Keys Required:</strong> This module requires the following API keys to function:
                        <ul className="list-disc list-inside mt-2">
                          {module.api_requirements.map((req, index) => (
                            <li key={index} className="text-sm">
                              {req.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                            </li>
                          ))}
                        </ul>
                      </AlertDescription>
                    </Alert>
                  )}

                  {module.required_config.length > 0 && (
                    <div>
                      <p className="text-sm text-muted-foreground mb-2">Configuration required:</p>
                      <div className="grid gap-1">
                        {module.required_config.map((config, index) => (
                          <div key={index} className="flex items-center gap-2">
                            <div className="h-2 w-2 rounded-full bg-chart-2" />
                            <span className="text-sm">
                              {config.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}

            {/* Installation Note */}
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                After installation, you'll need to configure the module with your API keys and settings before it can be
                activated.
              </AlertDescription>
            </Alert>
          </div>
        )
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {installStep === "confirm" && `Install ${module.display_name}`}
            {installStep === "installing" && "Installing Module"}
            {installStep === "success" && "Installation Complete"}
          </DialogTitle>
          {installStep === "confirm" && (
            <DialogDescription>Review the module details before installation</DialogDescription>
          )}
        </DialogHeader>

        {renderContent()}

        {installStep === "confirm" && (
          <DialogFooter>
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button onClick={handleInstall} disabled={isInstalling} className="gap-2">
              <Download className="h-4 w-4" />
              Install Module
            </Button>
          </DialogFooter>
        )}
      </DialogContent>
    </Dialog>
  )
}
