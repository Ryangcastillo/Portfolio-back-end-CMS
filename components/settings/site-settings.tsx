"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Save, Globe, Palette, Mail, Building2 } from "lucide-react"
import { apiClient } from "@/lib/api-client"

interface SiteConfig {
  site_title: string
  site_description: string
  site_logo?: string
  site_favicon?: string
  company_name: string
  company_logo?: string
  company_address?: string
  company_phone?: string
  company_business_hours?: string
  footer_text: string
  contact_email: string
  social_links: Record<string, string>
  theme_settings: {
    primary_color: string
    secondary_color: string
    font_family: string
    dark_mode_enabled: boolean
  }
}

export function SiteSettings() {
  const [config, setConfig] = useState<SiteConfig>({
    site_title: "My CMS Site",
    site_description: "A powerful CMS built with Stitch",
    company_name: "My Company",
    company_address: "123 Business St, City, State 12345",
    company_phone: "(555) 123-4567",
    company_business_hours: "Mon-Fri 9AM-5PM",
    footer_text: "© 2024 My CMS Site. All rights reserved.",
    contact_email: "admin@example.com",
    social_links: {},
    theme_settings: {
      primary_color: "#3b82f6",
      secondary_color: "#64748b",
      font_family: "Inter",
      dark_mode_enabled: true,
    },
  })
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [logoUploading, setLogoUploading] = useState(false)

  useEffect(() => {
    loadSiteConfig()
  }, [])

  const loadSiteConfig = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getSiteConfig()
      if (response.data) {
        setConfig(response.data)
      }
    } catch (error) {
      console.error("Error loading site config:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      const response = await apiClient.updateSiteConfig(config)
      if (response.data) {
        // Show success message
        console.log("Site configuration saved successfully")
      }
    } catch (error) {
      console.error("Error saving site config:", error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleLogoUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
    type: "company_logo" | "site_logo" | "site_favicon",
  ) => {
    const file = event.target.files?.[0]
    if (!file) return

    setLogoUploading(true)
    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append("file", file)
      formData.append("type", type)

      // In a real implementation, you'd upload to your file storage service
      // For now, we'll create a placeholder URL
      const logoUrl = URL.createObjectURL(file)

      updateConfig(type, logoUrl)
      console.log(`${type} uploaded successfully`)
    } catch (error) {
      console.error(`Error uploading ${type}:`, error)
    } finally {
      setLogoUploading(false)
    }
  }

  const updateConfig = (path: string, value: any) => {
    setConfig((prev) => {
      const keys = path.split(".")
      const newConfig = { ...prev }
      let current: any = newConfig

      for (let i = 0; i < keys.length - 1; i++) {
        current[keys[i]] = { ...current[keys[i]] }
        current = current[keys[i]]
      }

      current[keys[keys.length - 1]] = value
      return newConfig
    })
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading site settings...</div>
  }

  return (
    <div className="space-y-6">
      {/* Company Branding */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Building2 className="h-5 w-5" />
            Company Branding
          </CardTitle>
          <CardDescription>Manage your company logo, name, and contact information</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="company_name">Company Name</Label>
              <Input
                id="company_name"
                value={config.company_name}
                onChange={(e) => updateConfig("company_name", e.target.value)}
                placeholder="Your Company Name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="company_phone">Company Phone</Label>
              <Input
                id="company_phone"
                value={config.company_phone || ""}
                onChange={(e) => updateConfig("company_phone", e.target.value)}
                placeholder="(555) 123-4567"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="company_address">Company Address</Label>
            <Textarea
              id="company_address"
              value={config.company_address || ""}
              onChange={(e) => updateConfig("company_address", e.target.value)}
              placeholder="123 Business Street, City, State 12345"
              rows={2}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="company_business_hours">Business Hours</Label>
            <Input
              id="company_business_hours"
              value={config.company_business_hours || ""}
              onChange={(e) => updateConfig("company_business_hours", e.target.value)}
              placeholder="Mon-Fri 9AM-5PM"
            />
          </div>

          {/* Logo Upload Section */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Company Logo</Label>
              <div className="flex items-center gap-4">
                {config.company_logo && (
                  <div className="w-16 h-16 border rounded-lg overflow-hidden bg-muted flex items-center justify-center">
                    <img
                      src={config.company_logo || "/placeholder.svg"}
                      alt="Company Logo"
                      className="w-full h-full object-contain"
                    />
                  </div>
                )}
                <div className="flex-1">
                  <Input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleLogoUpload(e, "company_logo")}
                    disabled={logoUploading}
                    className="cursor-pointer"
                  />
                  <p className="text-sm text-muted-foreground mt-1">
                    Upload PNG, JPG, or SVG. Recommended size: 200x200px
                  </p>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Site Logo</Label>
              <div className="flex items-center gap-4">
                {config.site_logo && (
                  <div className="w-16 h-16 border rounded-lg overflow-hidden bg-muted flex items-center justify-center">
                    <img
                      src={config.site_logo || "/placeholder.svg"}
                      alt="Site Logo"
                      className="w-full h-full object-contain"
                    />
                  </div>
                )}
                <div className="flex-1">
                  <Input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleLogoUpload(e, "site_logo")}
                    disabled={logoUploading}
                    className="cursor-pointer"
                  />
                  <p className="text-sm text-muted-foreground mt-1">Logo for website header and navigation</p>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Favicon</Label>
              <div className="flex items-center gap-4">
                {config.site_favicon && (
                  <div className="w-8 h-8 border rounded overflow-hidden bg-muted flex items-center justify-center">
                    <img
                      src={config.site_favicon || "/placeholder.svg"}
                      alt="Favicon"
                      className="w-full h-full object-contain"
                    />
                  </div>
                )}
                <div className="flex-1">
                  <Input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleLogoUpload(e, "site_favicon")}
                    disabled={logoUploading}
                    className="cursor-pointer"
                  />
                  <p className="text-sm text-muted-foreground mt-1">
                    Small icon for browser tabs. Recommended: 32x32px ICO or PNG
                  </p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* General Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            General Settings
          </CardTitle>
          <CardDescription>Basic information about your website</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="site_title">Site Title</Label>
              <Input
                id="site_title"
                value={config.site_title}
                onChange={(e) => updateConfig("site_title", e.target.value)}
                placeholder="My Awesome Website"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="contact_email">Contact Email</Label>
              <Input
                id="contact_email"
                type="email"
                value={config.contact_email}
                onChange={(e) => updateConfig("contact_email", e.target.value)}
                placeholder="admin@example.com"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="site_description">Site Description</Label>
            <Textarea
              id="site_description"
              value={config.site_description}
              onChange={(e) => updateConfig("site_description", e.target.value)}
              placeholder="A brief description of your website"
              rows={3}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="footer_text">Footer Text</Label>
            <Input
              id="footer_text"
              value={config.footer_text}
              onChange={(e) => updateConfig("footer_text", e.target.value)}
              placeholder="© 2024 My Website. All rights reserved."
            />
          </div>
        </CardContent>
      </Card>

      {/* Theme Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Palette className="h-5 w-5" />
            Theme Settings
          </CardTitle>
          <CardDescription>Customize the appearance of your website</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="primary_color">Primary Color</Label>
              <div className="flex gap-2">
                <Input
                  id="primary_color"
                  type="color"
                  value={config.theme_settings.primary_color}
                  onChange={(e) => updateConfig("theme_settings.primary_color", e.target.value)}
                  className="w-16 h-10 p-1"
                />
                <Input
                  value={config.theme_settings.primary_color}
                  onChange={(e) => updateConfig("theme_settings.primary_color", e.target.value)}
                  placeholder="#3b82f6"
                  className="flex-1"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="secondary_color">Secondary Color</Label>
              <div className="flex gap-2">
                <Input
                  id="secondary_color"
                  type="color"
                  value={config.theme_settings.secondary_color}
                  onChange={(e) => updateConfig("theme_settings.secondary_color", e.target.value)}
                  className="w-16 h-10 p-1"
                />
                <Input
                  value={config.theme_settings.secondary_color}
                  onChange={(e) => updateConfig("theme_settings.secondary_color", e.target.value)}
                  placeholder="#64748b"
                  className="flex-1"
                />
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="font_family">Font Family</Label>
            <Select
              value={config.theme_settings.font_family}
              onValueChange={(value) => updateConfig("theme_settings.font_family", value)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Inter">Inter</SelectItem>
                <SelectItem value="Roboto">Roboto</SelectItem>
                <SelectItem value="Open Sans">Open Sans</SelectItem>
                <SelectItem value="Lato">Lato</SelectItem>
                <SelectItem value="Poppins">Poppins</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center space-x-2">
            <Switch
              id="dark_mode"
              checked={config.theme_settings.dark_mode_enabled}
              onCheckedChange={(checked) => updateConfig("theme_settings.dark_mode_enabled", checked)}
            />
            <Label htmlFor="dark_mode">Enable dark mode support</Label>
          </div>
        </CardContent>
      </Card>

      {/* Social Links */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Mail className="h-5 w-5" />
            Social Links
          </CardTitle>
          <CardDescription>Add links to your social media profiles</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="twitter">Twitter</Label>
              <Input
                id="twitter"
                value={config.social_links.twitter || ""}
                onChange={(e) =>
                  updateConfig("social_links", {
                    ...config.social_links,
                    twitter: e.target.value,
                  })
                }
                placeholder="https://twitter.com/username"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="facebook">Facebook</Label>
              <Input
                id="facebook"
                value={config.social_links.facebook || ""}
                onChange={(e) =>
                  updateConfig("social_links", {
                    ...config.social_links,
                    facebook: e.target.value,
                  })
                }
                placeholder="https://facebook.com/page"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="linkedin">LinkedIn</Label>
              <Input
                id="linkedin"
                value={config.social_links.linkedin || ""}
                onChange={(e) =>
                  updateConfig("social_links", {
                    ...config.social_links,
                    linkedin: e.target.value,
                  })
                }
                placeholder="https://linkedin.com/company/name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="instagram">Instagram</Label>
              <Input
                id="instagram"
                value={config.social_links.instagram || ""}
                onChange={(e) =>
                  updateConfig("social_links", {
                    ...config.social_links,
                    instagram: e.target.value,
                  })
                }
                placeholder="https://instagram.com/username"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button onClick={handleSave} disabled={isSaving} className="gap-2">
          <Save className="h-4 w-4" />
          {isSaving ? "Saving..." : "Save Settings"}
        </Button>
      </div>
    </div>
  )
}
