import { Static, Type } from "@fastify/type-provider-typebox";

// DTOs
export enum MessageRoles {
  User = "USER",
  System = "SYSTEM",
  Chatbot = "CHATBOT",
}

// Requests
export const ChatRequestSchema = Type.Object({
  message: Type.String(),
});

export type ChatRequest = Static<typeof ChatRequestSchema>;

// Responses
export const ConversationResponseSchema = Type.Object({
  id: Type.String(),
});

export type ConversationResponse = Static<typeof ConversationResponseSchema>;

export const MessageResponseSchema = Type.Object({
  id: Type.String(),
  text: Type.String(),
  role: Type.Enum(MessageRoles),
  createdAt: Type.String({ format: "date-time" }),
  updatedAt: Type.String({ format: "date-time" }),
});

export type MessageResponse = Static<typeof MessageResponseSchema>;

export const MessagesResponseSchema = Type.Object({
  messages: Type.Array(MessageResponseSchema),
});

export type MessagesResponse = Static<typeof MessagesResponseSchema>;

// Routes
export type ConversationIDRouteParams = { params: { conversationId: string } };
