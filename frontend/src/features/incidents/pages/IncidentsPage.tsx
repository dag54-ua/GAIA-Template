// [Feature: Incident Management] [Story: INC-USER-002] [Ticket: INC-USER-002-FE-T03]
import { IncidentList } from "../components/IncidentList";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Plus } from "lucide-react";

export default function IncidentsPage() {
  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Community Incidents</h1>
        <Button asChild>
            <Link to="/incidents/new">
                <Plus className="mr-2 h-4 w-4" /> Report Issue
            </Link>
        </Button>
      </div>
      <IncidentList />
    </div>
  );
}
