import { Outlet } from "react-router-dom";

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b">
        <div className="container mx-auto py-4 flex justify-between items-center">
             <div className="font-bold text-xl text-primary">Community App</div>
             <nav className="space-x-4">
                 <a href="/incidents" className="text-sm font-medium hover:text-primary">Incidents</a>
             </nav>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
