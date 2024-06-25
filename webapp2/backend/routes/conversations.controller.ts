import { Type, TypeBoxTypeProvider } from "@fastify/type-provider-typebox";
import { FastifyError, FastifyServerOptions } from "fastify";
import { FastifyInstance } from "fastify/types/instance";
import {
  ChatRequestSchema,
  ConversationResponseSchema,
  MessageResponseSchema,
  MessagesResponseSchema,
} from "../models/conversation.model";
import {
  createConversation,
  createMessage,
  getMessagesForConversation,
  initiateChat,
} from "../services/conversations.service";

const router = (
  fastify: FastifyInstance,
  opts: FastifyServerOptions,
  done: (err?: FastifyError) => void
) => {
  fastify.withTypeProvider<TypeBoxTypeProvider>().post(
    "/",
    {
      schema: {
        response: {
          201: ConversationResponseSchema,
        },
      },
    },
    async (_, response) => {
      const conversation = await createConversation();

      return response.code(201).send(conversation);
    }
  );

  fastify.withTypeProvider<TypeBoxTypeProvider>().post(
    "/:conversationId/messages",
    {
      schema: {
        body: ChatRequestSchema,
        params: Type.Object({
          conversationId: Type.String(),
        }),
        response: {
          200: MessageResponseSchema,
        },
      },
    },
    async (request, response) => {
      const { conversationId } = request.params;

      const message = await createMessage(conversationId, request.body);

      return response.code(200).send(message);
    }
  );

  fastify.withTypeProvider<TypeBoxTypeProvider>().get(
    "/:conversationId/messages",
    {
      schema: {
        params: Type.Object({
          conversationId: Type.String(),
        }),
        response: {
          200: MessagesResponseSchema,
        },
      },
    },
    async (request, response) => {
      const { conversationId } = request.params;

      const messages = await getMessagesForConversation(conversationId);

      response.code(200).send(messages);
    }
  );

  fastify.withTypeProvider<TypeBoxTypeProvider>().post(
    "/:conversationId/chat",
    {
      schema: {
        params: Type.Object({
          conversationId: Type.String(),
        }),
        response: {
          200: MessageResponseSchema,
        },
      },
    },
    async (request, response) => {
      const { conversationId } = request.params;

      const message = await initiateChat(conversationId);

      response.code(200).send(message);
    }
  );

  done();
};

export default router;
