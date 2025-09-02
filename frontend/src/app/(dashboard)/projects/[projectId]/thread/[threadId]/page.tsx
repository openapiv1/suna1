'use client';

// Required for static export - generate empty params for client-side routing
export async function generateStaticParams(): Promise<{ projectId: string, threadId: string }[]> {
  return [];
}

import React from 'react';
import { ThreadComponent } from '@/components/thread/ThreadComponent';

export default function ThreadPage({
  params,
}: {
  params: Promise<{
    projectId: string;
    threadId: string;
  }>;
}) {
  const unwrappedParams = React.use(params);
  const { projectId, threadId } = unwrappedParams;

  return <ThreadComponent projectId={projectId} threadId={threadId} />;
}
