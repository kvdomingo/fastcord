import Login from "@/components/auth/Login.tsx";
import FullPageLoading from "@/components/common/FullPageLoading.tsx";
import useAuth from "@/hooks/useAuth.ts";
import type { PropsWithChildren } from "react";

export default function AuthenticatedView({ children }: PropsWithChildren) {
  const { isPending, isAuthenticated } = useAuth();

  return isPending ? (
    <FullPageLoading />
  ) : isAuthenticated ? (
    children
  ) : (
    <Login />
  );
}
