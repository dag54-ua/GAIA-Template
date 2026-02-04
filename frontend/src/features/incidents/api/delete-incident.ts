// [Feature: Incident Management] [Story: INC-USER-003] [Ticket: INC-USER-003-FE-T03]
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const useDeleteIncident = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (incidentId: string) => {
      // TODO: Replace with actual auth when available
      const mockUserId = localStorage.getItem("mock_user_id") || "00000000-0000-0000-0000-000000000001";
      
      await axios.delete(`${API_BASE_URL}/incidents/${incidentId}`, {
        headers: {
          "X-User-Id": mockUserId,
        },
      });
    },
    onSuccess: () => {
      // Invalidate and refetch incidents list
      queryClient.invalidateQueries({ queryKey: ["incidents"] });
    },
  });
};
