import { httpClient } from "@/lib/http-client";
import { AuthData } from "@/types";

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";

export class AuthService {
  static async login(email: string, password: string): Promise<string> {
    const data = await httpClient.post<AuthData>("/auth/login", {
      email,
      password,
    });
    return data.access_token;
  }

  static async register(email: string, password: string): Promise<void> {
    await httpClient.post("/auth/register", { email, password });
  }

  static async googleAuth(code: string, redirectUri: string): Promise<string> {
    const data = await httpClient.post<AuthData>("/auth/google", {
      code,
      redirect_uri: redirectUri,
    });
    return data.access_token;
  }

  static getGoogleAuthUrl(): string {
    const redirectUri = `${window.location.origin}/callback`;
    const params = new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      redirect_uri: redirectUri,
      response_type: "code",
      scope: "openid email profile",
      access_type: "offline",
      prompt: "consent",
    });
    return `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
  }
}
