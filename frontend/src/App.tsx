import React from "react";
import { Outlet, Link } from "react-router-dom";

export default function App() {
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <Link to="/" className="font-bold text-xl">College SaaS</Link>
          </div>
          <div className="space-x-4">
            <Link to="/events" className="text-sm">Events</Link>
            <Link to="/upload" className="text-sm">Upload</Link>
            <Link to="/checkin" className="text-sm">Check-in</Link>
            <Link to="/reports" className="text-sm">Reports</Link>
          </div>
        </div>
      </nav>
      <main className="container mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
