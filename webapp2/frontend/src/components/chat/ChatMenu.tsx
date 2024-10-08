import React from "react";
import { Student } from "@phosphor-icons/react/dist/ssr";

interface ChatMenuProps {
  isMenuOpen: boolean;
  onOpenMenu: () => void;
}

const ChatMenu: React.FC<ChatMenuProps> = ({ isMenuOpen, onOpenMenu }) => {
  return (
    <div className="relative col-span-1 hidden md:block">
      {isMenuOpen ? (
        <div className="fixed right-4 top-4 z-10">
          <ul className="menu w-56 rounded-box bg-base-200">
            <li>
              <a>
                <Student size={24} /> My Profile
              </a>
            </li>
          </ul>
        </div>
      ) : (
        <button
          className="btn btn-square fixed right-4 top-4 z-10"
          onClick={onOpenMenu}
        >
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
    </div>
  );
};

export default ChatMenu;
