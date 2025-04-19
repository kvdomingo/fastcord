import Google from "@/components/icons/Google.tsx";
import { Button } from "@/components/ui/button.tsx";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card.tsx";

const subdomain =
  import.meta.env.VITE_STYTCH_ENVIRONMENT === "test" ? "test" : "api";

const loginURL = `https://${subdomain}.stytch.com/v1/public/oauth/google/start?public_token=${import.meta.env.VITE_STYTCH_PUBLIC_TOKEN}`;

export default function Login() {
  return (
    <div className="flex h-dvh items-center justify-center">
      <Card className="w-[400px]">
        <CardHeader className="flex flex-col items-center">
          <CardTitle>Fastcord</CardTitle>
          <CardDescription>Login</CardDescription>
        </CardHeader>
        <CardContent className="flex justify-center">
          <a href={loginURL}>
            <Button className="cursor-pointer">
              <Google className="fill-blue-500" />
              Login with Google
            </Button>
          </a>
        </CardContent>
      </Card>
    </div>
  );
}
