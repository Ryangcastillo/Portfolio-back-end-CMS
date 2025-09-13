"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Separator } from "@/components/ui/separator"
import { Mail, Send, Clock, CheckCircle, XCircle, AlertCircle, Users, BarChart3, Settings, Plus } from "lucide-react"
import { apiClient } from "@/lib/api-client"

interface NotificationStats {
  total_sent: number
  total_delivered: number
  total_opened: number
  total_clicked: number
  bounce_rate: number
  open_rate: number
  click_rate: number
}

interface Communication {
  id: number
  type: string
  subject: string
  recipient_email: string
  recipient_name: string
  sent_at: string
  delivery_status: string
  opened_at?: string
  clicked_at?: string
}

interface NotificationPanelProps {
  eventId: number
}

export function NotificationPanel({ eventId }: NotificationPanelProps) {
  const [stats, setStats] = useState<NotificationStats | null>(null)
  const [communications, setCommunications] = useState<Communication[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSending, setIsSending] = useState(false)
  const [emailList, setEmailList] = useState("")
  const [testEmail, setTestEmail] = useState("")

  useEffect(() => {
    loadNotificationData()
  }, [eventId])

  const loadNotificationData = async () => {
    setIsLoading(true)
    try {
      const [statsResponse, communicationsResponse] = await Promise.all([
        apiClient.request(`/notifications/${eventId}/notification-stats`, { method: "GET" }),
        apiClient.request(`/notifications/${eventId}/communications`, { method: "GET" }),
      ])

      if (statsResponse.data) setStats(statsResponse.data)
      if (communicationsResponse.data) setCommunications(communicationsResponse.data)
    } catch (error) {
      console.error("Error loading notification data:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendInvitations = async () => {
    if (!emailList.trim()) return

    setIsSending(true)
    try {
      const emails = emailList
        .split(/[,\n]/)
        .map((email) => email.trim())
        .filter((email) => email && email.includes("@"))

      const response = await apiClient.request(`/notifications/${eventId}/send-invitations`, {
        method: "POST",
        body: JSON.stringify({ recipient_emails: emails }),
      })

      if (response.data) {
        setEmailList("")
        loadNotificationData()
      }
    } catch (error) {
      console.error("Error sending invitations:", error)
    } finally {
      setIsSending(false)
    }
  }

  const handleSendReminders = async () => {
    setIsSending(true)
    try {
      const response = await apiClient.request(`/notifications/${eventId}/send-reminders`, {
        method: "POST",
      })

      if (response.data) {
        loadNotificationData()
      }
    } catch (error) {
      console.error("Error sending reminders:", error)
    } finally {
      setIsSending(false)
    }
  }

  const handleSendTestEmail = async () => {
    if (!testEmail.trim()) return

    try {
      const response = await apiClient.request("/notifications/test-email", {
        method: "POST",
        body: JSON.stringify({ recipient_email: testEmail }),
      })

      if (response.data) {
        setTestEmail("")
      }
    } catch (error) {
      console.error("Error sending test email:", error)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "sent":
      case "delivered":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "failed":
      case "bounced":
        return <XCircle className="h-4 w-4 text-red-500" />
      case "pending":
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-gray-500" />
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case "invitation":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
      case "reminder":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
      case "confirmation":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading notification data...</div>
  }

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Sent</CardTitle>
              <Mail className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_sent}</div>
              <p className="text-xs text-muted-foreground">All notifications</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Delivered</CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_delivered}</div>
              <p className="text-xs text-muted-foreground">Successfully delivered</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Open Rate</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.open_rate}%</div>
              <p className="text-xs text-muted-foreground">{stats.total_opened} opened</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Click Rate</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.click_rate}%</div>
              <p className="text-xs text-muted-foreground">{stats.total_clicked} clicked</p>
            </CardContent>
          </Card>
        </div>
      )}

      <Tabs defaultValue="send" className="space-y-4">
        <TabsList>
          <TabsTrigger value="send">Send Notifications</TabsTrigger>
          <TabsTrigger value="history">Communication History</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="send" className="space-y-4">
          <div className="grid gap-6 md:grid-cols-2">
            {/* Send Invitations */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Send className="h-5 w-5" />
                  Send Invitations
                </CardTitle>
                <CardDescription>Send event invitations to new recipients</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email-list">Email Addresses</Label>
                  <Textarea
                    id="email-list"
                    placeholder="Enter email addresses separated by commas or new lines&#10;example@email.com, another@email.com"
                    value={emailList}
                    onChange={(e) => setEmailList(e.target.value)}
                    rows={4}
                  />
                </div>
                <Button onClick={handleSendInvitations} disabled={isSending || !emailList.trim()} className="w-full">
                  {isSending ? "Sending..." : "Send Invitations"}
                </Button>
              </CardContent>
            </Card>

            {/* Send Reminders */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Send Reminders
                </CardTitle>
                <CardDescription>Send reminder emails to all RSVPs</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  This will send reminder emails to all people who have RSVPed to this event, regardless of their
                  response status.
                </p>
                <Button onClick={handleSendReminders} disabled={isSending} className="w-full">
                  {isSending ? "Sending..." : "Send Reminders"}
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="history" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Communication History</CardTitle>
              <CardDescription>View all notifications sent for this event</CardDescription>
            </CardHeader>
            <CardContent>
              {communications.length === 0 ? (
                <div className="text-center py-8">
                  <Mail className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No communications yet</h3>
                  <p className="text-muted-foreground">Send your first invitation to get started</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {communications.map((comm) => (
                    <div key={comm.id} className="flex items-start justify-between p-4 border rounded-lg">
                      <div className="flex items-start gap-3">
                        {getStatusIcon(comm.delivery_status)}
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <Badge className={getTypeColor(comm.type)}>{comm.type}</Badge>
                            <span className="text-sm font-medium">{comm.subject}</span>
                          </div>
                          <p className="text-sm text-muted-foreground">
                            To: {comm.recipient_name || comm.recipient_email}
                          </p>
                          <p className="text-xs text-muted-foreground">Sent: {formatDate(comm.sent_at)}</p>
                          {comm.opened_at && (
                            <p className="text-xs text-green-600">Opened: {formatDate(comm.opened_at)}</p>
                          )}
                        </div>
                      </div>
                      <Badge variant="outline" className="capitalize">
                        {comm.delivery_status}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Email Settings
              </CardTitle>
              <CardDescription>Test and configure email notifications</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="test-email">Test Email Address</Label>
                <div className="flex gap-2">
                  <Input
                    id="test-email"
                    type="email"
                    placeholder="your@email.com"
                    value={testEmail}
                    onChange={(e) => setTestEmail(e.target.value)}
                  />
                  <Button onClick={handleSendTestEmail} disabled={!testEmail.trim()}>
                    Send Test
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground">
                  Send a test email to verify your email configuration is working
                </p>
              </div>

              <Separator />

              <div className="space-y-2">
                <h4 className="text-sm font-medium">Email Templates</h4>
                <p className="text-xs text-muted-foreground">
                  Customize your notification templates in the settings section
                </p>
                <Button variant="outline" size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Manage Templates
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
