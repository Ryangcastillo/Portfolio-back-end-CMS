// API service for connecting to the headless CMS backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

class PortfolioAPI {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL
  }

  async fetchJSON(url, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${url}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed: ${url}`, error)
      throw error
    }
  }

  // Profile endpoints
  async getProfile() {
    return this.fetchJSON('/api/public/profile')
  }

  async getStats() {
    return this.fetchJSON('/api/public/stats')
  }

  // Skills endpoints
  async getSkills(params = {}) {
    const searchParams = new URLSearchParams()
    if (params.featured_only) searchParams.set('featured_only', 'true')
    if (params.category) searchParams.set('category', params.category)
    
    const queryString = searchParams.toString()
    const url = `/api/public/skills${queryString ? `?${queryString}` : ''}`
    return this.fetchJSON(url)
  }

  async getFeaturedSkills() {
    return this.getSkills({ featured_only: true })
  }

  // Projects endpoints
  async getProjects(params = {}) {
    const searchParams = new URLSearchParams()
    if (params.featured_only) searchParams.set('featured_only', 'true')
    if (params.category) searchParams.set('category', params.category)
    if (params.limit) searchParams.set('limit', params.limit.toString())
    
    const queryString = searchParams.toString()
    const url = `/api/public/projects${queryString ? `?${queryString}` : ''}`
    return this.fetchJSON(url)
  }

  async getFeaturedProjects(limit = 3) {
    return this.getProjects({ featured_only: true, limit })
  }

  async getProject(projectId) {
    return this.fetchJSON(`/api/public/projects/${projectId}`)
  }

  async getProjectCategories() {
    return this.fetchJSON('/api/public/project-categories')
  }

  // Experience endpoints
  async getExperience(params = {}) {
    const searchParams = new URLSearchParams()
    if (params.featured_only) searchParams.set('featured_only', 'true')
    
    const queryString = searchParams.toString()
    const url = `/api/public/experience${queryString ? `?${queryString}` : ''}`
    return this.fetchJSON(url)
  }

  // Testimonials endpoints
  async getTestimonials(params = {}) {
    const searchParams = new URLSearchParams()
    if (params.featured_only) searchParams.set('featured_only', 'true')
    if (params.limit) searchParams.set('limit', params.limit.toString())
    
    const queryString = searchParams.toString()
    const url = `/api/public/testimonials${queryString ? `?${queryString}` : ''}`
    return this.fetchJSON(url)
  }

  // Convenience endpoints
  async getHomepageData() {
    return this.fetchJSON('/api/public/homepage-data')
  }

  async getPortfolioOverview() {
    return this.fetchJSON('/api/public/portfolio-overview')
  }
}

// Create a singleton instance
const portfolioAPI = new PortfolioAPI()

// Hook for React components
export const usePortfolioAPI = () => {
  return portfolioAPI
}

export default portfolioAPI

// Utility function to handle loading states and errors
export const withErrorHandling = async (apiCall, fallbackData = null) => {
  try {
    return await apiCall()
  } catch (error) {
    console.error('API Error:', error)
    return fallbackData
  }
}