import type { NextConfig } from 'next';

const nextConfig = (): NextConfig => {
  const isUnified = process.env.NEXT_OUTPUT === 'export' || process.env.UNIFIED_MODE === 'true';
  
  return {
    output: (process.env.NEXT_OUTPUT as 'standalone' | 'export') || undefined,
    trailingSlash: isUnified,
    
    // For unified mode, we need to handle API routes differently
    ...(isUnified && {
      basePath: '',
      assetPrefix: '',
      images: {
        unoptimized: true
      }
    }),
    
    async rewrites() {
      // In unified mode, API calls go to the same server
      if (isUnified) {
        return [];
      }
      
      return [
        {
          source: '/ingest/static/:path*',
          destination: 'https://eu-assets.i.posthog.com/static/:path*',
        },
        {
          source: '/ingest/:path*',
          destination: 'https://eu.i.posthog.com/:path*',
        },
        {
          source: '/ingest/flags',
          destination: 'https://eu.i.posthog.com/flags',
        },
      ];
    },
    skipTrailingSlashRedirect: true,
  };
};

export default nextConfig;
