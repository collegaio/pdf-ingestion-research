import { Message } from "@prisma/client";
import { db } from "../clients/db";
import {
  ChatRequest,
  MessageResponse,
  MessageRoles,
} from "../models/conversation.model";
import { callChatAPI } from "../clients/chatApi";
import { NotFoundError } from "../models/error.model";

export const createConversation = async () => {
  const conversation = await db.conversation.create({
    data: {
      name: "placeholder",
    },
  });

  return { id: conversation.id };
};

export const getMessagesForConversation = async (conversationId: string) => {
  const messages = await db.message.findMany({
    where: { conversation_id: conversationId },
    orderBy: {
      created_at: "asc",
    },
  });

  return {
    messages: messages.map((message) => ({
      id: message.id,
      text: message.text,
      role: message.role as MessageRoles,
      createdAt: message.created_at.toISOString(),
      updatedAt: message.updated_at.toISOString(),
    })),
  };
};

export const createMessage = async (
  conversationId: string,
  body: ChatRequest
) => {
  const conversation = await db.conversation.findFirst({
    where: { id: conversationId },
    include: {
      messages: true,
    },
  });

  if (!conversation) {
    throw new NotFoundError(`Conversation ${conversationId} not found`);
  }

  const message = await db.message.create({
    data: {
      conversation_id: conversationId,
      text: body.message,
      role: "USER",
    },
  });

  return {
    id: message.id,
    text: message.text,
    createdAt: message.created_at.toISOString(),
    role: message.role as MessageRoles,
    updatedAt: message.updated_at.toISOString(),
  };
};

export const initiateChat = async (
  conversationId: string
): Promise<MessageResponse> => {
  const messages = await db.message.findMany({
    where: { conversation_id: conversationId },
    orderBy: {
      created_at: "asc",
    },
  });

  // if (!conversation) {
  //   return NextResponse.json(
  //     { error: `Conversation ${params.conversationId} not found` },
  //     { status: 404 },
  //   );
  // }

  // TODO: move to service level
  let hasAllNewMessages = false;
  const foundMessages: Message[] = [];
  const history: Message[] = [];

  for (const message of messages.reverse()) {
    if (
      MessageRoles.User === (message.role as MessageRoles) &&
      !hasAllNewMessages
    ) {
      foundMessages.push(message);
    } else {
      hasAllNewMessages = true;
      history.push(message);
    }
  }

  // TODO: condense conversation (possibly on bot side)
  // TODO: don't send if last message is not from user (possibly regenerate response)
  const response = await callChatAPI(
    foundMessages
      .reverse()
      .map((message) => message.text)
      .join("\n\n"),
    history
      .reverse()
      .map((message) => ({ text: message.text, role: message.role }))
  );

  const responseMessage = await db.message.create({
    data: {
      conversation_id: conversationId,
      text: response,
      role: "CHATBOT",
    },
  });

  return {
    id: responseMessage.id,
    role: responseMessage.role as MessageRoles,
    text: responseMessage.text,
    createdAt: responseMessage.created_at.toISOString(),
    updatedAt: responseMessage.updated_at.toISOString(),
  };
};
