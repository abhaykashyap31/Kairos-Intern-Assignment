import React from 'react';
import styled from 'styled-components';
import PaperCard from './PaperCard';
import SummaryCard from './SummaryCard';

const ChatContainer = styled.div`
  margin-top: 12px;
`;

const UserMsg = styled.div`
  font-weight: 500;
  margin: 18px 0 6px 0;
  color: #333;
`;

const AssistantMsg = styled.div`
  background: #f0f2f6;
  padding: 18px 18px 12px 18px;
  border-radius: 8px;
  margin-bottom: 12px;
  color: #222;
`;

interface ChatHistoryItem {
  sender: 'user' | 'assistant';
  message: string;
}

interface ChatHistoryProps {
  history: ChatHistoryItem[];
}

function parsePapers(message: string) {
  // Detects if message is a paper search result (multiple papers, separated by ---)
  if (message.trim().startsWith('Title:') && message.includes('---')) {
    const papers = message.split('---').map(paper => {
      const lines = paper.split('\n').map(l => l.trim()).filter(Boolean);
      let title = '', authors = '', summary = '', link = '';
      for (const line of lines) {
        if (line.startsWith('Title:')) title = line.replace('Title:', '').trim();
        else if (line.startsWith('Authors:')) authors = line.replace('Authors:', '').trim();
        else if (line.startsWith('Summary:')) summary = line.replace('Summary:', '').trim();
        else if (line.startsWith('Link:')) link = line.replace('Link:', '').trim();
      }
      if (title || authors || summary || link) {
        return { title, authors, summary, link };
      }
      return null;
    }).filter(Boolean);
    return papers;
  }
  return null;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ history }) => (
  <ChatContainer>
    {history.map((item, idx) => {
      if (item.sender === 'user') {
        return <UserMsg key={idx}>You: {item.message}</UserMsg>;
      } else {
        // Try to parse as paper search result
        const papers = parsePapers(item.message);
        if (papers && papers.length > 0) {
          return papers.filter(Boolean).map((p, i) => (
            <PaperCard
              key={idx + '-' + i}
              title={p!.title || ''}
              authors={p!.authors || ''}
              summary={p!.summary || ''}
              link={p!.link || ''}
            />
          ));
        }
        // Otherwise, treat as summary or assistant message
        return <AssistantMsg key={idx}><SummaryCard summary={item.message} /></AssistantMsg>;
      }
    })}
  </ChatContainer>
);

export default ChatHistory; 