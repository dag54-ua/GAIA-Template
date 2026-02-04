import { useNavigate } from "react-router-dom";
import { CreateIncidentForm } from "../components/CreateIncidentForm";

// [Feature: Incident Management] [Story: INC-USER-001] [Ticket: INC-USER-001-FE-T03]
export default function CreateIncidentPage() {
  const navigate = useNavigate();

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6 text-center">Incident Management</h1>
      <CreateIncidentForm onSuccess={() => navigate("/incidents")} />
    </div>
  );
}
