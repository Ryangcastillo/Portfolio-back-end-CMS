import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Download, ArrowRight, BarChart3, Brain } from 'lucide-react'
import { Link } from 'react-router-dom'

const ProfileHero = ({ profile, stats = [] }) => {
  return (
    <section className="relative py-20 lg:py-32 bg-gradient-to-br from-background via-background to-muted/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <Badge variant="secondary" className="w-fit">
                {profile?.availability_status || "Available for New Opportunities"}
              </Badge>
              <h1 className="text-4xl lg:text-6xl font-bold tracking-tight">
                {profile?.title || "Data Analyst"} &{' '}
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Process Improvement
                </span>{' '}
                Specialist
              </h1>
              <p className="text-xl text-muted-foreground max-w-2xl">
                {profile?.bio_description || 
                  "Transforming business challenges into actionable insights through advanced analytics and AI innovation. 8+ years of experience delivering measurable business value through data-driven solutions."
                }
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" className="flex items-center space-x-2" asChild>
                <Link to="/data-analysis">
                  <span>View My Work</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                className="flex items-center space-x-2"
                onClick={() => window.open(profile?.resume_url || '/resume.pdf', '_blank')}
              >
                <Download className="w-4 h-4" />
                <span>Download Resume</span>
              </Button>
            </div>

            {/* Quick Stats */}
            {stats.length > 0 && (
              <div className={`grid grid-cols-${Math.min(stats.length, 3)} gap-6 pt-8 border-t border-border`}>
                {stats.slice(0, 3).map((stat) => (
                  <div key={stat.id} className="text-center">
                    <div className="text-2xl font-bold text-primary">{stat.metric_value}</div>
                    <div className="text-sm text-muted-foreground">{stat.metric_name}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Profile Image Placeholder */}
          <div className="flex justify-center lg:justify-end">
            <div className="relative">
              <div className="w-80 h-80 bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20 rounded-2xl flex items-center justify-center border border-border">
                <div className="text-center space-y-4">
                  <div className="w-24 h-24 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto">
                    <span className="text-white font-bold text-2xl">
                      {profile?.full_name ? 
                        profile.full_name.split(' ').map(n => n[0]).join('') : 
                        'RC'
                      }
                    </span>
                  </div>
                  <div>
                    <p className="font-semibold text-lg">{profile?.full_name || "Ryan Castillo"}</p>
                    <p className="text-muted-foreground">{profile?.location || "Auckland, New Zealand"}</p>
                  </div>
                </div>
              </div>
              
              {/* Floating elements */}
              <div className="absolute -top-4 -right-4 w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center animate-bounce">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div className="absolute -bottom-4 -left-4 w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center animate-bounce" style={{ animationDelay: '0.5s' }}>
                <Brain className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default ProfileHero