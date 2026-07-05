// ── AAKAAR:STAMPED_TYPES (do not remove this marker) ──────────────────────────────
// Entity interfaces are stamped here from the build contract; they mirror
// backend/schemas.py exactly. Generated components must import from this file.

export interface Session {
  id: string;
  user_id: string;
  token: string;
  expires_at: string;
  created_at: string;
}

export interface SessionCreate {
  token: string;
}

export interface ChatHistory {
  id: string;
  user_id: string;
  session_id: string;
  question: string;
  answer: string;
  source_chunk_ids: string;
  asked_at: string;
}

export interface ChatHistoryCreate {
  session_id: string;
  question: string;
  answer: string;
  source_chunk_ids: string;
}
