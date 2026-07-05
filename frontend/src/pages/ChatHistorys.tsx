import { useEffect, useState } from "react";
import { api } from "../api/client";
import { ChatHistory } from "../types";

export default function ChatHistorys() {
  const [chatHistories, setChatHistories] = useState<ChatHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newChatHistory, setNewChatHistory] = useState<Partial<ChatHistory>>({
    question: "",
    answer: "",
    source_chunk_ids: [],
  });

  useEffect(() => {
    const fetchChatHistories = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get("/api/chat_history");
        setChatHistories(response.data);
      } catch (err: any) {
        setError(err.message || "Failed to fetch chat histories.");
      } finally {
        setLoading(false);
      }
    };

    fetchChatHistories();
  }, []);

  const handleCreate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post("/api/chat_history", newChatHistory);
      setChatHistories((prev) => [...prev, response.data]);
      setNewChatHistory({ question: "", answer: "", source_chunk_ids: [] });
    } catch (err: any) {
      setError(err.message || "Failed to create chat history.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (id: string, updatedFields: Partial<ChatHistory>) => {
    setLoading(true);
    setError(null);
    try {
      await api.patch(`/api/chat_history/${id}`, updatedFields);
      setChatHistories((prev) =>
        prev.map((chatHistory) =>
          chatHistory.id === id ? { ...chatHistory, ...updatedFields } : chatHistory
        )
      );
    } catch (err: any) {
      setError(err.message || "Failed to update chat history.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/api/chat_history/${id}`);
      setChatHistories((prev) => prev.filter((chatHistory) => chatHistory.id !== id));
    } catch (err: any) {
      setError(err.message || "Failed to delete chat history.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Chat Histories</h1>
      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <div className="mb-4">
        <h2 className="text-xl font-semibold">Create New Chat History</h2>
        <div className="flex flex-col gap-2">
          <input
            type="text"
            placeholder="Question"
            value={newChatHistory.question || ""}
            onChange={(e) =>
              setNewChatHistory((prev) => ({ ...prev, question: e.target.value }))
            }
            className="border p-2 rounded"
          />
          <input
            type="text"
            placeholder="Answer"
            value={newChatHistory.answer || ""}
            onChange={(e) =>
              setNewChatHistory((prev) => ({ ...prev, answer: e.target.value }))
            }
            className="border p-2 rounded"
          />
          <input
            type="text"
            placeholder="Source Chunk IDs (comma-separated)"
            value={newChatHistory.source_chunk_ids?.join(",") || ""}
            onChange={(e) =>
              setNewChatHistory((prev) => ({
                ...prev,
                source_chunk_ids: e.target.value.split(",").map((id) => id.trim()),
              }))
            }
            className="border p-2 rounded"
          />
          <button
            onClick={handleCreate}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Create
          </button>
        </div>
      </div>
      <div>
        <h2 className="text-xl font-semibold mb-4">Existing Chat Histories</h2>
        {chatHistories.length === 0 ? (
          <p className="text-gray-500">No chat histories found.</p>
        ) : (
          <ul className="space-y-4">
            {chatHistories.map((chatHistory) => (
              <li
                key={chatHistory.id}
                className="border p-4 rounded flex flex-col gap-2"
              >
                <div>
                  <strong>Question:</strong> {chatHistory.question}
                </div>
                <div>
                  <strong>Answer:</strong> {chatHistory.answer}
                </div>
                <div>
                  <strong>Source Chunk IDs:</strong>{" "}
                  {chatHistory.source_chunk_ids.join(", ")}
                </div>
                <div>
                  <strong>Asked At:</strong> {new Date(chatHistory.asked_at).toLocaleString()}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() =>
                      handleUpdate(chatHistory.id, { answer: "Updated Answer" })
                    }
                    className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
                  >
                    Update Answer
                  </button>
                  <button
                    onClick={() => handleDelete(chatHistory.id)}
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}