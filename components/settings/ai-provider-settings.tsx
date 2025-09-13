"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Plus, Bot, Key, Trash2, Edit } from "lucide-react"
import { apiClient } from "@/lib/api-client"

interface AIProvider {
  id: number
  name: string
  display_name: string
  is_active: boolean
  is_default: boolean
  has_api_key: boolean
}

const providerTemplates = [
  {
    name: "openrouter",
    display_name: "OpenRouter",
    description: "Access multiple AI models through OpenRouter",
    base_url: "https://openrouter.ai/api/v1",
    models: ["meta-llama/llama-3.1-8b-instruct:free", "anthropic/claude-3-haiku", "openai/gpt-3.5-turbo"],
  },
  {
    name: "openai",
    display_name: "OpenAI",
    description: "Direct OpenAI API integration",
    base_url: "https://api.openai.com/v1",
    models: ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
  },
  {
    name: "anthropic",
    display_name: "Anthropic",
    description: "Claude AI models from Anthropic",
    base_url: "https://api.anthropic.com/v1",
    models: ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
  },
]

export function AIProviderSettings() {
  const [providers, setProviders] = useState<AIProvider[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)
  const [newProvider, setNewProvider] = useState({
    name: "",
    display_name: "",
    api_key: "",
    base_url: "",
    is_active: false,
  })

  useEffect(() => {
    loadProviders()
  }, [])

  const loadProviders = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getAIProviders()
      if (response.data) {
        setProviders(response.data)
      }
    } catch (error) {
      console.error("Error loading AI providers:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddProvider = async () => {
    if (!newProvider.name || !newProvider.api_key) return

    try {
      const response = await apiClient.createAIProvider(newProvider)
      if (response.data) {
        await loadProviders()
        setShowAddForm(false)
        setNewProvider({
          name: "",
          display_name: "",
          api_key: "",
          base_url: "",
          is_active: false,
        })
      }
    } catch (error) {
      console.error("Error adding AI provider:", error)
    }
  }

  const handleTemplateSelect = (template: (typeof providerTemplates)[0]) => {
    setNewProvider({
      name: template.name,
      display_name: template.display_name,
      api_key: "",
      base_url: template.base_url,
      is_active: false,
    })
  }

  const testConnection = async (provider: AIProvider) => {
    // Mock test - in real app would make actual API call
    console.log("Testing connection for provider:", provider.name)
  }

  return (
    <div className="space-y-6">
      {/* Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            AI Provider Configuration
          </CardTitle>
          <CardDescription>
            Configure AI providers for content generation, SEO optimization, and other AI-powered features. You can use
            multiple providers and switch between them as needed.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Alert>
            <Key className="h-4 w-4" />
            <AlertDescription>
              API keys are encrypted and stored securely. You can change providers at any time without losing your
              content.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Current Providers */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0">
          <div>
            <CardTitle>Configured Providers</CardTitle>
            <CardDescription>Manage your AI service providers</CardDescription>
          </div>
          <Button onClick={() => setShowAddForm(true)} className="gap-2">
            <Plus className="h-4 w-4" />
            Add Provider
          </Button>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="text-center py-8">Loading providers...</div>
          ) : providers.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No AI providers configured. Add one to get started with AI features.
            </div>
          ) : (
            <div className="space-y-4">
              {providers.map((provider) => (
                <div key={provider.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      <Bot className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-medium">{provider.display_name}</h3>
                        {provider.is_active && <Badge className="bg-chart-1 text-white">Active</Badge>}
                        {provider.is_default && <Badge variant="outline">Default</Badge>}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {provider.has_api_key ? "API key configured" : "No API key"}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" onClick={() => testConnection(provider)}>
                      Test
                    </Button>
                    <Button variant="outline" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm" className="text-destructive bg-transparent">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Add Provider Form */}
      {showAddForm && (
        <Card>
          <CardHeader>
            <CardTitle>Add AI Provider</CardTitle>
            <CardDescription>Configure a new AI service provider for your CMS</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Provider Templates */}
            <div className="space-y-3">
              <Label>Quick Setup</Label>
              <div className="grid gap-3 sm:grid-cols-3">
                {providerTemplates.map((template) => (
                  <Button
                    key={template.name}
                    variant="outline"
                    className="h-auto p-4 justify-start bg-transparent"
                    onClick={() => handleTemplateSelect(template)}
                  >
                    <div className="text-left">
                      <div className="font-medium">{template.display_name}</div>
                      <div className="text-sm text-muted-foreground">{template.description}</div>
                    </div>
                  </Button>
                ))}
              </div>
            </div>

            <Separator />

            {/* Manual Configuration */}
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="provider_name">Provider Name</Label>
                <Select
                  value={newProvider.name}
                  onValueChange={(value) => setNewProvider((prev) => ({ ...prev, name: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select provider" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="openrouter">OpenRouter</SelectItem>
                    <SelectItem value="openai">OpenAI</SelectItem>
                    <SelectItem value="anthropic">Anthropic</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="display_name">Display Name</Label>
                <Input
                  id="display_name"
                  value={newProvider.display_name}
                  onChange={(e) =>
                    setNewProvider((prev) => ({
                      ...prev,
                      display_name: e.target.value,
                    }))
                  }
                  placeholder="My AI Provider"
                />
              </div>

              <div className="space-y-2 sm:col-span-2">
                <Label htmlFor="api_key">API Key</Label>
                <Input
                  id="api_key"
                  type="password"
                  value={newProvider.api_key}
                  onChange={(e) => setNewProvider((prev) => ({ ...prev, api_key: e.target.value }))}
                  placeholder="Enter your API key"
                />
              </div>

              <div className="space-y-2 sm:col-span-2">
                <Label htmlFor="base_url">Base URL (Optional)</Label>
                <Input
                  id="base_url"
                  value={newProvider.base_url}
                  onChange={(e) => setNewProvider((prev) => ({ ...prev, base_url: e.target.value }))}
                  placeholder="https://api.example.com/v1"
                />
              </div>

              <div className="flex items-center space-x-2 sm:col-span-2">
                <Switch
                  id="is_active"
                  checked={newProvider.is_active}
                  onCheckedChange={(checked) => setNewProvider((prev) => ({ ...prev, is_active: checked }))}
                />
                <Label htmlFor="is_active">Set as active provider</Label>
              </div>
            </div>

            <div className="flex gap-2">
              <Button onClick={handleAddProvider} disabled={!newProvider.name || !newProvider.api_key}>
                Add Provider
              </Button>
              <Button variant="outline" onClick={() => setShowAddForm(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
