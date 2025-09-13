"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Save, Key, AlertCircle } from "lucide-react"
import { apiClient } from "@/lib/api-client"

interface ModuleConfigDialogProps {
  module: {
    id: number
    name: string
    description: string
    version: string
    is_active: boolean
    has_api_keys: boolean
  }
  open: boolean
  onOpenChange: (open: boolean) => void
  onSave: () => void
}

const moduleConfigs: Record<string, any> = {
  google_analytics: {
    fields: [
      { key: "tracking_id", label: "Tracking ID", type: "text", required: true, placeholder: "GA-XXXXXXXXX-X" },
      { key: "enhanced_ecommerce", label: "Enhanced E-commerce", type: "boolean", default: false },
    ],
    apiKeys: [{ key: "google_analytics_key", label: "Google Analytics API Key", required: true }],
  },
  seo_optimizer: {
    fields: [
      {
        key: "target_keywords",
        label: "Target Keywords",
        type: "textarea",
        placeholder: "keyword1, keyword2, keyword3",
      },
      { key: "auto_optimize", label: "Auto Optimize", type: "boolean", default: true },
    ],
    apiKeys: [{ key: "seo_api_key", label: "SEO API Key", required: true }],
  },
  social_media: {
    fields: [
      { key: "platforms", label: "Platforms", type: "text", placeholder: "twitter,facebook,linkedin" },
      { key: "auto_post", label: "Auto Post", type: "boolean", default: false },
    ],
    apiKeys: [
      { key: "twitter_api_key", label: "Twitter API Key", required: false },
      { key: "facebook_api_key", label: "Facebook API Key", required: false },
    ],
  },
  email_marketing: {
    fields: [
      { key: "sender_email", label: "Sender Email", type: "email", required: true },
      { key: "list_name", label: "Default List Name", type: "text", placeholder: "Newsletter" },
    ],
    apiKeys: [{ key: "mailchimp_api_key", label: "Mailchimp API Key", required: true }],
  },
  backup_manager: {
    fields: [
      {
        key: "backup_frequency",
        label: "Backup Frequency",
        type: "select",
        options: ["daily", "weekly", "monthly"],
        default: "weekly",
      },
      { key: "retention_days", label: "Retention Days", type: "number", default: 30 },
    ],
    apiKeys: [{ key: "cloud_storage_key", label: "Cloud Storage API Key", required: true }],
  },
}

