import type { User } from "@/lib/types/auth.ts";
import type {
  CreateGuildSchema,
  Guild,
  UpdateGuildSchema,
} from "@/lib/types/guilds.ts";
import { QueryClient, keepPreviousData } from "@tanstack/query-core";
import axios, { type AxiosResponse } from "axios";

const baseURL = "/api";

export const axi = axios.create({ baseURL });

export const api = {
  auth: {
    me: async (): Promise<AxiosResponse<User>> => await axi.get("/auth/me"),
  },
  guilds: {
    list: async (): Promise<AxiosResponse<Guild[]>> => await axi.get("/guilds"),
    create: async (body: CreateGuildSchema): Promise<AxiosResponse<Guild>> =>
      await axi.post("/guilds", body),
    get: async (id: string): Promise<AxiosResponse<Guild>> =>
      await axi.get(`/guilds/${id}`),
    update: async (
      id: string,
      body: UpdateGuildSchema,
    ): Promise<AxiosResponse<Guild>> => await axi.patch(`/guilds/${id}`, body),
    delete: async (id: string): Promise<AxiosResponse<string>> =>
      await axi.delete(`/guilds/${id}`, { responseType: "text" }),
  },
};

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: true,
      refetchOnMount: true,
      refetchOnReconnect: true,
      placeholderData: keepPreviousData,
      retry: false,
    },
    mutations: {
      retry: false,
    },
  },
});
