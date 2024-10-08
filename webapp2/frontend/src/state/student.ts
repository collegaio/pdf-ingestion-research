import { create } from "zustand";
import { persist } from "zustand/middleware";

interface StudentStore {
  studentId?: string | null;
  setStudentId: (studentId: string) => void;
  _hasHydrated: boolean;
  setHasHydrated: (hasHydrated: boolean) => void;
}

export const useHomepageStudentStore = create<StudentStore>()(
  persist(
    // (set, get)
    (set) => ({
      studentId: undefined,
      setStudentId: (studentId: string) => set({ studentId }),
      _hasHydrated: false,
      setHasHydrated: (hasHydrated: boolean) => {
        set({
          _hasHydrated: hasHydrated,
        });
      },
    }),
    {
      name: "homepage-student",
      onRehydrateStorage: () => (state) => {
        if (state) {
          state.setHasHydrated(true);
        }
      },
    },
  ),
);
