// [Feature: Incident Management] [Story: INC-USER-003] [Ticket: INC-USER-003-FE-T03]
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const useDeleteIncident = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (incidentId: string) => {
      await axios.delete(`${API_BASE_URL}/incidents/${incidentId}`);
    },
    onSuccess: () => {
      // Invalidate and refetch incidents list
      queryClient.invalidateQueries({ queryKey: ["incidents"] });
    },
  });
};
