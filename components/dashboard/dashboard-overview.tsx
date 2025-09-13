"use client"

import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Users, BarChart3, Puzzle, Plus, TrendingUp, Eye, Edit, Calendar } from "lucide-react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts"

// Mock data for charts
const contentData = [
  { name: "Mon", articles: 4, pages: 2 },
  { name: "Tue", articles: 3, pages: 1 },
  { name: "Wed", articles: 6, pages: 3 },
  { name: "Thu", articles: 8, pages: 2 },
  { name: "Fri", articles: 5, pages: 4 },
  { name: "Sat", articles: 2, pages: 1 },
  { name: "Sun", articles: 3, pages: 2 },
]

const trafficData = [
  { name: "Jan", visitors: 1200 },
  { name: "Feb", visitors: 1900 },
  { name: "Mar", visitors: 1700 },
  { name: "Apr", visitors: 2400 },
  { name: "May", visitors: 2100 },
  { name: "Jun", visitors: 2800 },
]

const recentActivity = [
  {
    id: 1,
    title: "New article published",
    description: "Getting Started with Next.js",
    time: "2 hours ago",
    type: "content",
  },
  {
    id: 2,
    title: "User registered",
    description: "john.doe@example.com",
    time: "4 hours ago",
    type: "user",
  },
  {
    id: 3,
    title: "Module activated",
    description: "SEO Optimizer",
    time: "1 day ago",
    type: "module",
  },
  {
    id: 4,
    title: "Page updated",
    description: "About Us page",
    time: "2 days ago",
    type: "content",
  },
]

const quickActions = [
  {
    title: "Create Article",
    description: "Write a new article with AI assistance",
    icon: FileText,
    href: "/content/create?type=article",
    color: "bg-blue-500",
  },
  {
    title: "Add Page",
    description: "Build a new page for your site",
    icon: Edit,
    href: "/content/create?type=page",
    color: "bg-green-500",
  },
  {
    title: "View Analytics",
    description: "Check your site performance",
    icon: BarChart3,
    href: "/analytics",
    color: "bg-purple-500",
  },
  {
    title: "Manage Modules",
    description: "Install or configure modules",
    icon: Puzzle,
    href: "/modules",
    color: "bg-orange-500",
  },
]

export function DashboardOverview() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance text-black">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's what's happening with your site.</p>
        </div>
        <Link href="/content/create">
          <Button className="gap-2 bg-black text-white hover:bg-gray-800">
            <Plus className="h-4 w-4" />
            Create Content
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-white border-gray-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">Total Content</CardTitle>
            <FileText className="h-4 w-4 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-black">127</div>
            <p className="text-xs text-gray-600">
              <span className="text-green-600 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                +12%
              </span>
              from last month
            </p>
          </CardContent>
        </Card>

        <Card className="bg-white border-gray-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">Published</CardTitle>
            <Eye className="h-4 w-4 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-black">89</div>
            <p className="text-xs text-gray-600">
              <span className="text-green-600 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                +8%
              </span>
              from last month
            </p>
          </CardContent>
        </Card>

        <Card className="bg-white border-gray-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">Monthly Visitors</CardTitle>
            <Users className="h-4 w-4 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-black">2,847</div>
            <p className="text-xs text-gray-600">
              <span className="text-green-600 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                +23%
              </span>
              from last month
            </p>
          </CardContent>
        </Card>

        <Card className="bg-white border-gray-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-700">Active Modules</CardTitle>
            <Puzzle className="h-4 w-4 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-black">7</div>
            <p className="text-xs text-gray-600">
              <span className="text-green-600 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                +2
              </span>
              new this month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts and Activity */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Content Creation Chart */}
        <Card className="bg-white border-gray-200">
          <CardHeader>
            <CardTitle className="text-black">Content Creation</CardTitle>
            <CardDescription className="text-gray-600">Articles and pages created this week</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={contentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="articles" fill="#000000" />
                <Bar dataKey="pages" fill="#6b7280" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Traffic Chart */}
        <Card className="bg-white border-gray-200">
          <CardHeader>
            <CardTitle className="text-black">Site Traffic</CardTitle>
            <CardDescription className="text-gray-600">Monthly visitors over the last 6 months</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="visitors" stroke="#000000" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions and Recent Activity */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Quick Actions */}
        <Card className="lg:col-span-2 bg-white border-gray-200">
          <CardHeader>
            <CardTitle className="text-black">Quick Actions</CardTitle>
            <CardDescription className="text-gray-600">Common tasks to get things done faster</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              {quickActions.map((action) => {
                const Icon = action.icon
                return (
                  <Link key={action.title} href={action.href}>
                    <Button
                      variant="outline"
                      className="h-auto p-4 justify-start bg-white border-gray-200 hover:bg-gray-50 hover:border-gray-300 w-full text-left"
                    >
                      <div className="flex items-start gap-3 w-full">
                        <div className={`p-2 rounded-md ${action.color} flex-shrink-0`}>
                          <Icon className="h-4 w-4 text-white" />
                        </div>
                        <div className="text-left min-w-0 flex-1">
                          <div className="font-medium text-black text-sm">{action.title}</div>
                          <div className="text-sm text-gray-600 mt-1">{action.description}</div>
                        </div>
                      </div>
                    </Button>
                  </Link>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="bg-white border-gray-200">
          <CardHeader>
            <CardTitle className="text-black">Recent Activity</CardTitle>
            <CardDescription className="text-gray-600">Latest updates and changes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start gap-3">
                  <div className="mt-1">
                    {activity.type === "content" && <div className="h-2 w-2 rounded-full bg-blue-500" />}
                    {activity.type === "user" && <div className="h-2 w-2 rounded-full bg-green-500" />}
                    {activity.type === "module" && <div className="h-2 w-2 rounded-full bg-purple-500" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-black">{activity.title}</p>
                    <p className="text-sm text-gray-600 truncate">{activity.description}</p>
                    <p className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                      <Calendar className="h-3 w-3" />
                      {activity.time}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
