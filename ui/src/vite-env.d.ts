/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_STYTCH_ENVIRONMENT: "test" | "live";
  readonly VITE_STYTCH_PUBLIC_TOKEN: string;
  readonly VITE_APP_HOST: string;
  readonly VITE_API_HOST: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
