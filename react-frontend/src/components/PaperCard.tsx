import React from 'react';
import styled from 'styled-components';

const Card = styled.div`
  background: #fff;
  border: 1px solid #e0e0e0;
  padding: 20px 24px;
  margin-bottom: 18px;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.01);
`;

const Title = styled.div`
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 4px;
`;

const Authors = styled.div`
  color: #555;
  margin-bottom: 4px;
  font-size: 0.98em;
`;

const Summary = styled.div`
  margin-bottom: 8px;
  color: #222;
`;

const Link = styled.a`
  color: #2a6ae6;
  text-decoration: underline;
  font-size: 0.97em;
`;

interface PaperCardProps {
  title: string;
  authors: string;
  summary: string;
  link: string;
}

const PaperCard: React.FC<PaperCardProps> = ({ title, authors, summary, link }) => (
  <Card>
    <Title>{title}</Title>
    <Authors><b>Authors:</b> {authors}</Authors>
    <Summary>{summary}</Summary>
    <Link href={link} target="_blank" rel="noopener noreferrer">Read on arXiv</Link>
  </Card>
);

export default PaperCard; 