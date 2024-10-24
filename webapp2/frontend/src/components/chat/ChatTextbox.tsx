import { PaperPlaneRight } from "@phosphor-icons/react/dist/ssr";
import { Textarea } from "../ui/textarea";
import { useMemo, useState } from "react";
import { Button } from "../ui/button";

interface ChatTextboxProps {
  message?: string;
  setMessage: (message: string) => void;
  onSendMessage: () => void;
}

const messageNotEmpty = (message?: string) => !!message?.trim();

const ChatTextbox = ({
  message,
  setMessage,
  onSendMessage,
}: ChatTextboxProps) => {
  // TODO: possibly disable button when sending
  const messagePopulated = useMemo(() => messageNotEmpty(message), [message]);

  return (
    <div className={`flex w-full flex-row items-end space-x-4`}>
      <Textarea
        value={message}
        className="shadow-lg"
        placeholder="Type your message here."
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSendMessage();
          }
        }}
      />

      <Button
        className="p-2 shadow-lg"
        size="icon"
        onClick={onSendMessage}
        disabled={!messagePopulated}
      >
        <PaperPlaneRight color="white" size={32} />
      </Button>
    </div>
  );
};

export default ChatTextbox;
