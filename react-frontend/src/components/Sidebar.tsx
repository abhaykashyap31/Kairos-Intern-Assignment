import React from 'react';
import styled from 'styled-components';

const SidebarContainer = styled.div`
  width: 260px;
  background: #f7f7fa;
  padding: 32px 24px;
  min-height: 100vh;
  box-sizing: border-box;
  border-right: 1px solid #ececec;
`;

const Title = styled.div`
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 32px;
`;

const Label = styled.div`
  color: #888;
  font-size: 0.95em;
`;

const Value = styled.div`
  font-weight: 500;
  margin-bottom: 16px;
`;

interface SidebarProps {
  provider: string;
  model: string;
}

const Sidebar: React.FC<SidebarProps> = ({ provider, model }) => (
  <SidebarContainer>
    <Title>LLM Configuration</Title>
    <Label>Provider:</Label>
    <Value>{provider}</Value>
    <Label>Model:</Label>
    <Value>{model}</Value>
  </SidebarContainer>
);

export default Sidebar; 