import UserWidget from "@/components/auth/UserWidget.tsx";
import AuthenticatedView from "@/components/common/AuthenticatedView.tsx";
import type { QueryClient } from "@tanstack/query-core";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Outlet, createRootRouteWithContext } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";

interface RouterContext {
  queryClient: QueryClient;
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: () => (
    <>
      <AuthenticatedView>
        <main className="flex h-dvh">
          <section className="h-full w-[70px] bg-slate-900">Guilds</section>
          <section className="h-full w-1/6 bg-slate-800">Channels</section>
          <section className="h-full flex-1 bg-slate-700">
            <Outlet />
          </section>
          <section className="h-full w-1/6 bg-slate-800">Friends</section>

          <UserWidget />
        </main>
      </AuthenticatedView>

      <TanStackRouterDevtools />
      <ReactQueryDevtools />
    </>
  ),
});
