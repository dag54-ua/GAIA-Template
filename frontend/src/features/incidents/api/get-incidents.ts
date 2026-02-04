// [Feature: Incident Management] [Story: INC-USER-002] [Ticket: INC-USER-002-FE-T03]
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Incident } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const useIncidents = (limit = 50, offset = 0) => {
  return useQuery({
    queryKey: ["incidents", limit, offset],
    queryFn: async (): Promise<Incident[]> => {
      const response = await axios.get(`${API_BASE_URL}/incidents`, {
        params: { limit, offset },
      });
      return response.data;
    },
  });
};
