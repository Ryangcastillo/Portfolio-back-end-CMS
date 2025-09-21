import { Github, Linkedin, Mail, MapPin } from 'lucide-react'
import { Button } from '@/components/ui/button'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-muted/50 border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">RC</span>
              </div>
              <span className="font-bold text-xl">Ryan Castillo</span>
            </div>
            <p className="text-muted-foreground mb-4 max-w-md">
              Data Analyst & Process Improvement Specialist with 8+ years of experience 
              transforming business challenges into actionable insights through advanced 
              analytics and AI innovation.
            </p>
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              <MapPin className="w-4 h-4" />
              <span>Auckland, New Zealand</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-muted-foreground hover:text-primary transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a href="/data-analysis" className="text-muted-foreground hover:text-primary transition-colors">
                  Data Analysis
                </a>
              </li>
              <li>
                <a href="/machine-learning" className="text-muted-foreground hover:text-primary transition-colors">
                  Machine Learning
                </a>
              </li>
              <li>
                <a href="/web-apps" className="text-muted-foreground hover:text-primary transition-colors">
                  Web Applications
                </a>
              </li>
              <li>
                <a href="/ai-agents" className="text-muted-foreground hover:text-primary transition-colors">
                  AI Agents
                </a>
              </li>
            </ul>
          </div>

          {/* Contact & Social */}
          <div>
            <h3 className="font-semibold mb-4">Connect</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-9 h-9 p-0"
                  onClick={() => window.open('mailto:ryan.castillo@email.com', '_blank')}
                >
                  <Mail className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-9 h-9 p-0"
                  onClick={() => window.open('https://linkedin.com/in/ryancastillo', '_blank')}
                >
                  <Linkedin className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-9 h-9 p-0"
                  onClick={() => window.open('https://github.com/ryancastillo', '_blank')}
                >
                  <Github className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="text-sm text-muted-foreground">
                <p>Available for new opportunities</p>
                <p>Currently pursuing Masters in Analytics</p>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>© {currentYear} Ryan Castillo. All rights reserved.</p>
          <p className="mt-1">Built with React, Tailwind CSS, and modern web technologies.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

