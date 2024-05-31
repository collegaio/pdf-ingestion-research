import { type NextRequest, NextResponse } from "next/server";
import { db } from "~/server/db";

import {
  MessageRoles,
  type ConversationIDRouteParams,
} from "~/models/conversations";
import { callChatAPI } from "~/server/chatApi";
import { type Message } from "@prisma/client";

export const POST = async (
  request: NextRequest,
  { params }: ConversationIDRouteParams,
) => {
  const conversation = await db.conversation.findFirst({
    where: { id: params.conversationId },
    include: {
      messages: true,
    },
  });

  if (!conversation) {
    return NextResponse.json(
      { error: `Conversation ${params.conversationId} not found` },
      { status: 404 },
    );
  }

  // TODO: move to service level
  let hasAllNewMessages = false;
  const foundMessages: Message[] = [];
  const history: Message[] = [];

  for (const message of conversation.messages.reverse()) {
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
    history.reverse().map((message) => message.text),
  );

  const responseMessage = await db.message.create({
    data: {
      conversation_id: params.conversationId,
      text: response,
      role: "CHATBOT",
    },
  });

  return NextResponse.json(responseMessage);
};
