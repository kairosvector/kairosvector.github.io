import type { APIRoute } from 'astro';
import locationsData from '../../../data/locations.json';

export const GET: APIRoute = async () => {
  const issues = locationsData.weeklyFeatured;
  const currentProductId = (locationsData as any).currentProductIssueId || 'issue-05';
  const productIssue = issues.find(x => x.id === currentProductId) || issues[1] || issues[0];

  const rawNum = productIssue?.issue ? productIssue.issue.replace(/[^0-9]/g, '') : '05';
  const issueNum = parseInt(rawNum, 10) || 5;
  const startDate = productIssue?.date ? productIssue.date.split('~')[0].trim() : '2026-09-26';
  const issueFormatted = productIssue?.issue || ('第 ' + String(issueNum).padStart(2, '0') + ' 期');

  const body = {
    schemaVersion: 1,
    status: 'product',
    issue: issueNum,
    issueFormatted: issueFormatted,
    title: productIssue?.theme || '',
    publishedAt: startDate,
    dateRange: productIssue?.date || '',
    category: productIssue?.categoryName || '',
    spotsCount: productIssue?.spots?.length || 0,
    url: 'https://kairosvector.pages.dev/geosim/weekly-featured/latest?embed=true',
    backupUrl: 'https://kairosvector.github.io/geosim/weekly-featured/latest?embed=true'
  };

  return new Response(JSON.stringify(body, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=1800'
    }
  });
};
