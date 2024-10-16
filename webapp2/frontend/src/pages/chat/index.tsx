import { useEffect } from "react";
import { createConversation } from "../../actions/conversations";
import ConversationContainer from "../../components/chat/ConversationContainer";
import { useHomepageConversationStore } from "../../state/conversations";
import { useHomepageStudentStore } from "../../state/student";
import { createStudent } from "../../actions/students";

const ChatPage = () => {
  const { conversationId, setConversationId, hasLoadedConversation } =
    useHomepageConversationStore((state) => ({
      conversationId: state.conversationId,
      setConversationId: state.setConversationId,
      hasLoadedConversation: state._hasHydrated,
    }));

  const { studentId, setStudentId, hasLoadedStudent } = useHomepageStudentStore(
    (state) => ({
      studentId: state.studentId,
      setStudentId: state.setStudentId,
      hasLoadedStudent: state._hasHydrated,
    }),
  );

  // Create conversation if no conversation
  useEffect(() => {
    const handleCreateConversation = async (studentId: string) => {
      const conversation = await createConversation(studentId);
      setConversationId(conversation.id);
    };

    if (hasLoadedConversation && !conversationId && studentId) {
      void handleCreateConversation(studentId);
    }
  }, [conversationId, hasLoadedConversation, studentId, setConversationId]);

  // Create student if no student
  useEffect(() => {
    if (hasLoadedStudent && !studentId) {
      const handleCreateStudent = async () => {
        const student = await createStudent();
        setStudentId(student.id);
      };

      void handleCreateStudent();
    }
  }, [hasLoadedStudent, studentId, setStudentId]);

  console.log("conversationId:", conversationId);
  console.log("studentId:", studentId);

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
