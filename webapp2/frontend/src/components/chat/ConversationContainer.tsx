import useSWR from "swr";
// import { MessageRoles, type MessagesResponse } from "~/models/conversations";
import { type ErrorResponse } from "../../models/errors";
import { askChatbot, sendMessage } from "../../actions/conversations";
import { useEffect, useMemo, useRef, useState } from "react";
import { createId } from "@paralleldrive/cuid2";
import { fetchJSON } from "../../clients/fetch";
import { MessageRoles, MessagesResponse } from "../../models/conversations";
import ChatMenu from "./ChatMenu";
import ChatTextbox from "./ChatTextbox";
import MessagePrompt from "./MessagePrompt";
interface ConversationContainerProps {
  conversationId: string;
}

const prompts = [
  "What are the application deadlines for [School Name]?",
  "What are the admission requirements for [School Name]?",
  "How can I improve my chances of admission?",
  "What scholarships are available for [Major/Program]?",
  "How do I write a strong personal statement?",
  "What are the application deadlines for [School Name]?",
];

const ConversationContainer = ({
  conversationId,
}: ConversationContainerProps) => {
  const [message, setMessage] = useState("");
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

      try {
        const reply = await askChatbot(conversationId);

        setHasSentMessage(false);

        await mutateMessages({
          messages: [...messagesResponse.messages, reply],
        });
      } catch (error) {
        console.error("Error asking chatbot:", error);
      } finally {
        setIsLoadingReply(false);
      }
    };

    const timeoutId = setTimeout(() => {
      // check if last message sent is from user and user has sent message
      void handleAskChatbot();
    }, 2_000);

    return () => clearTimeout(timeoutId);
  }, [hasSentMessage, conversationId, messagesResponse, mutateMessages]);

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

  const hasMessages = useMemo(() => {
    return !isLoadingMessages && (messagesResponse?.messages.length ?? 0) > 0;
  }, [isLoadingMessages, messagesResponse?.messages.length]);

  return (
    <div className="grid h-full grid-cols-6 gap-4" onClick={handleCloseMenu}>
      <div className="col-span-1 hidden md:block" />

      <div className="col-span-6 mx-4 flex h-full w-auto flex-grow flex-col rounded-lg md:col-span-4 md:mx-0">
        {!hasMessages ? (
          <div className="flex h-full w-full flex-grow flex-col items-center justify-center space-y-8">
            <h1 className="text-center text-4xl font-extrabold tracking-tight md:text-6xl">
              Welcome to Collega!
            </h1>

            <div className="grid grid-cols-2 gap-4">
              {prompts.map((prompt) => (
                <MessagePrompt
                  prompt={prompt}
                  onClick={() => setMessage(prompt)}
                />
              ))}
            </div>

            <ChatTextbox
              message={message}
              setMessage={setMessage}
              onSendMessage={handleSendMessage}
            />
          </div>
        ) : (
          <div className="flex w-full flex-grow flex-col">
            <div className="flex-grow space-y-2 overflow-y-auto p-4">
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

              {isLoadingReply && (
                <div className="chat chat-start">
                  <div className="chat-bubble shadow-lg">
                    <span className="loading loading-bars" />
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>
        )}

        {hasMessages && (
          <ChatTextbox
            message={message}
            setMessage={setMessage}
            onSendMessage={handleSendMessage}
          />
        )}
      </div>

      <div className="col-span-1">
        <ChatMenu
          isMenuOpen={isMenuOpen}
          onOpenMenu={() => setIsMenuOpen(true)}
        />
      </div>
    </div>
  );
};

export default ConversationContainer;
