import React from 'react';
import styled from 'styled-components';

const InputRow = styled.form`
  display: flex;
  gap: 12px;
  margin: 24px 0 8px 0;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1em;
  background: #f8f8fa;
`;

const Button = styled.button`
  background: #f66;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0 24px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  &:hover {
    background: #d44;
  }
`;

interface ChatInputProps {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ value, onChange, onSend, disabled }) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!disabled && value.trim()) onSend();
  };
  return (
    <InputRow onSubmit={handleSubmit}>
      <Input
        type="text"
        placeholder="Type a command below..."
        value={value}
        onChange={e => onChange(e.target.value)}
        disabled={disabled}
      />
      <Button type="submit" disabled={disabled || !value.trim()}>Send</Button>
    </InputRow>
  );
};

export default ChatInput; 