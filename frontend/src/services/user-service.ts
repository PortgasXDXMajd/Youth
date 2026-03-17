import { httpClient } from "@/lib/http-client";
import { User } from "@/types";

export class UserService {
  static async me(): Promise<User> {
    return httpClient.get<User>("/users/me");
  }
}
