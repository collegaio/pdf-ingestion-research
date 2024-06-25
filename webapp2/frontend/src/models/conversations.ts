export enum MessageRoles {
  User = "USER",
  System = "SYSTEM",
  Chatbot = "CHATBOT",
}

// export const ChatRequestSchema = z.object({
//   message: z.string(),
// });

// Responses
export interface ConversationResponse {
  id: string;
}

export interface MessageResponse {
  id: string;
  text: string;
  role: MessageRoles;
  createdAt: string;
  updatedAt: string;
}

export interface MessagesResponse {
  messages: MessageResponse[];
}
