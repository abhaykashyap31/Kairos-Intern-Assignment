import React from 'react';
import styled from 'styled-components';

const Card = styled.div`
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(60,60,60,0.07);
  padding: 36px 32px;
  margin: 32px 0;
  color: #23272f;
  font-size: 1.13em;
  line-height: 1.8;
  max-width: 800px;
  border: 1px solid #e5e7eb;
  max-height: 500px;
  overflow-y: auto;
`;

const SectionTitle = styled.div`
  font-size: 1.18em;
  font-weight: 700;
  margin: 18px 0 8px 0;
  color: #1a237e;
`;

const Abstract = styled.div`
  background: #f7f8fa;
  border-left: 4px solid #6c63ff;
  padding: 14px 18px;
  margin: 16px 0 24px 0;
  font-style: italic;
  color: #444;
`;

const Authors = styled.div`
  font-size: 1em;
  color: #555;
  margin-bottom: 10px;
`;

function parseSummary(summary: string) {
  // Remove all asterisks from the summary
  const cleanSummary = summary.replace(/\*/g, '');

  // Try to extract title, authors, abstract, and sections from the cleaned summary string
  const titleMatch = cleanSummary.match(/^(.*?)\s*Authors:/);
  const authorsMatch = cleanSummary.match(/Authors:\s*([^\n]*)/);
  const abstractMatch = cleanSummary.match(/Abstract:\s*([\s\S]*?)(\d+\. |$)/);

  let title = titleMatch ? titleMatch[1].trim() : '';
  let authors = authorsMatch ? authorsMatch[1].trim() : '';
  let abstract = abstractMatch ? abstractMatch[1].trim() : '';

  // Remove extracted parts from the summary
  let rest = cleanSummary
    .replace(/^(.*?)Authors:/, '')
    .replace(/Authors:[^\n]*/, '')
    .replace(/Abstract:[\s\S]*?(\d+\. |$)/, '')
    .trim();

  // Split rest into sections by numbered headings (e.g., 1. INTRODUCTION)
  const sectionRegex = /(\d+\. [^\n]+)/g;
  let sections: { title: string, content: string }[] = [];
  let match;
  let lastIndex = 0;
  let sectionTitles: string[] = [];
  while ((match = sectionRegex.exec(rest)) !== null) {
    sectionTitles.push(match[1]);
  }
  if (sectionTitles.length > 0) {
    for (let i = 0; i < sectionTitles.length; i++) {
      const start = rest.indexOf(sectionTitles[i]) + sectionTitles[i].length;
      const end = i + 1 < sectionTitles.length ? rest.indexOf(sectionTitles[i + 1]) : rest.length;
      const content = rest.substring(start, end).trim();
      sections.push({ title: sectionTitles[i], content });
    }
  } else if (rest) {
    sections.push({ title: '', content: rest });
  }

  return { title, authors, abstract, sections };
}

interface SummaryCardProps {
  summary: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
  const { title, authors, abstract, sections } = parseSummary(summary);
  return (
    <Card>
      {title && <SectionTitle>{title}</SectionTitle>}
      {authors && <Authors><b>Authors:</b> {authors}</Authors>}
      {abstract && <Abstract>{abstract}</Abstract>}
      {sections.map((section, idx) => (
        <div key={idx}>
          {section.title && <SectionTitle>{section.title}</SectionTitle>}
          <div style={{ marginBottom: 18 }}>{section.content}</div>
        </div>
      ))}
    </Card>
  );
};

export default SummaryCard; 