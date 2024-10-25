import React, { useState } from "react";
import { Student } from "@phosphor-icons/react/dist/ssr";

import { Dialog, DialogTrigger } from "../ui/dialog";
import SettingsCard from "../settings/SettingsCard";
import { useHomepageStudentStore } from "../../state/student";

interface ChatMenuProps {
  isMenuOpen: boolean;
  onOpenMenu: () => void;
}

const ChatMenu: React.FC<ChatMenuProps> = ({ isMenuOpen, onOpenMenu }) => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  const { studentId } = useHomepageStudentStore((state) => ({
    studentId: state.studentId,
  }));

  return (
    <>
      <Dialog open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
        {isMenuOpen ? (
          <ul className="menu w-56 rounded-box bg-base-200">
            <li>
              <DialogTrigger>
                <Student size={24} /> My Profile
              </DialogTrigger>
            </li>
          </ul>
        ) : (
          // </div>
          <button className="btn btn-square" onClick={onOpenMenu}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              className="h-6 w-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        )}

        {studentId && (
          <SettingsCard
            studentId={studentId}
            onClose={() => setIsSettingsOpen(false)}
          />
        )}
      </Dialog>
    </>
  );
};

export default ChatMenu;
