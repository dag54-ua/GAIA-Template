// [Feature: Incident Management] [Story: INC-USER-003] [Ticket: INC-USER-003-FE-T03]
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { useDeleteIncident } from "../api/delete-incident";

interface DeleteIncidentDialogProps {
  incidentId: string;
  incidentTitle: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function DeleteIncidentDialog({
  incidentId,
  incidentTitle,
  open,
  onOpenChange,
}: DeleteIncidentDialogProps) {
  const { mutate: deleteIncident, isPending } = useDeleteIncident();

  const handleDelete = () => {
    deleteIncident(incidentId, {
      onSuccess: () => {
        onOpenChange(false);
      },
    });
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Incident</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete "{incidentTitle}"? This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={isPending}>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            disabled={isPending}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            {isPending ? "Deleting..." : "Delete"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
