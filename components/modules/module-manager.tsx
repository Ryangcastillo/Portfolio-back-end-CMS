"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ModuleCatalog } from "./module-catalog"
import { InstalledModules } from "./installed-modules"
import { Puzzle, Download } from "lucide-react"

export function ModuleManager() {
  const [activeTab, setActiveTab] = useState("installed")

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance">Module Management</h1>
          <p className="text-muted-foreground">
            Extend your CMS with powerful modules for analytics, SEO, marketing, and more
          </p>
        </div>
      </div>

      {/* Module Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="installed" className="gap-2">
            <Puzzle className="h-4 w-4" />
            Installed Modules
          </TabsTrigger>
          <TabsTrigger value="catalog" className="gap-2">
            <Download className="h-4 w-4" />
            Module Catalog
          </TabsTrigger>
        </TabsList>

        <TabsContent value="installed" className="space-y-6">
          <InstalledModules />
        </TabsContent>

        <TabsContent value="catalog" className="space-y-6">
          <ModuleCatalog />
        </TabsContent>
      </Tabs>
    </div>
  )
}
