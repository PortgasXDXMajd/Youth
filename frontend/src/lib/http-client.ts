import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { ApiResponse } from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_PREFIX = "/api/v1";

export class HttpClient {
  private client: AxiosInstance;

  constructor(baseURL: string = BASE_URL, prefix: string = API_PREFIX) {
    this.client = axios.create({
      baseURL: `${baseURL}${prefix}`,
      headers: { "Content-Type": "application/json" },
    });

    this.client.interceptors.request.use((config) => {
      if (typeof window !== "undefined") {
        const token = localStorage.getItem("token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      }
      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        const message =
          error.response?.data?.msg || error.message || "Request failed";
        return Promise.reject(new Error(message));
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<ApiResponse<T>>(url, config);
    return response.data.data;
  }

  async post<T>(
    url: string,
    data?: unknown,
    config?: AxiosRequestConfig
  ): Promise<T> {
    const response = await this.client.post<ApiResponse<T>>(url, data, config);
    return response.data.data;
  }
}

export const httpClient = new HttpClient();
