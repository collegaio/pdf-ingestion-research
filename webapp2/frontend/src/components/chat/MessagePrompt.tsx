interface MessagePromptProps {
  prompt: string;
  onClick: () => void;
}

const MessagePrompt = ({ prompt, onClick }: MessagePromptProps) => {
  return (
    <div
      className="flex h-full cursor-pointer items-center justify-center rounded-lg border border-gray-200 p-4 text-center shadow-md transition-colors duration-200 hover:bg-gray-100"
      onClick={onClick}
    >
      <p className="text-lg font-semibold">{prompt}</p>
    </div>
  );
};

export default MessagePrompt;
