import { QueryClient, keepPreviousData } from "@tanstack/react-query";
import axios from "axios";

const baseURL = "/api";

export const axi = axios.create({
  baseURL,
  withCredentials: true,
});

export const api = {};

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: true,
      refetchOnMount: true,
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
      placeholderData: keepPreviousData,
    },
    mutations: {
      retry: false,
    },
  },
});
