import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ConversationStore {
  conversationId?: string | null;
  setConversationId: (conversationId: string) => void;
  _hasHydrated: boolean;
  setHasHydrated: (hasHydrated: boolean) => void;
}

export const useHomepageConversationStore = create<ConversationStore>()(
  persist(
    (set, _) => ({
      conversationId: undefined,
      setConversationId: (conversationId: string) => set({ conversationId }),
      _hasHydrated: false,
      setHasHydrated: (hasHydrated: boolean) => {
        set({
          _hasHydrated: hasHydrated,
        });
      },
    }),
    {
      name: "homepage-conversation",
      onRehydrateStorage: () => (state) => {
        if (state) {
          state.setHasHydrated(true);
        }
      },
    },
  ),
);
