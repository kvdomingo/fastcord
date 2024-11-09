import axios from "axios";
import { browser } from "$app/environment";
import { keepPreviousData, QueryClient } from "@tanstack/svelte-query";

const baseURL = "http://localhost:8000";

export const axi = axios.create({ baseURL });

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      enabled: browser,
      retry: 3,
      refetchOnWindowFocus: true,
      refetchOnMount: true,
      refetchOnReconnect: true,
      placeholderData: keepPreviousData,
    },
    mutations: {
      retry: false,
    },
  },
});
