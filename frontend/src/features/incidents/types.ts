// [Feature: Incident Management] [Story: INC-USER-002] [Ticket: INC-USER-002-FE-T03]
import { IncidentCategory } from "./schemas";

export interface Incident {
  id: string;
  title: string;
  description: string;
  category: z.infer<typeof IncidentCategory>;
  created_at: string;
  owner_id: string;
}

export type IncidentListResponse = Incident[];
