export interface User {
  id: string;
  created: Date;
  modified: Date;
  username: string;
  discriminator: number;
  full_username: string;
  email: string;
  avatar: string | null;
  cover: string | null;
}
