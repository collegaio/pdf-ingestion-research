import { apiClient } from "../clients/fetch";
import {
  type ConversationResponse,
  type MessageResponse,
} from "../models/conversations";

export const createConversation = async (studentId: string) => {
  const response = await apiClient.post<ConversationResponse>(
    `/conversations`,
    {
      studentId,
    },
  );

  return response.data;
};

export const sendMessage = async (
  conversationId: string,
  message: string,
): Promise<MessageResponse> => {
  const response = await apiClient.post<MessageResponse>(
    `/conversations/${conversationId}/messages`,
    {
      message,
    },
  );

  return response.data;
};

export const askChatbot = async (conversationId: string) => {
  const response = await apiClient.post<MessageResponse>(
    `/conversations/${conversationId}/chat`,
  );

  return response.data;
};
