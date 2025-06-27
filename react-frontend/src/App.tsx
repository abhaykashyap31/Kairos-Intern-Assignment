import React, { useState } from 'react';
import styled from 'styled-components';
import Sidebar from './components/Sidebar';
import ChatInput from './components/ChatInput';
import ChatHistory from './components/ChatHistory';
import { sendChatMessage } from './api';

const Layout = styled.div`
  display: flex;
  min-height: 100vh;
  background: #fafbfc;
`;

const Main = styled.div`
  flex: 1;
  padding: 0 0 0 0;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 2.1em;
  font-weight: 700;
  margin: 36px 0 8px 0;
  color: #2a2a2a;
`;

const Logo = styled.img`
  width: 44px;
  height: 44px;
`;

const Instructions = styled.div`
  margin: 8px 0 18px 0;
  color: #444;
  font-size: 1.08em;
  background: #f7f7fa;
  border-radius: 8px;
  padding: 18px 22px;
`;

function getLLMConfig() {
  // In a real app, fetch from backend or config endpoint
  // For demo, hardcode or use env
  return {
    provider: 'gemini',
    model: 'gemini-2.0-flash',
  };
}

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<{ sender: 'user' | 'assistant'; message: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const llmConfig = getLLMConfig();

  const handleSend = async () => {
    if (!input.trim()) return;
    setHistory(h => [...h, { sender: 'user', message: input }]);
    setLoading(true);
    try {
      const res = await sendChatMessage(input);
      setHistory(h => [...h, { sender: 'assistant', message: res.response }]);
    } catch (e) {
      setHistory(h => [...h, { sender: 'assistant', message: 'Error: Could not get response.' }]);
    }
    setInput('');
    setLoading(false);
  };

  return (
    <Layout>
      <Sidebar provider={llmConfig.provider} model={llmConfig.model} />
      <Main>
        <div style={{ maxWidth: 900, margin: '0 auto', padding: '0 0 0 0' }}>
          <Header>
            <Logo src="/logo.svg" alt="logo" />
            Scientific-Paper Scout
          </Header>
          <Instructions>
            <div>Type a command below:</div>
            <ul style={{ margin: '8px 0 0 0', paddingLeft: 24 }}>
              <li><b>search &lt;topic&gt;</b> to find recent papers</li>
              <li><b>summarize {'{pdf_url}'}</b> to summarize a paper</li>
            </ul>
          </Instructions>
          <ChatInput value={input} onChange={setInput} onSend={handleSend} disabled={loading} />
          <ChatHistory history={history} />
        </div>
      </Main>
    </Layout>
  );
};

export default App;
