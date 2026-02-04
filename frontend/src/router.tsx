import { createBrowserRouter } from "react-router-dom";
import AppLayout from "@/layouts/AppLayout";
import CreateIncidentPage from "@/features/incidents/pages/CreateIncidentPage";
import IncidentsPage from "@/features/incidents/pages/IncidentsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
        {
            path: "incidents/new",
            element: <CreateIncidentPage />
        },
        {
            path: "incidents",
            element: <IncidentsPage />
        }
    ]
  },
]);
