// [Feature: Incident Management] [Story: INC-USER-001] [Ticket: INC-USER-001-FE-T03]
import { z } from "zod";

export const IncidentCategory = z.enum(["CLEANING", "NOISE", "MAINTENANCE", "SECURITY"]);
export type IncidentCategory = z.infer<typeof IncidentCategory>;

export const createIncidentSchema = z.object({
  title: z.string().min(1, "Title is required").max(100, "Title must be less than 100 characters"),
  description: z.string().min(1, "Description is required").max(500, "Description must be less than 500 characters"),
  category: IncidentCategory,
});

export type CreateIncidentInput = z.infer<typeof createIncidentSchema>;
