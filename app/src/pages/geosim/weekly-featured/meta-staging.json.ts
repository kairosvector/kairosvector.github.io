import type { APIRoute } from 'astro';
import locationsData from '../../../data/locations.json';

export const GET: APIRoute = async () => {
  const issues = locationsData.weeklyFeatured;
  const currentStagingId = (locationsData as any).currentStagingIssueId || 'issue-06';
  const stagingIssue = issues.find((x) => x.id === currentStagingId) || issues[0];

  const rawNum = stagingIssue?.issue ? stagingIssue.issue.replace(/[^0-9]/g, '') : '06';
  const issueNum = parseInt(rawNum, 10) || 6;
  const startDate = stagingIssue?.date ? stagingIssue.date.split('~')[0].trim() : '2026-10-03';
  const issueFormatted = stagingIssue?.issue || ('第 ' + String(issueNum).padStart(2, '0') + ' 期');

  const body = {
    schemaVersion: 1,
    status: 'staging',
    issue: issueNum,
    issueFormatted: issueFormatted,
    title: stagingIssue?.theme || '',
    publishedAt: startDate,
    dateRange: stagingIssue?.date || '',
    category: stagingIssue?.categoryName || '',
    spotsCount: stagingIssue?.spots?.length || 0,
    url: 'https://kairosvector.pages.dev/geosim/weekly-featured/staging?embed=true',
    backupUrl: 'https://kairosvector.github.io/geosim/weekly-featured/staging?embed=true'
  };

  return new Response(JSON.stringify(body, null, 2), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    }
  });
};
