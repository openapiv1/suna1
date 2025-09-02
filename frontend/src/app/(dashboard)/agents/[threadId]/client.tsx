'use client';

// Required for static export - generate empty params for client-side routing
export async function generateStaticParams(): Promise<{ threadId: string }[]> {
  return [];
}
import React from 'react';
import {
  ThreadParams,
} from '@/components/thread/types';
import { RedirectPage } from './redirect-page';

export default function ThreadPage({
  params,
}: {
  params: Promise<ThreadParams>;
}) {
  const unwrappedParams = React.use(params);
  return <RedirectPage threadId={unwrappedParams.threadId} />;
}