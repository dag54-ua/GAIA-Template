// [Feature: Incident Management] [Story: INC-USER-001] [Ticket: INC-USER-001-FE-T03]
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { CreateIncidentInput } from "../schemas";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const createIncident = async (data: CreateIncidentInput) => {
  const response = await axios.post(`${API_BASE_URL}/incidents`, data);
  return response.data;
};

export const useCreateIncident = () => {
  return useMutation({
    mutationFn: createIncident,
  });
};
