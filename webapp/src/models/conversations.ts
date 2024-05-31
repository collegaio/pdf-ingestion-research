import { z } from "zod";

// DTOs
export enum MessageRoles {
  User = "USER",
  System = "SYSTEM",
  Chatbot = "CHATBOT",
}

// Requests
export const ChatRequestSchema = z.object({
  message: z.string(),
});

export type ChatRequest = z.infer<typeof ChatRequestSchema>;

// Responses
export const ConversationResponseSchema = z.object({
  id: z.string(),
});

export type ConversationResponse = z.infer<typeof ConversationResponseSchema>;

export const MessageResponseSchema = z.object({
  id: z.string(),
  text: z.string(),
  role: z.nativeEnum(MessageRoles),
  createdAt: z.string().date(),
  updatedAt: z.string().date(),
});

export type MessageResponse = z.infer<typeof MessageResponseSchema>;

export const MessagesResponseSchema = z.object({
  messages: z.array(MessageResponseSchema),
});

export type MessagesResponse = z.infer<typeof MessagesResponseSchema>;

// Routes
export type ConversationIDRouteParams = { params: { conversationId: string } };
