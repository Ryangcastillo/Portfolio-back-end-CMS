import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, ExternalLink, Github } from 'lucide-react'
import { Link } from 'react-router-dom'

const ProjectCard = ({ project, showFullDescription = false, className = "" }) => {
  return (
    <Card className={`group transition-all duration-300 hover:shadow-lg hover:-translate-y-1 ${className}`}>
      {project.thumbnail_url && (
        <div className="aspect-video w-full overflow-hidden rounded-t-lg">
          <img 
            src={project.thumbnail_url} 
            alt={project.title}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      )}
      
      <CardHeader>
        <div className="flex justify-between items-start">
          <CardTitle className="group-hover:text-primary transition-colors">
            {project.title}
          </CardTitle>
          {project.category && (
            <Badge variant="outline">{project.category.name || project.category}</Badge>
          )}
        </div>
        <CardDescription>
          {showFullDescription ? project.full_description : project.short_description || project.description}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {project.impact_metric && (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full" />
            <span className="text-sm font-medium text-green-600">{project.impact_metric || project.impact}</span>
          </div>
        )}

        {(project.technologies || project.tech) && (
          <div className="flex flex-wrap gap-2">
            {(project.technologies || project.tech)?.map((tech, index) => (
              <Badge key={index} variant="secondary" className="text-xs">
                {tech}
              </Badge>
            ))}
          </div>
        )}

        {project.business_problem && showFullDescription && (
          <div className="space-y-2">
            <h4 className="font-semibold text-sm">Business Problem</h4>
            <p className="text-sm text-muted-foreground">{project.business_problem}</p>
          </div>
        )}

        {project.solution_approach && showFullDescription && (
          <div className="space-y-2">
            <h4 className="font-semibold text-sm">Solution</h4>
            <p className="text-sm text-muted-foreground">{project.solution_approach}</p>
          </div>
        )}

        {project.results_achieved && showFullDescription && (
          <div className="space-y-2">
            <h4 className="font-semibold text-sm">Results</h4>
            <p className="text-sm text-muted-foreground">{project.results_achieved}</p>
          </div>
        )}

        <div className="flex gap-2 pt-2">
          {project.link && (
            <Button size="sm" asChild>
              <Link to={project.link}>
                <span>View Details</span>
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </Button>
          )}
          
          {project.demo_url && (
            <Button variant="outline" size="sm" asChild>
              <a href={project.demo_url} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="w-4 h-4 mr-2" />
                <span>Demo</span>
              </a>
            </Button>
          )}
          
          {project.github_url && (
            <Button variant="outline" size="sm" asChild>
              <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                <Github className="w-4 h-4 mr-2" />
                <span>Code</span>
              </a>
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

const ProjectsGrid = ({ projects = [], title = "Featured Projects", description, limit }) => {
  const displayProjects = limit ? projects.slice(0, limit) : projects

  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">{title}</h2>
          {description && (
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              {description}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {displayProjects.map((project) => (
            <ProjectCard 
              key={project.id} 
              project={project}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export { ProjectCard, ProjectsGrid }
export default ProjectsGrid