import { Avatar, AvatarFallback } from "@/components/ui/avatar.tsx";
import { Separator } from "@/components/ui/separator.tsx";
import { cn } from "@/lib/utils.ts";
import { Link, useLocation } from "@tanstack/react-router";

export default function GuildList() {
  const { pathname } = useLocation();

  const isHome = ["/", "/shop", "/nitro"].includes(pathname);

  return (
    <div className="flex flex-col gap-2 py-2">
      <div
        className={cn("flex w-full justify-center", {
          "border-l-2 border-l-white border-solid": isHome,
        })}
      >
        <Link to="/">
          <Avatar className="size-12 cursor-pointer">
            <AvatarFallback
              className={cn({
                "rounded-lg bg-indigo-700": isHome,
              })}
            >
              FC
            </AvatarFallback>
          </Avatar>
        </Link>
      </div>

      <div className="px-4">
        <Separator />
      </div>
    </div>
  );
}
