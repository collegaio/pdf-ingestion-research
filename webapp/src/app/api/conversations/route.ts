import { NextResponse } from "next/server";
import { ConversationResponse } from "~/models/conversations";
import { db } from "~/server/db";

export const POST = async (): Promise<NextResponse<ConversationResponse>> => {
  const conversation = await db.conversation.create({
    data: {
      name: "placeholder",
    },
  });

  return NextResponse.json({ id: conversation.id });
};
