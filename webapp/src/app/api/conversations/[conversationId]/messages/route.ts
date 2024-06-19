import { type NextRequest, NextResponse } from "next/server";
import { db } from "~/server/db";

import {
  ChatRequestSchema,
  type MessageRoles,
  type MessagesResponse,
  type ConversationIDRouteParams,
  type MessageResponse,
} from "~/models/conversations";
import { type ErrorResponse } from "~/models/errors";

export const GET = async (
  request: NextRequest,
  { params }: ConversationIDRouteParams,
): Promise<NextResponse<MessagesResponse | ErrorResponse>> => {
  const messages = await db.message.findMany({
    where: { conversation_id: params.conversationId },
    orderBy: {
      created_at: "asc",
    },
  });

  // if (!conversation) {
  //   return NextResponse.json(
  //     { error: `Failed to find conversation with ID ${params.conversationId}` },
  //     { status: 404 },
  //   );
  // }

  return NextResponse.json({
    messages: messages.map((message) => ({
      id: message.id,
      text: message.text,
      role: message.role as MessageRoles,
      createdAt: message.created_at.toISOString(),
      updatedAt: message.updated_at.toISOString(),
    })),
  });
};

export const POST = async (
  request: NextRequest,
  { params }: ConversationIDRouteParams,
): Promise<NextResponse<MessageResponse | ErrorResponse>> => {
  const body = ChatRequestSchema.parse(await request.json());

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

  const message = await db.message.create({
    data: {
      conversation_id: params.conversationId,
      text: body.message,
      role: "USER",
    },
  });

  return NextResponse.json({
    id: message.id,
    text: message.text,
    createdAt: message.created_at.toISOString(),
    role: message.role as MessageRoles,
    updatedAt: message.updated_at.toISOString(),
  });
};