export function ModuleConfigDialog({ module, open, onOpenChange, onSave }: ModuleConfigDialogProps) {
  const [configuration, setConfiguration] = useState<Record<string, any>>({})
  const [apiKeys, setApiKeys] = useState<Record<string, string>>({})
  const [isActive, setIsActive] = useState(module.is_active)
  const [isSaving, setIsSaving] = useState(false)

  const moduleConfig = moduleConfigs[module.name] || { fields: [], apiKeys: [] }

  useEffect(() => {
    // Initialize with default values
    const defaultConfig: Record<string, any> = {}
    moduleConfig.fields.forEach((field: any) => {
      if (field.default !== undefined) {
        defaultConfig[field.key] = field.default
      }
    })
    setConfiguration(defaultConfig)
    setIsActive(module.is_active)
  }, [module, moduleConfig])

  const handleSave = async () => {
    setIsSaving(true)
    try {
      // Update module configuration
      await apiClient.updateModule(module.id, {
        configuration,
        api_keys: apiKeys,
        is_active: isActive,
      })

      onSave()
      onOpenChange(false)
    } catch (error) {
      console.error("Error saving module configuration:", error)
    } finally {
      setIsSaving(false)
    }
  }

  const updateConfiguration = (key: string, value: any) => {
    setConfiguration((prev) => ({ ...prev, [key]: value }))
  }

  const updateApiKey = (key: string, value: string) => {
    setApiKeys((prev) => ({ ...prev, [key]: value }))
  }

  const hasRequiredApiKeys = () => {
    return moduleConfig.apiKeys.every((apiKey: any) => !apiKey.required || apiKeys[apiKey.key])
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            Configure {module.name.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
          </DialogTitle>
          <DialogDescription>{module.description}</DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Module Status */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div>
              <h4 className="font-medium">Module Status</h4>
              <p className="text-sm text-muted-foreground">Enable or disable this module</p>
            </div>
            <Switch checked={isActive} onCheckedChange={setIsActive} disabled={!hasRequiredApiKeys()} />
          </div>

          {/* API Keys Section */}
          {moduleConfig.apiKeys.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Key className="h-4 w-4" />
                <h4 className="font-medium">API Keys</h4>
              </div>

              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  API keys are encrypted and stored securely. They are required for this module to function properly.
                </AlertDescription>
              </Alert>

              <div className="space-y-3">
                {moduleConfig.apiKeys.map((apiKey: any) => (
                  <div key={apiKey.key} className="space-y-2">
                    <Label htmlFor={apiKey.key}>
                      {apiKey.label}
                      {apiKey.required && <span className="text-destructive ml-1">*</span>}
                    </Label>
                    <Input
                      id={apiKey.key}
                      type="password"
                      value={apiKeys[apiKey.key] || ""}
                      onChange={(e) => updateApiKey(apiKey.key, e.target.value)}
                      placeholder="Enter your API key"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Configuration Fields */}
          {moduleConfig.fields.length > 0 && (
            <>
              <Separator />
              <div className="space-y-4">
                <h4 className="font-medium">Configuration</h4>

                <div className="space-y-4">
                  {moduleConfig.fields.map((field: any) => (
                    <div key={field.key} className="space-y-2">
                      <Label htmlFor={field.key}>
                        {field.label}
                        {field.required && <span className="text-destructive ml-1">*</span>}
                      </Label>

                      {field.type === "text" && (
                        <Input
                          id={field.key}
                          value={configuration[field.key] || ""}
                          onChange={(e) => updateConfiguration(field.key, e.target.value)}
                          placeholder={field.placeholder}
                        />
                      )}

                      {field.type === "email" && (
                        <Input
                          id={field.key}
                          type="email"
                          value={configuration[field.key] || ""}
                          onChange={(e) => updateConfiguration(field.key, e.target.value)}
                          placeholder={field.placeholder}
                        />
                      )}

                      {field.type === "number" && (
                        <Input
                          id={field.key}
                          type="number"
                          value={configuration[field.key] || ""}
                          onChange={(e) => updateConfiguration(field.key, Number.parseInt(e.target.value))}
                          placeholder={field.placeholder}
                        />
                      )}

                      {field.type === "textarea" && (
                        <Textarea
                          id={field.key}
                          value={configuration[field.key] || ""}
                          onChange={(e) => updateConfiguration(field.key, e.target.value)}
                          placeholder={field.placeholder}
                          rows={3}
                        />
                      )}

                      {field.type === "boolean" && (
                        <div className="flex items-center space-x-2">
                          <Switch
                            id={field.key}
                            checked={configuration[field.key] || false}
                            onCheckedChange={(checked) => updateConfiguration(field.key, checked)}
                          />
                          <Label htmlFor={field.key}>Enable {field.label}</Label>
                        </div>
                      )}

                      {field.type === "select" && (
                        <select
                          id={field.key}
                          value={configuration[field.key] || field.default}
                          onChange={(e) => updateConfiguration(field.key, e.target.value)}
                          className="w-full p-2 border rounded-md"
                        >
                          {field.options.map((option: string) => (
                            <option key={option} value={option}>
                              {option.charAt(0).toUpperCase() + option.slice(1)}
                            </option>
                          ))}
                        </select>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Warning if module can't be activated */}
          {!hasRequiredApiKeys() && (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                This module requires API keys to be configured before it can be activated. Please provide all required
                API keys above.
              </AlertDescription>
            </Alert>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isSaving} className="gap-2">
            <Save className="h-4 w-4" />
            {isSaving ? "Saving..." : "Save Configuration"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
