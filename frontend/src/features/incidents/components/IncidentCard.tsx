// [Feature: Incident Management] [Story: INC-USER-002] [Ticket: INC-USER-002-FE-T03]
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Incident } from "../types";
import { formatDistanceToNow } from "date-fns";

interface IncidentCardProps {
  incident: Incident;
}

const categoryColors: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  CLEANING: "secondary",
  NOISE: "destructive",
  MAINTENANCE: "default",
  SECURITY: "destructive",
};

export function IncidentCard({ incident }: IncidentCardProps) {
  return (
    <Card className="mb-4 hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-lg font-bold">
          {incident.title}
        </CardTitle>
        <Badge variant={categoryColors[incident.category] || "outline"}>
          {incident.category}
        </Badge>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground mb-2">
            {formatDistanceToNow(new Date(incident.created_at), { addSuffix: true })}
        </p>
        <CardDescription className="line-clamp-3">
          {incident.description}
        </CardDescription>
      </CardContent>
    </Card>
  );
}
