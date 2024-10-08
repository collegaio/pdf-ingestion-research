import { Textarea } from "../ui/textarea";
import { PaperPlaneRight } from "@phosphor-icons/react/dist/ssr";
import useSWR from "swr";
// import { MessageRoles, type MessagesResponse } from "~/models/conversations";
import { type ErrorResponse } from "../../models/errors";
import { askChatbot, sendMessage } from "../../actions/conversations";
import { useEffect, useRef, useState } from "react";
import { createId } from "@paralleldrive/cuid2";
import { fetchJSON } from "../../clients/fetch";
import { MessageRoles, MessagesResponse } from "../../models/conversations";
import ChatMenu from "./ChatMenu";

interface ConversationContainerProps {
  conversationId: string;
}

const ConversationContainer = ({
  conversationId,
}: ConversationContainerProps) => {
  const [message, setMessage] = useState<string>();
  const [hasSentMessage, setHasSentMessage] = useState(false);
  const [isLoadingReply, setIsLoadingReply] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const {
    data: messagesResponse,
    isLoading: isLoadingMessages,
    // error: messagesError,
    mutate: mutateMessages,
  } = useSWR<MessagesResponse, ErrorResponse>(
    `/conversations/${conversationId}/messages`,
    fetchJSON,
  );

  // TODO: implement show error message

  // Wait 2 seconds after user is done sending messages to reply
  useEffect(() => {
    const handleAskChatbot = async () => {
      if (
        !hasSentMessage ||
        !(MessageRoles.User === messagesResponse?.messages.at(-1)?.role)
      ) {
        return;
      }

      setIsLoadingReply(true);
      const reply = await askChatbot(conversationId);

      setHasSentMessage(false);
      setIsLoadingReply(false);

      await mutateMessages({ messages: [...messagesResponse.messages, reply] });
    };

    const timeoutId = setTimeout(() => {
      // check if last message sent is from user and user has sent message
      void handleAskChatbot();
    }, 2_000);

    return () => clearTimeout(timeoutId);
  }, [
    message,
    hasSentMessage,
    conversationId,
    messagesResponse,
    mutateMessages,
  ]);

  // Start at bottom of screen
  useEffect(() => {
    scrollToBottom();
  }, [messagesResponse]);

  const handleSendMessage = async () => {
    if (!messagesResponse || isLoadingMessages || !message?.trim()) {
      return;
    }

    const updateFn = async () => {
      const newMessage = await sendMessage(conversationId, message);

      return {
        messages: [...messagesResponse.messages, newMessage],
      };
    };

    const optomisticNewMessages = {
      messages: [
        ...messagesResponse.messages,
        {
          id: createId(),
          text: message,
          role: MessageRoles.User,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        },
      ],
    };

    const options = {
      optimisticData: optomisticNewMessages,
    };

    await mutateMessages(updateFn(), options);
    setMessage("");
    setHasSentMessage(true);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleCloseMenu = () => {
    if (isMenuOpen) {
      setIsMenuOpen(false);
    }
  };

  return (
    <div className="grid grid-cols-6 gap-4" onClick={handleCloseMenu}>
      <div className="col-span-1 hidden md:block" />
      <div className="col-span-5 flex h-full w-full flex-grow flex-col rounded-lg md:col-span-4">
        <div className="flex w-full flex-grow flex-col items-center justify-center space-y-2">
          {!isLoadingMessages &&
          (messagesResponse?.messages.length ?? 0) < 1 ? (
            <>
              <h1 className="text-5xl font-extrabold tracking-tight">
                Welcome to Collega!
              </h1>

              <p className="text-xl">
                Get started by asking a question, like &quot;Which schools am I
                qualified for?&quot;
              </p>
            </>
          ) : (
            <></>
          )}
        </div>

        <div className="flex w-full flex-col space-y-2 overflow-y-scroll p-4">
          {messagesResponse?.messages.map((message) => (
            <div
              className={`chat ${MessageRoles.Chatbot === message.role ? "chat-start" : "chat-end"}`}
              key={message.id}
            >
              <div className="chat-bubble whitespace-pre-wrap shadow-lg">
                {message.text}
              </div>
            </div>
          ))}

          {isLoadingReply ? (
            <div className="chat chat-start">
              <div className="chat-bubble shadow-lg">
                <span className="loading loading-bars" />
              </div>
            </div>
          ) : (
            <></>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="flex w-full flex-row items-end space-x-4 p-4">
          <Textarea
            value={message}
            className="shadow-lg"
            placeholder="Type your message here."
            onChange={(e) => setMessage(e.target.value)}
          />

          <button
            className="btn btn-square bg-black shadow-lg"
            type="button"
            onClick={handleSendMessage}
          >
            <PaperPlaneRight color="white" size={32} />
          </button>
        </div>
      </div>

      <ChatMenu
        isMenuOpen={isMenuOpen}
        onOpenMenu={() => setIsMenuOpen(true)}
      />
    </div>
  );
};

export default ConversationContainer;
