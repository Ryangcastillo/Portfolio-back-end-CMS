import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { MessageCircle, X, Send, Bot, User } from 'lucide-react'

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hi! I'm Ryan's AI assistant. I can answer questions about his experience, skills, projects, or availability. What would you like to know?",
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Predefined responses based on common questions
  const getResponse = (message) => {
    const lowerMessage = message.toLowerCase()
    
    if (lowerMessage.includes('experience') || lowerMessage.includes('background')) {
      return "Ryan has 8+ years of experience in data analysis and process improvement. He's worked at major companies like Spark New Zealand and Auckland Transport, specializing in Power BI, SQL, SAP systems, and procurement analytics. He's currently pursuing a Masters in Analytics at AUT."
    }
    
    if (lowerMessage.includes('skills') || lowerMessage.includes('technical')) {
      return "Ryan's technical skills include: Power BI, SQL, Python, SAP FICO, Dynamics 365, PowerApps, ServiceNow, SharePoint, Azure DevOps, and Advanced Excel. He's also developing expertise in machine learning and AI agent development."
    }
    
    if (lowerMessage.includes('projects') || lowerMessage.includes('work')) {
      return "Ryan has worked on various impactful projects including supplier performance analytics dashboards, procurement spend forecasting, vendor master data optimization, and AI-powered process automation. Each project delivered measurable business value and cost savings."
    }
    
    if (lowerMessage.includes('available') || lowerMessage.includes('hire') || lowerMessage.includes('job')) {
      return "Yes, Ryan is actively seeking new opportunities in data analysis, business intelligence, or related fields. He's particularly interested in roles that combine his analytical skills with business process improvement expertise."
    }
    
    if (lowerMessage.includes('education') || lowerMessage.includes('degree')) {
      return "Ryan holds a Bachelor's in Industrial Engineering and a PGDip in Business Administration. He's currently pursuing a Masters in Analytics at Auckland University of Technology and holds several professional certifications including Microsoft Power BI Data Analyst (PL-300)."
    }
    
    if (lowerMessage.includes('location') || lowerMessage.includes('where')) {
      return "Ryan is based in Auckland, New Zealand, and is open to both local and remote opportunities."
    }
    
    if (lowerMessage.includes('contact') || lowerMessage.includes('reach')) {
      return "You can reach Ryan through the contact form on this website, connect with him on LinkedIn, or download his resume for direct contact information. He typically responds within 24 hours."
    }
    
    if (lowerMessage.includes('ai') || lowerMessage.includes('machine learning')) {
      return "Ryan is developing expertise in AI and machine learning applications, including predictive analytics, anomaly detection, and AI agent development. He's particularly interested in applying these technologies to business process optimization and cost reduction."
    }
    
    // Default response
    return "That's a great question! For detailed information about Ryan's background and experience, I'd recommend exploring the different sections of this portfolio or downloading his resume. Is there something specific about his data analysis or process improvement experience you'd like to know more about?"
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsTyping(true)

    // Simulate typing delay
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        type: 'bot',
        content: getResponse(inputValue),
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, botResponse])
      setIsTyping(false)
    }, 1000 + Math.random() * 1000) // Random delay between 1-2 seconds
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <>
      {/* Chat Toggle Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg transition-all duration-300 z-50 ${
          isOpen ? 'bg-destructive hover:bg-destructive/90' : 'bg-primary hover:bg-primary/90'
        }`}
      >
        {isOpen ? (
          <X className="w-6 h-6" />
        ) : (
          <MessageCircle className="w-6 h-6" />
        )}
      </Button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-80 h-96 bg-card border border-border rounded-lg shadow-xl z-40 flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-sm">Ryan's AI Assistant</h3>
                <p className="text-xs text-muted-foreground">Ask me anything!</p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg text-sm ${
                    message.type === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-muted-foreground'
                  }`}
                >
                  <div className="flex items-start space-x-2">
                    {message.type === 'bot' && (
                      <Bot className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    )}
                    {message.type === 'user' && (
                      <User className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    )}
                    <p className="leading-relaxed">{message.content}</p>
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-muted text-muted-foreground p-3 rounded-lg text-sm max-w-[80%]">
                  <div className="flex items-center space-x-2">
                    <Bot className="w-4 h-4" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-border">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about Ryan's experience..."
                className="flex-1 px-3 py-2 text-sm bg-background border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
              />
              <Button
                onClick={handleSendMessage}
                size="sm"
                className="px-3"
                disabled={!inputValue.trim() || isTyping}
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default ChatBot

