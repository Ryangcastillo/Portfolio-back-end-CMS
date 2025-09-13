"use client"

import { useState, useEffect } from "react"
import { DashboardLayout } from "@/components/dashboard/dashboard-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Users, Calendar, Mail, BarChart3, Search, Download } from "@/components/ui/icons"
import { apiClient } from "@/lib/api-client"

interface Event {
  id: number
  title: string
  start_date: string
  location?: string
  total_rsvps: number
  accepted_rsvps: number
  declined_rsvps: number
  pending_rsvps: number
  maybe_rsvps: number
}

interface RSVP {
  id: number
  event_id: number
  event_title: string
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

export default function RSVPManagementPage() {
  const [events, setEvents] = useState<Event[]>([])
  const [allRsvps, setAllRsvps] = useState<RSVP[]>([])
  const [filteredRsvps, setFilteredRsvps] = useState<RSVP[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [eventFilter, setEventFilter] = useState("all")

  useEffect(() => {
    loadRSVPData()
  }, [])

  useEffect(() => {
    filterRsvps()
  }, [allRsvps, searchTerm, statusFilter, eventFilter])

  const loadRSVPData = async () => {
    setIsLoading(true)
    try {
      const [eventsResponse, rsvpsResponse] = await Promise.all([
        apiClient.getEvents(),
        apiClient.request("/events/all-rsvps", { method: "GET" }),
      ])

      if (eventsResponse.data) setEvents(eventsResponse.data)
      if (rsvpsResponse.data) setAllRsvps(rsvpsResponse.data)
    } catch (error) {
      console.error("Error loading RSVP data:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const filterRsvps = () => {
    let filtered = allRsvps

    if (searchTerm) {
      filtered = filtered.filter(
        (rsvp) =>
          rsvp.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          rsvp.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
          rsvp.company?.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter((rsvp) => rsvp.status === statusFilter)
    }

    if (eventFilter !== "all") {
      filtered = filtered.filter((rsvp) => rsvp.event_id === Number.parseInt(eventFilter))
    }

    setFilteredRsvps(filtered)
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
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  const totalRsvps = allRsvps.length
  const acceptedCount = allRsvps.filter((r) => r.status === "accepted").length
  const pendingCount = allRsvps.filter((r) => r.status === "pending").length
  const declinedCount = allRsvps.filter((r) => r.status === "declined").length

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="text-center py-8">Loading RSVP data...</div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-balance">RSVP Management</h1>
            <p className="text-muted-foreground">Manage all event RSVPs from one central location</p>
          </div>
          <Button>
            <Download className="h-4 w-4 mr-2" />
            Export RSVPs
          </Button>
        </div>

        {/* Overview Stats */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total RSVPs</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalRsvps}</div>
              <p className="text-xs text-muted-foreground">Across all events</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Accepted</CardTitle>
              <Users className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{acceptedCount}</div>
              <p className="text-xs text-muted-foreground">
                {totalRsvps > 0 ? Math.round((acceptedCount / totalRsvps) * 100) : 0}% acceptance rate
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
              <Users className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{pendingCount}</div>
              <p className="text-xs text-muted-foreground">Awaiting response</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Declined</CardTitle>
              <Users className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{declinedCount}</div>
              <p className="text-xs text-muted-foreground">Cannot attend</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="all-rsvps" className="space-y-4">
          <TabsList>
            <TabsTrigger value="all-rsvps">All RSVPs</TabsTrigger>
            <TabsTrigger value="by-event">By Event</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          <TabsContent value="all-rsvps" className="space-y-4">
            {/* Filters */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Filter RSVPs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 flex-wrap">
                  <div className="flex-1 min-w-[200px]">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                      <Input
                        placeholder="Search by name, email, or company..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>

                  <Select value={statusFilter} onValueChange={setStatusFilter}>
                    <SelectTrigger className="w-[150px]">
                      <SelectValue placeholder="Status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Status</SelectItem>
                      <SelectItem value="accepted">Accepted</SelectItem>
                      <SelectItem value="pending">Pending</SelectItem>
                      <SelectItem value="declined">Declined</SelectItem>
                      <SelectItem value="maybe">Maybe</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select value={eventFilter} onValueChange={setEventFilter}>
                    <SelectTrigger className="w-[200px]">
                      <SelectValue placeholder="Event" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Events</SelectItem>
                      {events.map((event) => (
                        <SelectItem key={event.id} value={event.id.toString()}>
                          {event.title}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* RSVP List */}
            <Card>
              <CardHeader>
                <CardTitle>RSVPs ({filteredRsvps.length})</CardTitle>
                <CardDescription>All RSVP responses across your events</CardDescription>
              </CardHeader>
              <CardContent>
                {filteredRsvps.length === 0 ? (
                  <div className="text-center py-8">
                    <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">No RSVPs found</h3>
                    <p className="text-muted-foreground">Try adjusting your filters or create some events</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {filteredRsvps.map((rsvp) => (
                      <div key={rsvp.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <p className="font-medium">{rsvp.name || rsvp.email}</p>
                            <Badge className={getRsvpStatusColor(rsvp.status)}>{rsvp.status}</Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{rsvp.email}</p>
                          <p className="text-sm text-muted-foreground">Event: {rsvp.event_title}</p>
                          {rsvp.company && <p className="text-sm text-muted-foreground">Company: {rsvp.company}</p>}
                          {rsvp.guest_count > 1 && (
                            <p className="text-sm text-muted-foreground">Guests: {rsvp.guest_count}</p>
                          )}
                          {rsvp.responded_at && (
                            <p className="text-xs text-muted-foreground">Responded: {formatDate(rsvp.responded_at)}</p>
                          )}
                        </div>
                        <div className="flex items-center gap-2">
                          <Button variant="outline" size="sm">
                            <Mail className="h-4 w-4 mr-2" />
                            Contact
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="by-event" className="space-y-4">
            <div className="grid gap-4">
              {events.map((event) => (
                <Card key={event.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          <Calendar className="h-5 w-5" />
                          {event.title}
                        </CardTitle>
                        <CardDescription>
                          {formatDate(event.start_date)} {event.location && `• ${event.location}`}
                        </CardDescription>
                      </div>
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-4 md:grid-cols-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold">{event.total_rsvps}</div>
                        <p className="text-sm text-muted-foreground">Total</p>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{event.accepted_rsvps}</div>
                        <p className="text-sm text-muted-foreground">Accepted</p>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-yellow-600">{event.pending_rsvps}</div>
                        <p className="text-sm text-muted-foreground">Pending</p>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{event.declined_rsvps}</div>
                        <p className="text-sm text-muted-foreground">Declined</p>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    {event.total_rsvps > 0 && (
                      <div className="mt-4">
                        <div className="flex justify-between text-xs text-muted-foreground mb-1">
                          <span>Response Progress</span>
                          <span>{Math.round((event.accepted_rsvps / event.total_rsvps) * 100)}% accepted</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                          <div className="flex h-2 rounded-full overflow-hidden">
                            <div
                              className="bg-green-500"
                              style={{ width: `${(event.accepted_rsvps / event.total_rsvps) * 100}%` }}
                            />
                            <div
                              className="bg-yellow-500"
                              style={{ width: `${(event.pending_rsvps / event.total_rsvps) * 100}%` }}
                            />
                            <div
                              className="bg-red-500"
                              style={{ width: `${(event.declined_rsvps / event.total_rsvps) * 100}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  RSVP Analytics
                </CardTitle>
                <CardDescription>Insights and trends across all your events</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <BarChart3 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Analytics Coming Soon</h3>
                  <p className="text-muted-foreground">
                    Detailed analytics and reporting features will be available here
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}
