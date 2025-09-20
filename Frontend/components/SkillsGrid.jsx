import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import * as LucideIcons from 'lucide-react'

const SkillCard = ({ skill, isHovered, onHover, onLeave }) => {
  // Dynamically get icon component from Lucide
  const IconComponent = skill.icon_name ? LucideIcons[skill.icon_name] : LucideIcons.Wrench

  return (
    <Card 
      className={`relative overflow-hidden transition-all duration-300 hover:shadow-lg cursor-pointer ${
        isHovered ? 'scale-105' : ''
      }`}
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${skill.color_gradient || 'from-blue-500 to-blue-600'} opacity-5`} />
      
      <CardHeader className="relative">
        <div className={`w-12 h-12 bg-gradient-to-br ${skill.color_gradient || 'from-blue-500 to-blue-600'} rounded-lg flex items-center justify-center mb-4`}>
          <IconComponent className="w-6 h-6 text-white" />
        </div>
        <CardTitle className="text-lg">{skill.title}</CardTitle>
        <CardDescription>{skill.description}</CardDescription>
      </CardHeader>

      <CardContent className="relative">
        <div className="flex justify-between items-center text-sm">
          <div>
            <div className="font-semibold text-primary">{skill.projects_count || skill.projects}</div>
            <div className="text-muted-foreground">Projects</div>
          </div>
          <div className="text-right">
            <div className="font-semibold text-green-600">{skill.impact_metric || skill.impact}</div>
            <div className="text-muted-foreground">Impact</div>
          </div>
        </div>

        {skill.category && (
          <div className="mt-4">
            <Badge variant="secondary">{skill.category}</Badge>
          </div>
        )}
        
        {isHovered && (
          <div className="mt-4 p-3 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg">
            <p className="text-sm font-medium">Ready to leverage this expertise!</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

const SkillsGrid = ({ skills = [], title = "Core Expertise", description }) => {
  const [hoveredSkill, setHoveredSkill] = useState(null)

  return (
    <section className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">{title}</h2>
          {description && (
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              {description}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {skills.map((skill) => (
            <SkillCard 
              key={skill.id}
              skill={skill}
              isHovered={hoveredSkill === skill.id}
              onHover={() => setHoveredSkill(skill.id)}
              onLeave={() => setHoveredSkill(null)}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export { SkillCard, SkillsGrid }
export default SkillsGrid