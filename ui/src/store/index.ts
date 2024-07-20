import process from "node:process";
import { create } from "zustand";
import { createJSONStorage, devtools, persist } from "zustand/middleware";

interface AppState {
  count: number;
}

interface AppActions {
  setCount: (count: number) => void;
}

const initialState: AppState = {
  count: 0,
};

export const useStore = create<AppState & AppActions>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,
        setCount: (count) => set((state) => ({ count })),
      }),
      {
        name: "fastcord-store",
        storage: createJSONStorage(() => localStorage),
      },
    ),
    { enabled: process.env.NODE_ENV !== "production" },
  ),
);
