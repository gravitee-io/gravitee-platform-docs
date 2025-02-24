const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');

// Retrieve environment variables
const org = process.env.ORG_NAME;
const token = process.env.GITHUB_TOKEN;
const docsPath = process.env.DOCS_PATH;

if (!org || !token || !docsPath) {
  console.error("Missing required environment variables.");
  process.exit(1);
}

const headers = {
  'Accept': 'application/vnd.github.v3+json',
  'Authorization': `token ${token}`
};

// List repos in the organization, handling pagination
async function listRepos() {
  let repos = [];
  let page = 1;
  while (true) {
    const url = `https://api.github.com/orgs/${org}/repos?per_page=100&page=${page}`;
    const res = await fetch(url, { headers });
    if (res.status !== 200) {
      console.error(`Failed to fetch repos: ${res.status} ${res.statusText}`);
      process.exit(1);
    }
    const data = await res.json();
    if (!Array.isArray(data)) break;
    repos = repos.concat(data);
    if (data.length < 100) break;
    page++;
  }
  return repos;
}

// Fetch the README file for a repository
async function fetchReadme(repoName) {
  const url = `https://api.github.com/repos/${org}/${repoName}/readme`;
  const res = await fetch(url, { headers });
  if (res.status === 404) {
    console.warn(`README not found for repo: ${repoName}`);
    return null;
  }
  if (res.status !== 200) {
    console.error(`Error fetching README for ${repoName}: ${res.statusText}`);
    return null;
  }
  const data = await res.json();
  if (!data.content) return null;
  // Decode the base64 content
  const buff = Buffer.from(data.content, 'base64');
  return buff.toString('utf-8');
}

// Extract the first Markdown header as the title, fallback to repoName if not found
function extractTitle(content, repoName) {
  const lines = content.split('\n');
  for (const line of lines) {
    const match = line.match(/^#\s+(.*)/);
    if (match) {
      return match[1].trim();
    }
  }
  // Fallback to the repo name if no header found
  return repoName;
}

// Sanitize title to create a valid filename (replace spaces with underscores, remove special characters)
function sanitizeFilename(title) {
  return title
    .replace(/[^a-z0-9 \-_]/gi, '')  // remove unwanted characters
    .replace(/\s+/g, ' ')            // collapse whitespace
    .trim()
    .replace(/ /g, '_') + '.md';     // replace spaces with underscores and add .md extension
}

async function main() {
  try {
    const repos = await listRepos();
    // Filter for repos with "policy" in the name (case-insensitive)
    const policyRepos = repos.filter(repo => repo.name.toLowerCase().includes("policy"));
    console.log(`Found ${policyRepos.length} policy repos.`);
    for (const repo of policyRepos) {
      console.log(`Processing repo: ${repo.name}`);
      const readme = await fetchReadme(repo.name);
      if (!readme) {
        console.warn(`Skipping repo "${repo.name}" due to missing README.`);
        continue;
      }
      // Use the repo name as fallback if no markdown header is found.
      const title = extractTitle(readme, repo.name);
      const filename = sanitizeFilename(title);
      const filepath = path.join(docsPath, filename);
      // Write or update the file with the README content
      fs.writeFileSync(filepath, readme, 'utf8');
      console.log(`Updated file: ${filepath}`);
    }
  } catch (error) {
    console.error("Error during sync:", error);
    process.exit(1);
  }
}

main();