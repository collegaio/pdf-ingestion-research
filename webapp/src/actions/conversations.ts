import { apiClient } from "~/client/fetch";
import {
  type ConversationResponse,
  type MessageResponse,
} from "~/models/conversations";

export const createConversation = async () => {
  const response =
    await apiClient.post<ConversationResponse>(`/api/conversations`);

  return response.data;
};

export const sendMessage = async (
  conversationId: string,
  message: string,
): Promise<MessageResponse> => {
  const response = await apiClient.post<MessageResponse>(
    `/api/conversations/${conversationId}/messages`,
    {
      message,
    },
  );

  return response.data;
};

export const askChatbot = async (conversationId: string) => {
  const response = await apiClient.post<MessageResponse>(
    `/api/conversations/${conversationId}/chat`,
  );

  return response.data;
};
