"use client"

import React, { Component, ReactNode, ErrorInfo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AlertTriangle, RefreshCw, Home, Bug, Copy, Check } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

interface Props {
  children: ReactNode
  fallback?: ReactNode
  onError?: (error: Error, errorInfo: ErrorInfo) => void
}

interface State {
  hasError: boolean
  error?: Error
  errorInfo?: ErrorInfo
  errorId?: string
  copied: boolean
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, copied: false }
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console for development
    console.error('ErrorBoundary caught an error:', error, errorInfo)
    
    // Generate error ID for tracking
    const errorId = `frontend-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    this.setState({ error, errorInfo, errorId })
    
    // Report error to backend error management system
    this.reportError(error, errorInfo, errorId)
    
    // Call optional error callback
    if (this.props.onError) {
      this.props.onError(error, errorInfo)
    }
  }

  private async reportError(error: Error, errorInfo: ErrorInfo, errorId: string) {
    try {
      const errorReport = {
        errorId,
        message: error.message,
        name: error.name,
        stack: error.stack,
        componentStack: errorInfo.componentStack,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent,
        context: {
          react_error: true,
          component_stack: errorInfo.componentStack,
          error_boundary: true
        }
      }

      // Send to backend error management API
      await fetch('/api/errors/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(errorReport),
      })
    } catch (reportingError) {
      console.error('Failed to report error to backend:', reportingError)
    }
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined, errorId: undefined, copied: false })
  }

  private copyErrorDetails = async () => {
    const { error, errorInfo, errorId } = this.state
    
    const errorDetails = `
Error ID: ${errorId}
Error: ${error?.name}: ${error?.message}
Stack: ${error?.stack}
Component Stack: ${errorInfo?.componentStack}
Timestamp: ${new Date().toISOString()}
URL: ${window.location.href}
User Agent: ${navigator.userAgent}
    `.trim()
    
    try {
      await navigator.clipboard.writeText(errorDetails)
      this.setState({ copied: true })
      setTimeout(() => this.setState({ copied: false }), 2000)
    } catch (err) {
      console.error('Failed to copy error details:', err)
    }
  }

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback
      }

      // Default error UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4">
          <Card className="w-full max-w-lg mx-auto">
            <CardHeader className="text-center">
              <div className="flex justify-center mb-4">
                <div className="relative">
                  <AlertTriangle className="h-16 w-16 text-destructive" />
                  <Bug className="h-6 w-6 text-destructive-foreground absolute -bottom-1 -right-1 bg-destructive rounded-full p-1" />
                </div>
              </div>
              <CardTitle className="text-xl">Something went wrong!</CardTitle>
              <CardDescription>
                An unexpected error occurred in the application. The error has been reported to our team.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {this.state.errorId && (
                <div className="bg-muted p-3 rounded-md">
                  <p className="text-sm font-medium text-muted-foreground mb-2">Error Reference</p>
                  <div className="flex items-center justify-between">
                    <code className="text-xs bg-background px-2 py-1 rounded border">
                      {this.state.errorId}
                    </code>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={this.copyErrorDetails}
                      className="h-8 w-8 p-0"
                    >
                      {this.state.copied ? (
                        <Check className="h-4 w-4 text-green-600" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
              )}
              
              <div className="flex flex-col gap-2">
                <Button onClick={this.handleReset} className="w-full">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Try Again
                </Button>
                <Link href="/" className="w-full">
                  <Button variant="outline" className="w-full bg-transparent">
                    <Home className="h-4 w-4 mr-2" />
                    Go Home
                  </Button>
                </Link>
              </div>
              
              {process.env.NODE_ENV === 'development' && this.state.error && (
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm font-medium text-muted-foreground mb-2">
                    Debug Information
                  </summary>
                  <div className="bg-muted p-3 rounded-md mt-2">
                    <pre className="text-xs overflow-x-auto whitespace-pre-wrap">
                      <strong>Error:</strong> {this.state.error.message}
                      {'\n\n'}
                      <strong>Stack:</strong>
                      {'\n'}{this.state.error.stack}
                      {this.state.errorInfo?.componentStack && (
                        <>
                          {'\n\n'}
                          <strong>Component Stack:</strong>
                          {'\n'}{this.state.errorInfo.componentStack}
                        </>
                      )}
                    </pre>
                  </div>
                </details>
              )}
            </CardContent>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}

// Hook for functional components to report errors manually
export const useErrorReporting = () => {
  const reportError = async (
    error: Error,
    context?: Record<string, any>,
    severity: 'low' | 'medium' | 'high' | 'critical' = 'medium'
  ) => {
    const errorId = `manual-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    try {
      const errorReport = {
        errorId,
        message: error.message,
        name: error.name,
        stack: error.stack,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent,
        severity,
        context: {
          ...context,
          manual_report: true,
        }
      }

      await fetch('/api/errors/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(errorReport),
      })
      
      return errorId
    } catch (reportingError) {
      console.error('Failed to report error:', reportingError)
      throw reportingError
    }
  }

  return { reportError }
}

export default ErrorBoundary