"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ArrowLeft, Calendar, MapPin, Users, Clock, Settings, Mail } from "lucide-react"
import { DashboardLayout } from "@/components/dashboard/dashboard-layout"
import { NotificationPanel } from "@/components/events/notification-panel"
import { apiClient } from "@/lib/api-client"
import Link from "next/link"

interface Event {
  id: number
  title: string
  description?: string
  event_type: string
  start_date: string
  end_date?: string
  location?: string
  status: string
  max_attendees?: number
  rsvp_deadline?: string
  require_approval: boolean
  allow_guests: boolean
  send_reminders: boolean
  reminder_days_before: number[]
  created_at: string
}

interface RSVP {
  id: number
  email: string
  name: string
  phone?: string
  company?: string
  status: string
  guest_count: number
  dietary_restrictions?: string
  special_requests?: string
  responded_at?: string
  created_at: string
}

export default function EventDetailPage() {
  const params = useParams()
  const eventId = Number.parseInt(params.id as string)

  const [event, setEvent] = useState<Event | null>(null)
  const [rsvps, setRsvps] = useState<RSVP[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (eventId) {
      loadEventDetails()
    }
  }, [eventId])

  const loadEventDetails = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.getEventById(eventId)
      if (response.data) {
        setEvent(response.data.event)
        setRsvps(response.data.rsvps || [])
      }
    } catch (error) {
      console.error("Error loading event details:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "published":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      case "draft":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
      case "cancelled":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
    }
  }

  const getRsvpStatusColor = (status: string) => {
    switch (status) {
      case "accepted":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
      case "declined":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
      case "maybe":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
      case "pending":
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="text-center py-8">Loading event details...</div>
      </DashboardLayout>
    )
  }

  if (!event) {
    return (
      <DashboardLayout>
        <div className="text-center py-8">
          <h2 className="text-2xl font-bold mb-4">Event not found</h2>
          <Link href="/events">
            <Button>Back to Events</Button>
          </Link>
        </div>
      </DashboardLayout>
    )
  }

  const acceptedRsvps = rsvps.filter((r) => r.status === "accepted")
  const declinedRsvps = rsvps.filter((r) => r.status === "declined")
  const pendingRsvps = rsvps.filter((r) => r.status === "pending")
  const maybeRsvps = rsvps.filter((r) => r.status === "maybe")

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <Link href="/events">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h1 className="text-3xl font-bold text-balance">{event.title}</h1>
              <Badge className={getStatusColor(event.status)}>{event.status}</Badge>
            </div>
            {event.description && <p className="text-muted-foreground">{event.description}</p>}
          </div>
          <Button>
            <Settings className="h-4 w-4 mr-2" />
            Edit Event
          </Button>
        </div>

        {/* Event Details Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Event Details
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="font-medium">Start Date</p>
                  <p className="text-sm text-muted-foreground">{formatDate(event.start_date)}</p>
                </div>
              </div>

              {event.end_date && (
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">End Date</p>
                    <p className="text-sm text-muted-foreground">{formatDate(event.end_date)}</p>
                  </div>
                </div>
              )}

              {event.location && (
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Location</p>
                    <p className="text-sm text-muted-foreground">{event.location}</p>
                  </div>
                </div>
              )}

              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="font-medium">Event Type</p>
                  <p className="text-sm text-muted-foreground capitalize">{event.event_type}</p>
                </div>
              </div>

              {event.max_attendees && (
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Max Attendees</p>
                    <p className="text-sm text-muted-foreground">{event.max_attendees}</p>
                  </div>
                </div>
              )}

              {event.rsvp_deadline && (
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">RSVP Deadline</p>
                    <p className="text-sm text-muted-foreground">{formatDate(event.rsvp_deadline)}</p>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* RSVP Stats */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total RSVPs</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{rsvps.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Accepted</CardTitle>
              <Users className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{acceptedRsvps.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
              <Users className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{pendingRsvps.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Declined</CardTitle>
              <Users className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{declinedRsvps.length}</div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="rsvps" className="space-y-4">
          <TabsList>
            <TabsTrigger value="rsvps">RSVPs</TabsTrigger>
            <TabsTrigger value="notifications">
              <Mail className="h-4 w-4 mr-2" />
              Notifications
            </TabsTrigger>
          </TabsList>

          <TabsContent value="rsvps" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>RSVP List</CardTitle>
                <CardDescription>Manage event attendees and their responses</CardDescription>
              </CardHeader>
              <CardContent>
                {rsvps.length === 0 ? (
                  <div className="text-center py-8">
                    <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">No RSVPs yet</h3>
                    <p className="text-muted-foreground">Send invitations to start collecting RSVPs</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {rsvps.map((rsvp) => (
                      <div key={rsvp.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <p className="font-medium">{rsvp.name || rsvp.email}</p>
                            <Badge className={getRsvpStatusColor(rsvp.status)}>{rsvp.status}</Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{rsvp.email}</p>
                          {rsvp.company && <p className="text-sm text-muted-foreground">Company: {rsvp.company}</p>}
                          {rsvp.guest_count > 1 && (
                            <p className="text-sm text-muted-foreground">Guests: {rsvp.guest_count}</p>
                          )}
                          {rsvp.responded_at && (
                            <p className="text-xs text-muted-foreground">Responded: {formatDate(rsvp.responded_at)}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications">
            <NotificationPanel eventId={eventId} />
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}
