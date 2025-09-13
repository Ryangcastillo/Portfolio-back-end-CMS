"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Save, User, Shield, Bell } from "lucide-react"
import { apiClient } from "@/lib/api-client"

interface UserProfile {
  id: number
  email: string
  username: string
  full_name: string
  role: string
  is_active: boolean
  preferences: {
    theme: string
    notifications: {
      email: boolean
      push: boolean
      content_updates: boolean
      system_alerts: boolean
    }
    editor: {
      auto_save: boolean
      spell_check: boolean
      word_wrap: boolean
    }
  }
}

export function UserSettings() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [passwordData, setPasswordData] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  })

  useEffect(() => {
    loadUserProfile()
  }, [])

  const loadUserProfile = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getCurrentUser()
      if (response.data) {
        setProfile({
          ...response.data,
          preferences: {
            theme: "system",
            notifications: {
              email: true,
              push: true,
              content_updates: true,
              system_alerts: true,
            },
            editor: {
              auto_save: true,
              spell_check: true,
              word_wrap: true,
            },
            ...response.data.preferences,
          },
        })
      }
    } catch (error) {
      console.error("Error loading user profile:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveProfile = async () => {
    if (!profile) return

    setIsSaving(true)
    try {
      // In real app, make API call to update profile
      console.log("Saving profile:", profile)
      await new Promise((resolve) => setTimeout(resolve, 1000))
    } catch (error) {
      console.error("Error saving profile:", error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleChangePassword = async () => {
    if (passwordData.new_password !== passwordData.confirm_password) {
      alert("New passwords don't match")
      return
    }

    try {
      // In real app, make API call to change password
      console.log("Changing password")
      setPasswordData({
        current_password: "",
        new_password: "",
        confirm_password: "",
      })
    } catch (error) {
      console.error("Error changing password:", error)
    }
  }

  const updateProfile = (path: string, value: any) => {
    if (!profile) return

    setProfile((prev) => {
      if (!prev) return prev
      const keys = path.split(".")
      const newProfile = { ...prev }
      let current: any = newProfile

      for (let i = 0; i < keys.length - 1; i++) {
        current[keys[i]] = { ...current[keys[i]] }
        current = current[keys[i]]
      }

      current[keys[keys.length - 1]] = value
      return newProfile
    })
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading user settings...</div>
  }

  if (!profile) {
    return <div className="text-center py-8">Error loading user profile</div>
  }

  return (
    <div className="space-y-6">
      {/* Profile Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Profile Information
          </CardTitle>
          <CardDescription>Update your personal information and account details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <Avatar className="h-20 w-20">
              <AvatarImage src="/placeholder.svg" />
              <AvatarFallback className="text-lg">
                {profile.full_name
                  .split(" ")
                  .map((n) => n[0])
                  .join("")
                  .toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div>
              <Button variant="outline">Change Avatar</Button>
              <p className="text-sm text-muted-foreground mt-1">JPG, PNG or GIF. Max size 2MB.</p>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                value={profile.full_name}
                onChange={(e) => updateProfile("full_name", e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={profile.username}
                onChange={(e) => updateProfile("username", e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={profile.email}
                onChange={(e) => updateProfile("email", e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="role">Role</Label>
              <Select value={profile.role} onValueChange={(value) => updateProfile("role", value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">Administrator</SelectItem>
                  <SelectItem value="editor">Editor</SelectItem>
                  <SelectItem value="viewer">Viewer</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Password Change */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Change Password
          </CardTitle>
          <CardDescription>Update your account password</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="current_password">Current Password</Label>
            <Input
              id="current_password"
              type="password"
              value={passwordData.current_password}
              onChange={(e) => setPasswordData((prev) => ({ ...prev, current_password: e.target.value }))}
            />
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="new_password">New Password</Label>
              <Input
                id="new_password"
                type="password"
                value={passwordData.new_password}
                onChange={(e) => setPasswordData((prev) => ({ ...prev, new_password: e.target.value }))}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirm_password">Confirm New Password</Label>
              <Input
                id="confirm_password"
                type="password"
                value={passwordData.confirm_password}
                onChange={(e) => setPasswordData((prev) => ({ ...prev, confirm_password: e.target.value }))}
              />
            </div>
          </div>

          <Button onClick={handleChangePassword} variant="outline">
            Change Password
          </Button>
        </CardContent>
      </Card>

      {/* Preferences */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Preferences
          </CardTitle>
          <CardDescription>Customize your CMS experience</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Theme Preference */}
          <div className="space-y-3">
            <Label>Theme Preference</Label>
            <Select
              value={profile.preferences.theme}
              onValueChange={(value) => updateProfile("preferences.theme", value)}
            >
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="light">Light</SelectItem>
                <SelectItem value="dark">Dark</SelectItem>
                <SelectItem value="system">System</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Notifications */}
          <div className="space-y-3">
            <Label>Notifications</Label>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="email_notifications">Email Notifications</Label>
                  <p className="text-sm text-muted-foreground">Receive notifications via email</p>
                </div>
                <Switch
                  id="email_notifications"
                  checked={profile.preferences.notifications.email}
                  onCheckedChange={(checked) => updateProfile("preferences.notifications.email", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="content_updates">Content Updates</Label>
                  <p className="text-sm text-muted-foreground">Get notified about content changes</p>
                </div>
                <Switch
                  id="content_updates"
                  checked={profile.preferences.notifications.content_updates}
                  onCheckedChange={(checked) => updateProfile("preferences.notifications.content_updates", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="system_alerts">System Alerts</Label>
                  <p className="text-sm text-muted-foreground">Important system notifications</p>
                </div>
                <Switch
                  id="system_alerts"
                  checked={profile.preferences.notifications.system_alerts}
                  onCheckedChange={(checked) => updateProfile("preferences.notifications.system_alerts", checked)}
                />
              </div>
            </div>
          </div>

          {/* Editor Preferences */}
          <div className="space-y-3">
            <Label>Editor Preferences</Label>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="auto_save">Auto Save</Label>
                  <p className="text-sm text-muted-foreground">Automatically save content while editing</p>
                </div>
                <Switch
                  id="auto_save"
                  checked={profile.preferences.editor.auto_save}
                  onCheckedChange={(checked) => updateProfile("preferences.editor.auto_save", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="spell_check">Spell Check</Label>
                  <p className="text-sm text-muted-foreground">Enable spell checking in editor</p>
                </div>
                <Switch
                  id="spell_check"
                  checked={profile.preferences.editor.spell_check}
                  onCheckedChange={(checked) => updateProfile("preferences.editor.spell_check", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="word_wrap">Word Wrap</Label>
                  <p className="text-sm text-muted-foreground">Wrap long lines in editor</p>
                </div>
                <Switch
                  id="word_wrap"
                  checked={profile.preferences.editor.word_wrap}
                  onCheckedChange={(checked) => updateProfile("preferences.editor.word_wrap", checked)}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex justify-end">
        <Button onClick={handleSaveProfile} disabled={isSaving} className="gap-2">
          <Save className="h-4 w-4" />
          {isSaving ? "Saving..." : "Save Changes"}
        </Button>
      </div>
    </div>
  )
}
