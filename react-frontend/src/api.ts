import axios from 'axios';

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
  tool_calls: string[];
}

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const res = await axios.post<ChatResponse>(
    '/api/chat',
    { message },
    { headers: { 'Content-Type': 'application/json' } }
  );
  return res.data;
} 