"use client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { MapPin, Users, Clock, MoreHorizontal, Edit, Trash2, Send, BarChart3 } from "lucide-react"

interface Event {
  id: number
  title: string
  description?: string
  event_type: string
  start_date: string
  end_date?: string
  location?: string
  status: string
  total_rsvps: number
  accepted_rsvps: number
  declined_rsvps: number
  pending_rsvps: number
  created_at: string
}

interface EventListProps {
  events: Event[]
  onEventEdit?: (event: Event) => void
  onEventDelete?: (eventId: number) => void
  onSendInvitations?: (eventId: number) => void
  onViewAnalytics?: (eventId: number) => void
}

export function EventList({ events, onEventEdit, onEventDelete, onSendInvitations, onViewAnalytics }: EventListProps) {
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case "meeting":
        return "👥"
      case "webinar":
        return "💻"
      case "conference":
        return "🎤"
      case "workshop":
        return "🛠️"
      case "networking":
        return "🤝"
      case "social":
        return "🎉"
      default:
        return "📅"
    }
  }

  return (
    <div className="space-y-4">
      {events.map((event) => (
        <Card key={event.id} className="hover:shadow-md transition-shadow">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{getEventTypeIcon(event.event_type)}</span>
                  <CardTitle className="text-xl">{event.title}</CardTitle>
                  <Badge className={getStatusColor(event.status)}>{event.status}</Badge>
                </div>
                {event.description && <CardDescription className="text-base">{event.description}</CardDescription>}
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => onEventEdit?.(event)}>
                    <Edit className="h-4 w-4 mr-2" />
                    Edit Event
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => onSendInvitations?.(event.id)}>
                    <Send className="h-4 w-4 mr-2" />
                    Send Invitations
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => onViewAnalytics?.(event.id)}>
                    <BarChart3 className="h-4 w-4 mr-2" />
                    View Analytics
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => onEventDelete?.(event.id)} className="text-red-600">
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete Event
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                {formatDate(event.start_date)}
              </div>
              {event.location && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <MapPin className="h-4 w-4" />
                  {event.location}
                </div>
              )}
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Users className="h-4 w-4" />
                {event.total_rsvps} RSVPs
              </div>
              <div className="text-sm">
                <span className="text-green-600 font-medium">{event.accepted_rsvps} accepted</span>
                {event.pending_rsvps > 0 && <span className="text-yellow-600 ml-2">{event.pending_rsvps} pending</span>}
                {event.declined_rsvps > 0 && <span className="text-red-600 ml-2">{event.declined_rsvps} declined</span>}
              </div>
            </div>

            {/* RSVP Progress Bar */}
            {event.total_rsvps > 0 && (
              <div className="mt-4">
                <div className="flex justify-between text-xs text-muted-foreground mb-1">
                  <span>RSVP Progress</span>
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
  )
}
