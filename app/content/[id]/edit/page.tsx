import { DashboardLayout } from "@/components/dashboard/dashboard-layout"
import { ContentEditor } from "@/components/content/content-editor"

interface EditContentPageProps {
  params: {
    id: string
  }
}

export default function EditContentPage({ params }: EditContentPageProps) {
  return (
    <DashboardLayout>
      <ContentEditor contentId={params.id} />
    </DashboardLayout>
  )
}
