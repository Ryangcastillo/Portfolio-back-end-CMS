"use client"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AIProviderSettings } from "./ai-provider-settings"
import { SiteSettings } from "./site-settings"
import { UserSettings } from "./user-settings"
import { Bot, Globe, User } from "lucide-react"

export function SettingsManager() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance">Settings</h1>
          <p className="text-muted-foreground">Configure your CMS, AI providers, and user preferences</p>
        </div>
      </div>

      {/* Settings Tabs */}
      <Tabs defaultValue="ai" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="ai" className="gap-2">
            <Bot className="h-4 w-4" />
            AI Providers
          </TabsTrigger>
          <TabsTrigger value="site" className="gap-2">
            <Globe className="h-4 w-4" />
            Site Settings
          </TabsTrigger>
          <TabsTrigger value="user" className="gap-2">
            <User className="h-4 w-4" />
            User Settings
          </TabsTrigger>
        </TabsList>

        <TabsContent value="ai" className="space-y-6">
          <AIProviderSettings />
        </TabsContent>

        <TabsContent value="site" className="space-y-6">
          <SiteSettings />
        </TabsContent>

        <TabsContent value="user" className="space-y-6">
          <UserSettings />
        </TabsContent>
      </Tabs>
    </div>
  )
}
