import { api } from "@/lib/api.ts";
import { useQuery } from "@tanstack/react-query";
import { useMemo } from "react";

export default function useAuth() {
  const {
    isPending,
    isSuccess,
    data: authData,
  } = useQuery({
    queryKey: ["me"],
    queryFn: api.auth.me,
    staleTime: 10 * 60 * 1000,
  });

  const user = useMemo(() => authData?.data ?? null, [authData]);

  const isAuthenticated = useMemo(() => isSuccess && !!user, [isSuccess, user]);

  return { isPending, isAuthenticated, user };
}
