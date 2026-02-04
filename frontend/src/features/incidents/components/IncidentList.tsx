// [Feature: Incident Management] [Story: INC-USER-002] [Ticket: INC-USER-002-FE-T03]
import { useIncidents } from "../api/get-incidents";
import { IncidentCard } from "./IncidentCard";
import { Loader2 } from "lucide-react";

export function IncidentList() {
  const { data: incidents, isLoading, isError } = useIncidents();

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center p-8 text-destructive">
        Failed to load incidents. Please try again later.
      </div>
    );
  }

  if (!incidents || incidents.length === 0) {
    return (
      <div className="text-center p-12 text-muted-foreground border-2 border-dashed rounded-lg">
        No incidents reported.
      </div>
    );
  }

  return (
    <div className="space-y-4 max-w-2xl mx-auto">
        {incidents.map((incident) => (
            <IncidentCard key={incident.id} incident={incident} />
        ))}
    </div>
  );
}
