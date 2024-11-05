import { useEffect } from "react";
import { createConversation } from "../../actions/conversations";
import ConversationContainer from "../../components/chat/ConversationContainer";
import { useHomepageConversationStore } from "../../state/conversations";
import { useHomepageStudentStore } from "../../state/student";
import { createStudent } from "../../actions/students";

const ChatPage = () => {
  const { conversationId, setConversationId } = useHomepageConversationStore(
    (state) => ({
      conversationId: state.conversationId,
      setConversationId: state.setConversationId,
    }),
  );

  const { studentId, setStudentId, hasLoadedStudent } = useHomepageStudentStore(
    (state) => ({
      studentId: state.studentId,
      setStudentId: state.setStudentId,
      hasLoadedStudent: state._hasHydrated,
    }),
  );

  // Create student and conversation if no student or conversation
  useEffect(() => {
    if (hasLoadedStudent && !studentId && !conversationId) {
      const handleCreateStudent = async () => {
        const student = await createStudent();
        setStudentId(student.id);

        const conversation = await createConversation(student.id);
        setConversationId(conversation.id);
      };

      void handleCreateStudent();
    }
  }, [
    hasLoadedStudent,
    studentId,
    conversationId,
    setStudentId,
    setConversationId,
  ]);

  return (
    <main className="flex flex-col items-center">
      <div className="h-screen w-full">
        {conversationId && (
          <ConversationContainer conversationId={conversationId} />
        )}
      </div>
    </main>
  );
};

export default ChatPage;
