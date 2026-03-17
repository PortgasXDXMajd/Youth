export interface User {
  email: string;
  created_at: string;
  provider: string;
}

export interface ApiResponse<T> {
  data: T;
  msg?: string;
}

export interface AuthData {
  access_token: string;
}
