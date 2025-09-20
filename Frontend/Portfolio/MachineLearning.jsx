import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Brain, 
  TrendingUp, 
  AlertTriangle, 
  DollarSign, 
  Target,
  Code,
  BarChart3,
  Zap,
  CheckCircle,
  ExternalLink,
  Cpu,
  Activity
} from 'lucide-react'

const MachineLearning = () => {
  const [selectedProject, setSelectedProject] = useState(null)

  const projects = [
    {
      id: 1,
      title: "Equipment Failure Prediction Model",
      category: "Predictive Analytics",
      description: "Machine learning model predicting equipment failures 2 weeks in advance using sensor data and maintenance history, enabling proactive maintenance scheduling.",
      businessProblem: "Unexpected equipment failures were causing costly downtime, with average repair costs of $15K per incident and 24-48 hour service disruptions affecting operations.",
      mlApproach: "Implemented Random Forest ensemble model using 18 months of sensor data (temperature, vibration, pressure) combined with maintenance logs and failure history.",
      technicalDetails: {
        dataSize: "50,000+ sensor readings",
        features: "24 engineered features",
        algorithm: "Random Forest with hyperparameter tuning",
        validation: "Time-series cross-validation",
        deployment: "Real-time scoring pipeline"
      },
      results: {
        accuracy: 85,
        precision: 82,
        recall: 88,
        f1Score: 85
      },
      businessImpact: {
        primary: "$300K annual savings",
        metrics: [
          "85% accuracy in failure prediction",
          "2-week advance warning",
          "60% reduction in emergency repairs",
          "40% improvement in maintenance efficiency"
        ]
      },
      technologies: ["Python", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Azure ML"],
      status: "Production",
      year: "2023",
      complexity: "High"
    },
    {
      id: 2,
      title: "Demand Forecasting for Procurement",
      category: "Time Series Forecasting",
      description: "Advanced time series forecasting model for procurement demand planning using historical data, seasonal patterns, and external market indicators.",
      businessProblem: "Inaccurate demand forecasting led to $200K in excess inventory and frequent stockouts affecting operational efficiency and customer satisfaction.",
      mlApproach: "Developed ensemble model combining ARIMA, Prophet, and LSTM networks to capture multiple seasonal patterns and trend changes in procurement demand.",
      technicalDetails: {
        dataSize: "3 years historical data",
        features: "Seasonal, trend, and external factors",
        algorithm: "Ensemble (ARIMA + Prophet + LSTM)",
        validation: "Rolling window validation",
        deployment: "Automated monthly forecasts"
      },
      results: {
        accuracy: 78,
        mape: 15.2,
        improvement: 30,
        reliability: 92
      },
      businessImpact: {
        primary: "30% forecast improvement",
        metrics: [
          "20% reduction in inventory costs",
          "15% decrease in stockout incidents",
          "Improved supplier planning",
          "Better budget allocation"
        ]
      },
      technologies: ["Python", "Prophet", "TensorFlow", "Statsmodels", "Plotly", "Power BI"],
      status: "Production",
      year: "2023",
      complexity: "Medium"
    },
    {
      id: 3,
      title: "Expense Anomaly Detection System",
      category: "Anomaly Detection",
      description: "Intelligent system for detecting fraudulent or erroneous expense claims using unsupervised learning and statistical analysis.",
      businessProblem: "Manual expense review process was missing 15% of fraudulent claims and taking 40+ hours weekly, resulting in financial losses and compliance risks.",
      mlApproach: "Implemented Isolation Forest algorithm combined with statistical outlier detection to identify suspicious patterns in expense submissions.",
      technicalDetails: {
        dataSize: "100,000+ expense records",
        features: "Amount, category, timing, patterns",
        algorithm: "Isolation Forest + Statistical tests",
        validation: "Expert validation on flagged cases",
        deployment: "Real-time scoring API"
      },
      results: {
        accuracy: 95,
        precision: 88,
        recall: 92,
        falsePositiveRate: 5
      },
      businessImpact: {
        primary: "$50K fraud prevention",
        metrics: [
          "95% accuracy in anomaly detection",
          "80% reduction in review time",
          "Prevented fraudulent claims",
          "Improved compliance scores"
        ]
      },
      technologies: ["Python", "Scikit-learn", "Pandas", "FastAPI", "Docker", "Azure"],
      status: "Production",
      year: "2022",
      complexity: "Medium"
    },
    {
      id: 4,
      title: "Customer Churn Prediction Model",
      category: "Classification",
      description: "Predictive model identifying customers at risk of churning, enabling proactive retention strategies and targeted interventions.",
      businessProblem: "High customer acquisition costs ($500 per customer) made retention critical, but lack of early warning system resulted in 25% annual churn rate.",
      mlApproach: "Developed gradient boosting model using customer behavior data, transaction history, and engagement metrics to predict churn probability.",
      technicalDetails: {
        dataSize: "50,000 customer records",
        features: "Behavioral and transactional features",
        algorithm: "XGBoost with feature selection",
        validation: "Stratified cross-validation",
        deployment: "Monthly batch scoring"
      },
      results: {
        accuracy: 78,
        precision: 75,
        recall: 82,
        auc: 84
      },
      businessImpact: {
        primary: "15% retention improvement",
        metrics: [
          "78% accuracy in churn prediction",
          "Early identification of at-risk customers",
          "Targeted retention campaigns",
          "$150K revenue protection"
        ]
      },
      technologies: ["Python", "XGBoost", "Pandas", "Seaborn", "Jupyter", "MLflow"],
      status: "Pilot",
      year: "2024",
      complexity: "Medium"
    },
    {
      id: 5,
      title: "Supply Chain Risk Assessment",
      category: "Risk Modeling",
      description: "Multi-factor risk assessment model evaluating supplier reliability, market conditions, and operational factors to optimize supply chain decisions.",
      businessProblem: "Supply chain disruptions were causing 10% of projects to experience delays, with limited visibility into risk factors and mitigation strategies.",
      mlApproach: "Built ensemble model combining logistic regression and decision trees to assess multiple risk dimensions and provide actionable risk scores.",
      technicalDetails: {
        dataSize: "5,000 supplier assessments",
        features: "Financial, operational, market factors",
        algorithm: "Ensemble (Logistic + Decision Tree)",
        validation: "Historical validation",
        deployment: "Quarterly risk updates"
      },
      results: {
        accuracy: 82,
        precision: 79,
        recall: 85,
        riskReduction: 25
      },
      businessImpact: {
        primary: "25% risk reduction",
        metrics: [
          "Early warning system",
          "Improved supplier selection",
          "Reduced project delays",
          "Better contingency planning"
        ]
      },
      technologies: ["Python", "Scikit-learn", "Pandas", "Plotly", "Streamlit"],
      status: "Development",
      year: "2024",
      complexity: "High"
    }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'Production': return 'bg-green-500'
      case 'Pilot': return 'bg-yellow-500'
      case 'Development': return 'bg-blue-500'
      default: return 'bg-gray-500'
    }
  }

  const getComplexityColor = (complexity) => {
    switch (complexity) {
      case 'High': return 'text-red-500'
      case 'Medium': return 'text-yellow-500'
      case 'Low': return 'text-green-500'
      default: return 'text-gray-500'
    }
  }

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Predictive Analytics': return TrendingUp
      case 'Time Series Forecasting': return BarChart3
      case 'Anomaly Detection': return AlertTriangle
      case 'Classification': return Target
      case 'Risk Modeling': return Cpu
      default: return Brain
    }
  }

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl lg:text-5xl font-bold mb-6">
            Machine Learning & Predictive Analytics
          </h1>
          <p className="text-xl text-muted-foreground max-w-4xl mx-auto mb-8">
            Applying advanced machine learning techniques to solve real business problems, 
            from predictive maintenance and demand forecasting to anomaly detection and risk assessment. 
            Each model delivers measurable business value through data-driven insights.
          </p>
          
          {/* ML Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">85%</div>
              <div className="text-sm text-muted-foreground">Avg Model Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">5</div>
              <div className="text-sm text-muted-foreground">ML Models</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">$500K+</div>
              <div className="text-sm text-muted-foreground">Business Value</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">3</div>
              <div className="text-sm text-muted-foreground">In Production</div>
            </div>
          </div>
        </div>

        {/* Projects Grid */}
        <div className="space-y-8">
          {projects.map((project) => {
            const IconComponent = getCategoryIcon(project.category)
            const isExpanded = selectedProject === project.id
            
            return (
              <Card key={project.id} className="overflow-hidden">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                        <IconComponent className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2 mb-1">
                          <Badge variant="secondary">{project.category}</Badge>
                          <div className={`w-2 h-2 rounded-full ${getStatusColor(project.status)}`} />
                          <span className="text-xs text-muted-foreground">{project.status}</span>
                        </div>
                        <CardTitle className="text-xl">{project.title}</CardTitle>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="text-sm text-muted-foreground mb-1">{project.year}</div>
                      <div className={`text-xs font-medium ${getComplexityColor(project.complexity)}`}>
                        {project.complexity} Complexity
                      </div>
                    </div>
                  </div>
                  
                  <CardDescription className="text-sm leading-relaxed mt-3">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-6">
                  {/* Key Metrics */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-lg">
                    {project.results.accuracy && (
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{project.results.accuracy}%</div>
                        <div className="text-xs text-muted-foreground">Accuracy</div>
                      </div>
                    )}
                    {project.results.precision && (
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{project.results.precision}%</div>
                        <div className="text-xs text-muted-foreground">Precision</div>
                      </div>
                    )}
                    {project.results.recall && (
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">{project.results.recall}%</div>
                        <div className="text-xs text-muted-foreground">Recall</div>
                      </div>
                    )}
                    {project.results.improvement && (
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">+{project.results.improvement}%</div>
                        <div className="text-xs text-muted-foreground">Improvement</div>
                      </div>
                    )}
                  </div>

                  {/* Business Impact */}
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <Target className="w-4 h-4 text-green-500" />
                      <span className="font-medium text-green-600 dark:text-green-400">
                        {project.businessImpact.primary}
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {project.businessImpact.metrics.map((metric, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm">
                          <CheckCircle className="w-3 h-3 text-green-500" />
                          <span className="text-muted-foreground">{metric}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Technologies */}
                  <div>
                    <h4 className="font-medium text-sm mb-3">Technologies & Tools</h4>
                    <div className="flex flex-wrap gap-2">
                      {project.technologies.map((tech) => (
                        <Badge key={tech} variant="outline" className="text-xs">
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Expand/Collapse Button */}
                  <Button
                    variant="ghost"
                    className="w-full"
                    onClick={() => setSelectedProject(isExpanded ? null : project.id)}
                  >
                    {isExpanded ? 'Show Less' : 'View Technical Details'}
                    <Code className="w-4 h-4 ml-2" />
                  </Button>

                  {/* Expanded Technical Details */}
                  {isExpanded && (
                    <div className="space-y-6 pt-6 border-t border-border">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Business Problem */}
                        <div>
                          <h4 className="font-medium mb-3 flex items-center">
                            <AlertTriangle className="w-4 h-4 mr-2 text-orange-500" />
                            Business Challenge
                          </h4>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {project.businessProblem}
                          </p>
                        </div>

                        {/* ML Approach */}
                        <div>
                          <h4 className="font-medium mb-3 flex items-center">
                            <Brain className="w-4 h-4 mr-2 text-blue-500" />
                            ML Approach
                          </h4>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {project.mlApproach}
                          </p>
                        </div>
                      </div>

                      {/* Technical Specifications */}
                      <div>
                        <h4 className="font-medium mb-3 flex items-center">
                          <Cpu className="w-4 h-4 mr-2 text-purple-500" />
                          Technical Specifications
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {Object.entries(project.technicalDetails).map(([key, value]) => (
                            <div key={key} className="p-3 bg-muted/30 rounded-lg">
                              <div className="text-xs text-muted-foreground mb-1">
                                {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                              </div>
                              <div className="text-sm font-medium">{value}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* ML Methodology Section */}
        <section className="mt-20 py-16 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20 rounded-2xl">
          <div className="max-w-5xl mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold mb-4">ML Development Methodology</h2>
              <p className="text-muted-foreground">
                Rigorous approach ensuring reliable, production-ready machine learning solutions
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BarChart3 className="w-8 h-8 text-blue-500" />
                </div>
                <h3 className="font-semibold mb-3">Data Engineering</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Data collection & cleaning</div>
                  <div>Feature engineering</div>
                  <div>Pipeline automation</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Brain className="w-8 h-8 text-purple-500" />
                </div>
                <h3 className="font-semibold mb-3">Model Development</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Algorithm selection</div>
                  <div>Hyperparameter tuning</div>
                  <div>Cross-validation</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Activity className="w-8 h-8 text-green-500" />
                </div>
                <h3 className="font-semibold mb-3">Production & Monitoring</h3>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div>Model deployment</div>
                  <div>Performance monitoring</div>
                  <div>Continuous improvement</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default MachineLearning

