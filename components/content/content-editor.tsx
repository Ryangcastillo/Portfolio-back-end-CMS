"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Save, Eye, Wand2, ArrowLeft, Sparkles, Search, Tag } from "lucide-react"
import { AIAssistant } from "./ai-assistant"

interface ContentEditorProps {
  contentId?: string
}

interface ContentData {
  title: string
  content_type: string
  body: string
  excerpt: string
  status: string
  meta_title: string
  meta_description: string
  meta_keywords: string
}

export function ContentEditor({ contentId }: ContentEditorProps) {
  const [content, setContent] = useState<ContentData>({
    title: "",
    content_type: "article",
    body: "",
    excerpt: "",
    status: "draft",
    meta_title: "",
    meta_description: "",
    meta_keywords: "",
  })
  const [isLoading, setIsLoading] = useState(false)
  const [showAIAssistant, setShowAIAssistant] = useState(false)

  const isEditing = !!contentId

  useEffect(() => {
    if (contentId) {
      // In real app, fetch content data from API
      // For now, using mock data
      setContent({
        title: "Getting Started with Next.js",
        content_type: "article",
        body: "# Getting Started with Next.js\n\nNext.js is a powerful React framework that makes building web applications easier...",
        excerpt: "Learn the basics of Next.js and how to get started with your first project.",
        status: "draft",
        meta_title: "Getting Started with Next.js - Complete Guide",
        meta_description:
          "Learn Next.js from scratch with this comprehensive guide covering setup, routing, and deployment.",
        meta_keywords: "nextjs, react, web development, tutorial",
      })
    }
  }, [contentId])

  const handleSave = async (newStatus?: string) => {
    setIsLoading(true)
    try {
      const dataToSave = {
        ...content,
        status: newStatus || content.status,
      }

      // In real app, make API call to save content
      console.log("Saving content:", dataToSave)

      // Mock API delay
      await new Promise((resolve) => setTimeout(resolve, 1000))

      if (newStatus) {
        setContent((prev) => ({ ...prev, status: newStatus }))
      }
    } catch (error) {
      console.error("Error saving content:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleAIGenerate = (field: string, generatedContent: string) => {
    setContent((prev) => ({
      ...prev,
      [field]: generatedContent,
    }))
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" asChild>
            <a href="/content">
              <ArrowLeft className="h-4 w-4" />
            </a>
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-balance">{isEditing ? "Edit Content" : "Create Content"}</h1>
            <p className="text-muted-foreground">
              {isEditing ? "Update your existing content" : "Create new content with AI assistance"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={content.status === "published" ? "default" : "secondary"}>{content.status}</Badge>
          <Button variant="outline" className="gap-2 bg-transparent">
            <Eye className="h-4 w-4" />
            Preview
          </Button>
          <Button
            variant="outline"
            className="gap-2 bg-transparent"
            onClick={() => setShowAIAssistant(!showAIAssistant)}
          >
            <Wand2 className="h-4 w-4" />
            AI Assistant
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Main Content */}
        <div className="lg:col-span-3 space-y-6">
          <Tabs defaultValue="content" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="content">Content</TabsTrigger>
              <TabsTrigger value="seo">SEO</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>

            <TabsContent value="content" className="space-y-6">
              {/* Basic Content */}
              <Card>
                <CardHeader>
                  <CardTitle>Content Details</CardTitle>
                  <CardDescription>Enter the main content information</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="title">Title</Label>
                    <div className="flex gap-2">
                      <Input
                        id="title"
                        value={content.title}
                        onChange={(e) => setContent((prev) => ({ ...prev, title: e.target.value }))}
                        placeholder="Enter content title..."
                        className="flex-1"
                      />
                      <Button variant="outline" size="icon" onClick={() => setShowAIAssistant(true)}>
                        <Sparkles className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="excerpt">Excerpt</Label>
                    <div className="flex gap-2">
                      <Textarea
                        id="excerpt"
                        value={content.excerpt}
                        onChange={(e) => setContent((prev) => ({ ...prev, excerpt: e.target.value }))}
                        placeholder="Brief description of the content..."
                        rows={3}
                        className="flex-1"
                      />
                      <Button variant="outline" size="icon" onClick={() => setShowAIAssistant(true)}>
                        <Sparkles className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="body">Content Body</Label>
                    <div className="flex gap-2">
                      <Textarea
                        id="body"
                        value={content.body}
                        onChange={(e) => setContent((prev) => ({ ...prev, body: e.target.value }))}
                        placeholder="Write your content here... (Markdown supported)"
                        rows={15}
                        className="flex-1 font-mono"
                      />
                      <Button variant="outline" size="icon" onClick={() => setShowAIAssistant(true)}>
                        <Sparkles className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="seo" className="space-y-6">
              {/* SEO Settings */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Search className="h-5 w-5" />
                    SEO Optimization
                  </CardTitle>
                  <CardDescription>Optimize your content for search engines</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="meta_title">Meta Title</Label>
                    <div className="flex gap-2">
                      <Input
                        id="meta_title"
                        value={content.meta_title}
                        onChange={(e) => setContent((prev) => ({ ...prev, meta_title: e.target.value }))}
                        placeholder="SEO-optimized title..."
                        className="flex-1"
                      />
                      <Button variant="outline" size="icon" onClick={() => setShowAIAssistant(true)}>
                        <Sparkles className="h-4 w-4" />
                      </Button>
                    </div>
                    <p className="text-xs text-muted-foreground">{content.meta_title.length}/60 characters</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="meta_description">Meta Description</Label>
                    <div className="flex gap-2">
                      <Textarea
                        id="meta_description"
                        value={content.meta_description}
                        onChange={(e) => setContent((prev) => ({ ...prev, meta_description: e.target.value }))}
                        placeholder="Brief description for search results..."
                        rows={3}
                        className="flex-1"
                      />
                      <Button variant="outline" size="icon" onClick={() => setShowAIAssistant(true)}>
                        <Sparkles className="h-4 w-4" />
                      </Button>
                    </div>
                    <p className="text-xs text-muted-foreground">{content.meta_description.length}/160 characters</p>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="meta_keywords">Keywords</Label>
                    <div className="flex gap-2">
                      <Input
                        id="meta_keywords"
                        value={content.meta_keywords}
                        onChange={(e) => setContent((prev) => ({ ...prev, meta_keywords: e.target.value }))}
                        placeholder="keyword1, keyword2, keyword3..."
                        className="flex-1"
                      />
                      <Button variant="outline" size="icon" onClick={() => setShowAIAssistant(true)}>
                        <Tag className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="settings" className="space-y-6">
              {/* Content Settings */}
              <Card>
                <CardHeader>
                  <CardTitle>Content Settings</CardTitle>
                  <CardDescription>Configure content type and publication settings</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="content_type">Content Type</Label>
                    <Select
                      value={content.content_type}
                      onValueChange={(value) => setContent((prev) => ({ ...prev, content_type: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="article">Article</SelectItem>
                        <SelectItem value="page">Page</SelectItem>
                        <SelectItem value="blog_post">Blog Post</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="status">Status</Label>
                    <Select
                      value={content.status}
                      onValueChange={(value) => setContent((prev) => ({ ...prev, status: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="draft">Draft</SelectItem>
                        <SelectItem value="published">Published</SelectItem>
                        <SelectItem value="archived">Archived</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full gap-2" onClick={() => handleSave()} disabled={isLoading}>
                <Save className="h-4 w-4" />
                {isLoading ? "Saving..." : "Save Draft"}
              </Button>

              <Button
                variant="secondary"
                className="w-full gap-2"
                onClick={() => handleSave("published")}
                disabled={isLoading}
              >
                <Eye className="h-4 w-4" />
                Publish
              </Button>

              <Separator />

              <Button
                variant="outline"
                className="w-full gap-2 bg-transparent"
                onClick={() => setShowAIAssistant(true)}
              >
                <Wand2 className="h-4 w-4" />
                AI Assistant
              </Button>
            </CardContent>
          </Card>

          {/* AI Assistant Panel */}
          {showAIAssistant && (
            <AIAssistant content={content} onGenerate={handleAIGenerate} onClose={() => setShowAIAssistant(false)} />
          )}
        </div>
      </div>
    </div>
  )
}
