import type { APIRoute } from 'astro';
import locationsData from '../../../data/locations.json';

export const GET: APIRoute = async () => {
  const latestIssue = locationsData.weeklyFeatured[0];
  const rawNum = latestIssue?.issue ? latestIssue.issue.replace(/[^0-9]/g, '') : '06';
  const issueNum = parseInt(rawNum, 10) || 6;
  const startDate = latestIssue?.date ? latestIssue.date.split('~')[0].trim() : '2026-10-03';
  const issueFormatted = latestIssue?.issue || ('第 ' + String(issueNum).padStart(2, '0') + ' 期');

  const body = {
    schemaVersion: 1,
    issue: issueNum,
    issueFormatted: issueFormatted,
    title: latestIssue?.theme || '',
    publishedAt: startDate,
    dateRange: latestIssue?.date || '',
    category: latestIssue?.categoryName || '',
    spotsCount: latestIssue?.spots?.length || 0,
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
