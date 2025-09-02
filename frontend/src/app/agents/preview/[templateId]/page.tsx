import { redirect } from 'next/navigation';

// Required for static export - generate empty params since this just redirects
export async function generateStaticParams(): Promise<{ templateId: string }[]> {
  return [];
}

export default function AgentPreviewPage() {
  redirect('/dashboard');
}