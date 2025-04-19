import { Button } from "@/components/ui/button.tsx";
import { CommandDialog, CommandInput } from "@/components/ui/command.tsx";
import { Separator } from "@/components/ui/separator.tsx";
import { Link, useLocation } from "@tanstack/react-router";
import { Rocket, Store, Users } from "lucide-react";
import { useState } from "react";

const navButtons = [
  {
    label: "Friends",
    Icon: Users,
    href: "/",
  },
  {
    label: "Nitro",
    Icon: Rocket,
    href: "/nitro",
  },
  {
    label: "Shop",
    Icon: Store,
    href: "/shop",
  },
];

export default function DirectMessageList() {
  const { pathname } = useLocation();
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  return (
    <div className="flex flex-col gap-4 p-2">
      <div>
        <Button
          className="w-full cursor-pointer"
          variant="outline"
          onClick={() => setIsSearchOpen(true)}
        >
          Find or start a conversation
        </Button>
        <CommandDialog open={isSearchOpen} onOpenChange={setIsSearchOpen}>
          <CommandInput placeholder="Find or start a conversation" />
        </CommandDialog>
      </div>

      <div className="flex flex-col gap-1">
        {navButtons.map(({ Icon, ...nav }) => (
          <Link to={nav.href} key={nav.href}>
            <Button
              variant={pathname === nav.href ? "default" : "ghost"}
              className="flex w-full cursor-pointer justify-start"
            >
              <Icon />
              {nav.label}
            </Button>
          </Link>
        ))}
      </div>

      <Separator />
    </div>
  );
}
