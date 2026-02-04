// [Feature: Incident Management] [Story: INC-USER-002] [Ticket: INC-USER-002-FE-T03]
// [Feature: Incident Management] [Story: INC-USER-003] [Ticket: INC-USER-003-FE-T03]
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import { Incident } from "../types";
import { formatDistanceToNow } from "date-fns";
import { DeleteIncidentDialog } from "./DeleteIncidentDialog";

interface IncidentCardProps {
  incident: Incident;
  currentUserId?: string;
}

const categoryColors: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  CLEANING: "secondary",
  NOISE: "destructive",
  MAINTENANCE: "default",
  SECURITY: "destructive",
};

export function IncidentCard({ incident, currentUserId }: IncidentCardProps) {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const isOwner = currentUserId && incident.owner_id === currentUserId;

  return (
    <>
      <Card className="mb-4 hover:shadow-md transition-shadow">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-lg font-bold">
            {incident.title}
          </CardTitle>
          <div className="flex items-center gap-2">
            <Badge variant={categoryColors[incident.category] || "outline"}>
              {incident.category}
            </Badge>
            {isOwner && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setDeleteDialogOpen(true)}
                aria-label="Delete incident"
                className="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            )}
          </div>
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

      {isOwner && (
        <DeleteIncidentDialog
          incidentId={incident.id}
          incidentTitle={incident.title}
          open={deleteDialogOpen}
          onOpenChange={setDeleteDialogOpen}
        />
      )}
    </>
  );
}
