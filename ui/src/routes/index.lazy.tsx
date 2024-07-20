import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="flex h-screen w-full">
      <div className="w-[70px] bg-ctp-surface2">Guilds</div>
      <div className="w-[250px] bg-ctp-surface1">Channels</div>
      <div className="flex-auto bg-ctp-surface0">Main</div>
      <div className="w-[250px] bg-ctp-surface1">Members</div>
    </div>
  );
}
