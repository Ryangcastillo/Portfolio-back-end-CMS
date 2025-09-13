"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Wand2, Sparkles, Copy, RefreshCw, X, Lightbulb, Search, Tag } from "lucide-react"

interface AIAssistantProps {
  content: {
    title: string
    body: string
    excerpt: string
    meta_title: string
    meta_description: string
    meta_keywords: string
  }
  onGenerate: (field: string, content: string) => void
  onClose: () => void
}

const aiSuggestions = [
  {
    type: "title",
    icon: Lightbulb,
    label: "Generate Title",
    description: "Create engaging titles",
    suggestions: [
      "The Complete Guide to Next.js: Everything You Need to Know",
      "Next.js Mastery: From Beginner to Expert in 2024",
      "Building Modern Web Apps with Next.js: A Developer's Journey",
    ],
  },
  {
    type: "excerpt",
    icon: Sparkles,
    label: "Generate Excerpt",
    description: "Create compelling summaries",
    suggestions: [
      "Discover the power of Next.js and learn how to build lightning-fast web applications with this comprehensive guide.",
      "Master Next.js development with practical examples, best practices, and real-world projects.",
      "From setup to deployment, this guide covers everything you need to become a Next.js expert.",
    ],
  },
  {
    type: "meta_title",
    icon: Search,
    label: "SEO Title",
    description: "Optimize for search engines",
    suggestions: [
      "Next.js Tutorial 2024 | Complete Guide for Beginners",
      "Learn Next.js: Step-by-Step Guide | Web Development",
      "Next.js Framework Guide | React Development Tutorial",
    ],
  },
  {
    type: "meta_description",
    icon: Search,
    label: "Meta Description",
    description: "Improve search visibility",
    suggestions: [
      "Learn Next.js from scratch with our comprehensive tutorial. Covers routing, API routes, deployment, and more. Perfect for beginners and experienced developers.",
      "Master Next.js development with this complete guide. Build modern web applications with React, TypeScript, and the latest Next.js features.",
      "Complete Next.js tutorial covering everything from basics to advanced concepts. Build, optimize, and deploy modern web applications.",
    ],
  },
  {
    type: "meta_keywords",
    icon: Tag,
    label: "Keywords",
    description: "Target relevant keywords",
    suggestions: [
      "nextjs, react, web development, javascript, tutorial, framework",
      "next.js guide, react framework, web app development, javascript tutorial",
      "nextjs tutorial, react development, modern web apps, javascript framework",
    ],
  },
]

export function AIAssistant({ content, onGenerate, onClose }: AIAssistantProps) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [customPrompt, setCustomPrompt] = useState("")

  const handleGenerate = async (type: string, suggestion: string) => {
    setIsGenerating(true)
    try {
      // Simulate AI generation delay
      await new Promise((resolve) => setTimeout(resolve, 1500))
      onGenerate(type, suggestion)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCustomGenerate = async () => {
    if (!customPrompt.trim()) return

    setIsGenerating(true)
    try {
      // Simulate AI generation delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Mock AI response based on prompt
      const mockResponse = `Generated content based on: "${customPrompt}"\n\nThis is a sample AI-generated response that would be created based on your custom prompt. In a real implementation, this would connect to your AI provider.`

      onGenerate("body", content.body + "\n\n" + mockResponse)
      setCustomPrompt("")
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div>
          <CardTitle className="flex items-center gap-2">
            <Wand2 className="h-5 w-5" />
            AI Assistant
          </CardTitle>
          <CardDescription>Get AI-powered suggestions for your content</CardDescription>
        </div>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Custom Prompt */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Custom Request</label>
          <Textarea
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="Ask AI to help with your content... (e.g., 'Write an introduction about Next.js benefits')"
            rows={3}
          />
          <Button
            onClick={handleCustomGenerate}
            disabled={isGenerating || !customPrompt.trim()}
            className="w-full gap-2"
          >
            {isGenerating ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            {isGenerating ? "Generating..." : "Generate"}
          </Button>
        </div>

        <Separator />

        {/* Quick Suggestions */}
        <div className="space-y-4">
          <h4 className="text-sm font-medium">Quick Suggestions</h4>

          {aiSuggestions.map((section) => {
            const Icon = section.icon
            return (
              <div key={section.type} className="space-y-2">
                <div className="flex items-center gap-2">
                  <Icon className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">{section.label}</span>
                  <Badge variant="outline" className="text-xs">
                    {section.description}
                  </Badge>
                </div>

                <div className="space-y-2">
                  {section.suggestions.map((suggestion, index) => (
                    <div
                      key={index}
                      className="p-3 rounded-md border bg-muted/50 hover:bg-muted cursor-pointer group"
                      onClick={() => handleGenerate(section.type, suggestion)}
                    >
                      <p className="text-sm">{suggestion}</p>
                      <div className="flex items-center justify-between mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <span className="text-xs text-muted-foreground">Click to use</span>
                        <Copy className="h-3 w-3 text-muted-foreground" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
