import { useState, useEffect } from "react";
import { api } from "../api/client";
import { Session } from "../types";

export default function Sessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newToken, setNewToken] = useState("");

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get("/api/sessions");
      setSessions(response.data);
    } catch (err: any) {
      setError(err.message || "Failed to fetch sessions.");
    } finally {
      setLoading(false);
    }
  };

  const createSession = async () => {
    if (!newToken.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.post("/api/sessions", { token: newToken });
      setSessions((prev) => [...prev, response.data]);
      setNewToken("");
    } catch (err: any) {
      setError(err.message || "Failed to create session.");
    } finally {
      setLoading(false);
    }
  };

  const deleteSession = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/api/sessions/${id}`);
      setSessions((prev) => prev.filter((session) => session.id !== id));
    } catch (err: any) {
      setError(err.message || "Failed to delete session.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Sessions</h1>
      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <div className="mb-4">
        <input
          type="text"
          placeholder="New session token"
          value={newToken}
          onChange={(e) => setNewToken(e.target.value)}
          className="border p-2 rounded w-full mb-2"
        />
        <button
          onClick={createSession}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Create Session
        </button>
      </div>
      {sessions.length === 0 && !loading && (
        <p className="text-gray-500">No sessions found.</p>
      )}
      <ul className="space-y-4">
        {sessions.map((session) => (
          <li
            key={session.id}
            className="border p-4 rounded flex justify-between items-center"
          >
            <div>
              <p className="font-bold">Token: {session.token}</p>
              <p className="text-sm text-gray-500">
                Expires At: {new Date(session.expires_at).toLocaleString()}
              </p>
              <p className="text-sm text-gray-500">
                Created At: {new Date(session.created_at).toLocaleString()}
              </p>
            </div>
            <button
              onClick={() => deleteSession(session.id)}
              className="bg-red-500 text-white px-4 py-2 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}