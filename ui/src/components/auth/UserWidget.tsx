import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar.tsx";
import { Button } from "@/components/ui/button.tsx";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu.tsx";
import useAuth from "@/hooks/useAuth.ts";

export default function UserWidget() {
  const { user } = useAuth();

  return (
    <div className="absolute bottom-0 left-0 m-2 flex w-[350px] items-center gap-4 rounded-lg bg-slate-950 p-4">
      <Avatar>
        <AvatarImage src={user?.avatar ?? ""} />
        <AvatarFallback>
          {user?.username.slice(0, 2).toUpperCase() ?? "UU"}
        </AvatarFallback>
      </Avatar>

      <DropdownMenu>
        <DropdownMenuTrigger>
          <Button variant="ghost" className="cursor-pointer">
            {user?.full_username ?? "Unknown User"}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <a href={`${import.meta.env.VITE_API_HOST}/api/auth/logout`}>
            <DropdownMenuItem className="cursor-pointer">
              Logout
            </DropdownMenuItem>
          </a>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
