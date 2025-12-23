import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

type Event = {
  id: number;
  name: string;
  date: string;
  venue?: string;
};

export default function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  useEffect(() => {
    const token = localStorage.getItem("token");
    axios.get("/api/v1/events", { headers: { Authorization: `Bearer ${token}` } }).then(res => setEvents(res.data));
  }, []);
  return (
    <div>
      <h1 className="text-xl font-bold">Events</h1>
      <div className="mt-4">
        {events.map(e => (
          <div key={e.id} className="bg-white p-4 rounded mb-2 shadow">
            <div className="flex justify-between">
              <div>
                <div className="font-semibold">{e.name}</div>
                <div className="text-sm text-gray-600">{new Date(e.date).toLocaleString()}</div>
              </div>
              <div>
                <Link to={`/events/${e.id}`} className="text-blue-600">View</Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
