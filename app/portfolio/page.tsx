import { Metadata } from 'next'
import PortfolioManager from '@/components/portfolio/portfolio-manager'

export const metadata: Metadata = {
  title: 'Portfolio Management | Stitch CMS',
  description: 'Manage your portfolio content for the public website',
}

export default function PortfolioPage() {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <PortfolioManager />
    </div>
  )
}