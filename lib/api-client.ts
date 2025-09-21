interface APIResponse<T> {
  data?: T
  error?: string
  message?: string
}

class APIClient {
  private baseURL: string
  private token: string | null = null

  constructor(baseURL = "http://localhost:8000/api") {
    this.baseURL = baseURL

    // Get token from localStorage if available
    if (typeof window !== "undefined") {
      this.token = localStorage.getItem("auth_token")
    }
  }

  setToken(token: string) {
    this.token = token
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", token)
    }
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<APIResponse<T>> {
    const url = `${this.baseURL}${endpoint}`
    // If the caller provided a FormData body, don't force a JSON content-type
    const isFormData = typeof FormData !== 'undefined' && options.body instanceof FormData

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    }

    if (this.token) {
      ;(headers as Record<string, string>).Authorization = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      // Some endpoints may return an empty body (204). Read the raw text and
      // attempt JSON.parse only when there is content to avoid thrown errors.
      const text = await response.text()
      let data: any = undefined
      try {
        data = text ? JSON.parse(text) : undefined
      } catch (err) {
        // If response isn't JSON, keep the raw text
        data = text
      }

      if (!response.ok) {
        const errMsg = data && (data.detail || data.error || data.message)
        return { error: errMsg || 'An error occurred' }
      }

      return { data }
    } catch (error) {
      return { error: 'Network error occurred' }
    }
  }

  // Auth endpoints
  async login(username: string, password: string) {
    const formData = new FormData()
    formData.append("username", username)
    formData.append("password", password)

    return this.request<{ access_token: string; token_type: string }>("/auth/token", {
      method: "POST",
      headers: {},
      body: formData,
    })
  }

  async register(userData: {
    email: string
    username: string
    password: string
    full_name: string
  }) {
    return this.request<any>("/auth/register", {
      method: "POST",
      body: JSON.stringify(userData),
    })
  }

  async getCurrentUser() {
    return this.request<any>("/auth/me")
  }

  // Content endpoints
  async getContent(params?: {
    skip?: number
    limit?: number
    content_type?: string
    status?: string
    search?: string
  }) {
    const searchParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString())
        }
      })
    }

    const endpoint = `/content${searchParams.toString() ? `?${searchParams.toString()}` : ""}`
    return this.request<any[]>(endpoint)
  }

  async getContentById(id: string) {
    return this.request<any>(`/content/${id}`)
  }

  async createContent(contentData: any) {
    return this.request<any>("/content", {
      method: "POST",
      body: JSON.stringify(contentData),
    })
  }

  async updateContent(id: string, contentData: any) {
    return this.request<any>(`/content/${id}`, {
      method: "PUT",
      body: JSON.stringify(contentData),
    })
  }

  async deleteContent(id: string) {
    return this.request<any>(`/content/${id}`, {
      method: "DELETE",
    })
  }

  async generateAISuggestions(id: string) {
    return this.request<any>(`/content/${id}/ai-suggestions`, {
      method: "POST",
    })
  }

  // AI endpoints
  async generateAIContent(prompt: string, model?: string) {
    return this.request<{
      content: string
      provider: string
      model?: string
      usage?: any
    }>("/ai/generate-content", {
      method: "POST",
      body: JSON.stringify({ prompt, model }),
    })
  }

  async getAIProviders() {
    return this.request<any[]>("/ai/providers")
  }

  async createAIProvider(providerData: {
    name: string
    display_name: string
    api_key: string
    base_url?: string
    is_active: boolean
    configuration?: any
  }) {
    return this.request<any>("/ai/providers", {
      method: "POST",
      body: JSON.stringify(providerData),
    })
  }

  // Dashboard endpoints
  async getDashboardStats() {
    return this.request<{
      total_content: number
      published_content: number
      draft_content: number
      total_users: number
      active_modules: number
      recent_activity: any[]
    }>("/dashboard/stats")
  }

  async getQuickActions() {
    return this.request<any[]>("/dashboard/quick-actions")
  }

  async getAnalyticsOverview(days = 30) {
    return this.request<any>(`/dashboard/analytics?days=${days}`)
  }

  // Module endpoints
  async getAvailableModules(category?: string) {
    const endpoint = `/modules/available${category ? `?category=${category}` : ""}`
    return this.request<any[]>(endpoint)
  }

  async getInstalledModules() {
    return this.request<any[]>("/modules/installed")
  }

  async installModule(moduleName: string, moduleData: any) {
    return this.request<any>(`/modules/install/${moduleName}`, {
      method: "POST",
      body: JSON.stringify(moduleData),
    })
  }

  async updateModule(moduleId: number, moduleData: any) {
    return this.request<any>(`/modules/${moduleId}`, {
      method: "PUT",
      body: JSON.stringify(moduleData),
    })
  }

  async activateModule(moduleId: number) {
    return this.request<any>(`/modules/${moduleId}/activate`, {
      method: "POST",
    })
  }

  async deactivateModule(moduleId: number) {
    return this.request<any>(`/modules/${moduleId}/deactivate`, {
      method: "POST",
    })
  }

  async uninstallModule(moduleId: number) {
    return this.request<any>(`/modules/${moduleId}`, {
      method: "DELETE",
    })
  }

  // Settings endpoints
  async getSettings() {
    return this.request<any[]>("/settings")
  }

  async getSetting(key: string) {
    return this.request<any>(`/settings/${key}`)
  }

  async createSetting(settingData: {
    key: string
    value: any
    description?: string
  }) {
    return this.request<any>("/settings", {
      method: "POST",
      body: JSON.stringify(settingData),
    })
  }

  async updateSetting(
    key: string,
    settingData: {
      value: any
      description?: string
    },
  ) {
    return this.request<any>(`/settings/${key}`, {
      method: "PUT",
      body: JSON.stringify(settingData),
    })
  }

  async deleteSetting(key: string) {
    return this.request<any>(`/settings/${key}`, {
      method: "DELETE",
    })
  }

  async getSiteConfig() {
    return this.request<any>("/settings/config/site")
  }

  async updateSiteConfig(configData: any) {
    return this.request<any>("/settings/config/site", {
      method: "POST",
      body: JSON.stringify(configData),
    })
  }

  async initializeDefaultSettings() {
    return this.request<any>("/settings/initialize-defaults", {
      method: "POST",
    })
  }

  // Event endpoints
  async getEvents(params?: {
    skip?: number
    limit?: number
    status?: string
  }) {
    const searchParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString())
        }
      })
    }

    const endpoint = `/events${searchParams.toString() ? `?${searchParams.toString()}` : ""}`
    return this.request<any[]>(endpoint)
  }

  async getEventById(id: number) {
    return this.request<any>(`/events/${id}`)
  }

  async createEvent(eventData: {
    title: string
    description?: string
    event_type?: string
    start_date: string
    end_date?: string
    location?: string
    max_attendees?: number
    rsvp_deadline?: string
    require_approval?: boolean
    allow_guests?: boolean
    send_reminders?: boolean
    reminder_days_before?: number[]
  }) {
    return this.request<any>("/events", {
      method: "POST",
      body: JSON.stringify(eventData),
    })
  }

  async updateEvent(id: number, eventData: any) {
    return this.request<any>(`/events/${id}`, {
      method: "PUT",
      body: JSON.stringify(eventData),
    })
  }

  async deleteEvent(id: number) {
    return this.request<any>(`/events/${id}`, {
      method: "DELETE",
    })
  }

  async createRSVP(
    eventId: number,
    rsvpData: {
      email: string
      name: string
      phone?: string
      company?: string
      guest_count?: number
      dietary_restrictions?: string
      special_requests?: string
    },
  ) {
    return this.request<any>(`/events/${eventId}/rsvps`, {
      method: "POST",
      body: JSON.stringify({ event_id: eventId, ...rsvpData }),
    })
  }

  async updateRSVP(
    rsvpId: number,
    rsvpData: {
      status: string
      guest_count?: number
      dietary_restrictions?: string
      special_requests?: string
    },
  ) {
    return this.request<any>(`/events/rsvps/${rsvpId}`, {
      method: "PUT",
      body: JSON.stringify(rsvpData),
    })
  }

  async sendInvitations(eventId: number, emails: string[]) {
    return this.request<any>(`/events/${eventId}/send-invitations`, {
      method: "POST",
      body: JSON.stringify(emails),
    })
  }

  async getEventAnalytics(eventId: number) {
    return this.request<any>(`/events/${eventId}/analytics`)
  }

  // Portfolio endpoints
  async getPortfolioSummary() {
    return this.request<any>(`/v1/portfolio/summary`)
  }

  async getPortfolioProjects(featuredOnly = false) {
    const query = featuredOnly ? '?featured_only=true' : ''
    return this.request<any>(`/v1/portfolio/projects${query}`)
  }

  async getPortfolioSkills() {
    return this.request<any>(`/v1/portfolio/skills`)
  }

  async getPortfolioExperience() {
    return this.request<any>(`/v1/portfolio/experience`)
  }

  // RSVP Methods
  async getAllRsvps() {
    return this.request<any[]>(`/events/all-rsvps`)
  }

  // Notification Methods
  async getNotificationStats(eventId: number) {
    return this.request<any>(`/notifications/${eventId}/notification-stats`)
  }

  async getCommunications(eventId: number) {
    return this.request<any[]>(`/notifications/${eventId}/communications`)
  }

  async sendNotificationInvitations(eventId: number, recipientEmails: string[]) {
    return this.request<any>(`/notifications/${eventId}/send-invitations`, {
      method: "POST",
      body: JSON.stringify({ recipient_emails: recipientEmails }),
    })
  }

  async sendReminders(eventId: number) {
    return this.request<any>(`/notifications/${eventId}/send-reminders`, {
      method: "POST",
    })
  }

  async sendTestEmail(recipientEmail: string) {
    return this.request<any>("/notifications/test-email", {
      method: "POST",
      body: JSON.stringify({ recipient_email: recipientEmail }),
    })
  }
}

export const apiClient = new APIClient()
